import logging
import os
import json
from datetime import datetime
from typing import Dict, Any, Optional, List

import google.generativeai as genai
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler,
    filters,
    ContextTypes,
)
from supabase import create_client, Client

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Log the loaded TELEGRAM_TOKEN for debugging
token = os.environ.get("TELEGRAM_TOKEN")
logger.info(f"Loaded TELEGRAM_TOKEN: {token}")

# Validate token format (must contain ':' to ensure bot ID is included)
if not token or ":" not in token:
    logger.error("Invalid Telegram token format. Ensure it includes bot ID and hash (e.g., '123456:ABC-DEF').")
    exit(1)

# Constants for conversation states
NAME, STAGE, REVENUE, FEEDBACK = range(4)

# Project stages
STAGES = ["Idea", "Development", "Launched"]

# Configure Supabase
supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

# Configure Google AI
google_api_key = os.environ.get("GOOGLE_API_KEY")
genai.configure(api_key=google_api_key)
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    generation_config={
        "temperature": 0.7,
        "top_p": 0.9,
        "top_k": 40,
        "max_output_tokens": 150,
    },
    safety_settings=[
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
    ],
)

# Check required environment variables
required_vars = ["TELEGRAM_TOKEN", "GOOGLE_API_KEY", "SUPABASE_URL", "SUPABASE_KEY"]
missing_vars = [var for var in required_vars if not os.environ.get(var)]
if missing_vars:
    logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
    exit(1)

# Synchronous database checks
def check_tables_exist():
    try:
        response = supabase.table("projects").select("id", count="exact").limit(1).execute()
        logger.info("✅ Projects table exists")
    except Exception as e:
        logger.error(f"❌ Projects table does not exist: {e}")
        return False

    try:
        response = supabase.table("conversations").select("id", count="exact").limit(1).execute()
        logger.info("✅ Conversations table exists")
    except Exception as e:
        logger.error(f"❌ Conversations table does not exist: {e}")
        return False

    return True

def init_database():
    if not check_tables_exist():
        logger.warning("Required database tables are missing. Please run setup_db.py or create tables manually.")
    else:
        logger.info("✅ Database tables exist")

# Asynchronous functions for database operations
async def store_conversation(user_id: int, project_id: int, message: str, role: str) -> None:
    try:
        supabase.table("conversations").insert({
            "user_id": user_id,
            "project_id": project_id,
            "message": message,
            "role": role
        }).execute()
    except Exception as e:
        logger.error(f"Error storing conversation: {e}")

async def get_project_by_user_id(user_id: int) -> Optional[Dict[str, Any]]:
    try:
        response = supabase.table("projects").select("*").eq("user_id", user_id).order("created_at", desc=True).limit(1).execute()
        if response.data and len(response.data) > 0:
            return response.data[0]
        return None
    except Exception as e:
        logger.error(f"Error getting project: {e}")
        return None

async def get_conversation_history(user_id: int, limit: int = 10) -> List[Dict[str, str]]:
    try:
        response = supabase.table("conversations").select("*").eq("user_id", user_id).order("timestamp", desc=True).limit(limit).execute()
        conversation = []
        if response.data:
            for msg in reversed(response.data):
                conversation.append({"role": msg['role'], "content": msg['message']})
        return conversation
    except Exception as e:
        logger.error(f"Error getting conversation history: {e}")
        return []

async def get_ai_response(conversation_history: List[Dict[str, str]], 
                         user_message: str, 
                         project_info: Optional[Dict[str, Any]] = None) -> str:
    system_prompt = """
    You are Jeff Jr, a no-nonsense venture capitalist Telegram bot with a focus on startups, particularly in the blockchain and DeFi space on Solana. Your personality is blunt, professional, and a bit sarcastic. You value directness and efficiency in communication.

    Key Traits:
    1. **Blunt and Professional:** Provide honest feedback without sugar-coating, but remain professional.
    2. **Time-Conscious:** Keep responses concise and to the point.
    3. **Startup Expert:** Strong knowledge in MVPs, revenue models, market fit, and funding.
    4. **Critical Thinker:** Ask tough questions to help founders refine their ideas.
    5. **Blockchain and DeFi Savvy:** Expertise in crypto/blockchain projects, especially on Solana.
    6. **Calm and Collected with Sarcasm:** Maintain composure while being straightforward and occasionally sarcastic.

    Response Guidelines:
    - **Brevity:** Always limit responses to 2-3 sentences. If more detail is needed, ask the user if they want to know more.
    - **Probing Questions:** Ask about business models, revenue plans, and market fit when relevant.
    - **Constructive Criticism:** Challenge weak ideas firmly but constructively.
    - **Emojis:** Use sparingly for emphasis (max 1 per message).
    - **Actionable Advice:** Focus on practical steps the founder can take.
    - **Tone:** Friendly yet blunt, like a knowledgeable friend who doesn't hold back.
    - **Genuine Care:** Show interest in the project while being honest and direct.
    - **Handling Off-Topic Questions:** If the user asks something unrelated to their project or startup advice, respond with something like: "Hey, let's stay focused on your project. If you have questions about [topic], maybe we can discuss that later, but right now, I want to help you with your startup."

    Remember, your goal is to help founders build viable businesses by providing insightful, honest feedback and guidance. And if possible only give the ansewr in a single format as this is used for the telegram messages responses will not look good
    """
    
    chat = [{"role": "system", "content": system_prompt}]
    
    if project_info:
        project_context = f"""
        Current project information:
        - Name: {project_info.get('project_name', 'Unknown')}
        - Stage: {project_info.get('stage', 'Unknown')}
        - Revenue Goal: {project_info.get('revenue_goal', 'Unknown')}
        
        Tailor your feedback to this specific project stage and goals.
        """
        chat.append({"role": "system", "content": project_context})
    
    for message in conversation_history:
        chat.append(message)
    
    chat.append({"role": "user", "content": user_message})
    
    try:
        response = model.generate_content([msg["content"] for msg in chat])
        return response.text
    except Exception as e:
        logger.error(f"Error generating AI response: {e}")
        return "Sorry, I'm having trouble connecting to my brain right now. Try again in a moment. 🤔"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.effective_user
    logger.info(f"User {user.id} ({user.username}) started the bot")
    await update.message.reply_text(
        f"Welcome to Jeff Jr, your AI VC coach! 😎\nWhat's your project name? Be clear!"
    )
    return NAME

async def project_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    user = update.effective_user
    context.user_data["project_name"] = text
    logger.info(f"User {user.id} entered project name: {text}")
    keyboard = [
        [InlineKeyboardButton(stage, callback_data=stage)] for stage in STAGES
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f"{text}, huh? Alright:\n- What stage is it at?",
        reply_markup=reply_markup
    )
    return STAGE

async def project_stage(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    user = query.from_user
    selected_stage = query.data
    context.user_data["stage"] = selected_stage
    logger.info(f"User {user.id} selected stage: {selected_stage}")
    await query.answer()
    await query.edit_message_text(
        f"A {selected_stage.lower()}-stage {context.user_data['project_name']}? Noted.\n\n"
        f"What's your revenue goal? Be specific or I'll assume you're not serious!"
    )
    return REVENUE

async def revenue_goal(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    user = update.effective_user
    context.user_data["revenue_goal"] = text
    logger.info(f"User {user.id} entered revenue goal: {text}")
    try:
        project_data = {
            "user_id": user.id,
            "username": user.username,
            "project_name": context.user_data["project_name"],
            "stage": context.user_data["stage"],
            "revenue_goal": text
        }
        response = supabase.table("projects").insert(project_data).execute()
        project = response.data[0]
        context.user_data["project_id"] = project['id']
        await store_conversation(
            user_id=user.id,
            project_id=project['id'],
            message=f"My project is {project['project_name']} (Stage: {project['stage']}) with revenue goal: {project['revenue_goal']}",
            role="user"
        )
        ai_prompt = "The user has just provided their project details. Please provide an initial assessment and ask 2-3 relevant questions based on the project stage."
        ai_response = await get_ai_response([], ai_prompt, project)
        await store_conversation(
            user_id=user.id,
            project_id=project['id'],
            message=ai_response,
            role="assistant"
        )
        await update.message.reply_text(ai_response)
    except Exception as e:
        logger.error(f"Error saving project: {e}")
        await update.message.reply_text(
            "There was an error saving your project. Please try again with /start."
        )
    return FEEDBACK

async def handle_feedback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.effective_user
    text = update.message.text
    project = await get_project_by_user_id(user.id)
    if not project:
        await update.message.reply_text(
            "I can't find your project data. Please start over with /start."
        )
        return ConversationHandler.END
    conversation_history = await get_conversation_history(user.id)
    await store_conversation(
        user_id=user.id,
        project_id=project['id'],
        message=text,
        role="user"
    )
    ai_response = await get_ai_response(conversation_history, text, project)
    await store_conversation(
        user_id=user.id,
        project_id=project['id'],
        message=ai_response,
        role="assistant"
    )
    await update.message.reply_text(ai_response)
    return FEEDBACK

async def review(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    project = await get_project_by_user_id(user.id)
    if project:
        message = (
            f"Here's your project:\n"
            f"- Name: {project['project_name']}\n"
            f"- Stage: {project['stage']}\n"
            f"- Revenue Goal: {project['revenue_goal']}\n\n"
            f"Need to refine it? Type /start or ask away!"
        )
    else:
        message = "You don't have a project yet. Start with /start to create one!"
    await update.message.reply_text(message)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_text = (
        "I'm Jeff Jr, your AI VC coach! Here's how to use me:\n\n"
        "/start - Begin creating or updating your project\n"
        "/review - View your current project details\n"
        "/help - Show this help message\n\n"
        "After starting, just chat with me about your startup, and I'll give you "
        "honest, blunt feedback to help you refine your concept and business model. "
        "I'll remember your project details for our future conversations. 💰"
    )
    await update.message.reply_text(help_text)

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Operation cancelled. Use /start to begin again or /help for assistance."
    )
    return ConversationHandler.END

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error(f"Error: {context.error}")
    if update and isinstance(update, Update) and update.effective_chat:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="An error occurred. Please try again or use /start to restart."
        )

def main() -> None:
    """Start the bot."""
    application = Application.builder().token(os.environ["TELEGRAM_TOKEN"]).build()
    
    application.add_error_handler(error_handler)
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, project_name)],
            STAGE: [CallbackQueryHandler(project_stage)],
            REVENUE: [MessageHandler(filters.TEXT & ~filters.COMMAND, revenue_goal)],
            FEEDBACK: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_feedback)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    
    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("review", review))
    
    # Initialize the database during startup (synchronously)
    init_database()
    
    # Start the Bot
    application.run_polling()

if __name__ == "__main__":
    main()