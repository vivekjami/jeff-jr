#!/usr/bin/env python3
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

# Constants for conversation states
NAME, STAGE, REVENUE, FEEDBACK = range(4)

# Project stages
STAGES = ["Idea", "Development", "Launched"]

# Configure Supabase
supabase_url = os.environ.get("SUPABASE_URL", "https://kztlfophuvrndahhtojs.supabase.co")
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
        "max_output_tokens": 1024,
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


async def init_database() -> None:
    """Initialize the database with required tables."""
    try:
        # Check if the 'projects' table exists, if not create it
        supabase.table("projects").select("id", count="exact").limit(1).execute()
        logger.info("Projects table exists")
    except Exception as e:
        logger.info(f"Creating projects table: {e}")
        # Create the projects table
        supabase.postgrest.schema("public").execute_sql(
            """
            CREATE TABLE IF NOT EXISTS projects (
                id SERIAL PRIMARY KEY,
                user_id BIGINT NOT NULL,
                username TEXT,
                project_name TEXT NOT NULL,
                stage TEXT NOT NULL,
                revenue_goal TEXT NOT NULL,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            );
            """
        )
        
        # Create conversations table for chat history
        supabase.postgrest.schema("public").execute_sql(
            """
            CREATE TABLE IF NOT EXISTS conversations (
                id SERIAL PRIMARY KEY,
                user_id BIGINT NOT NULL,
                project_id INTEGER REFERENCES projects(id),
                message TEXT NOT NULL,
                role TEXT NOT NULL,
                timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            );
            """
        )


async def get_ai_response(conversation_history: List[Dict[str, str]], 
                          user_message: str, 
                          project_info: Optional[Dict[str, Any]] = None) -> str:
    """Generate AI response using Google's Gemini model."""
    try:
        # Prepare system prompt with Jeff Jr's persona
        system_prompt = """
        You are Jeff Jr, a no-nonsense venture capitalist Telegram bot. Your personality traits:
        
        1. Blunt but professional: You give direct, honest feedback without sugar-coating, but always remain professional.
        2. Time-conscious: You value efficiency and directness in communication.
        3. Expertise in startups: You have strong knowledge about MVPs, revenue models, market fit, and funding.
        4. Critical thinker: You ask tough questions to help founders refine their ideas.
        5. Blockchain savvy: You have particular expertise in crypto/blockchain projects.
        
        Your responses should:
        - Be brief and to the point (max 3-4 sentences)
        - Ask probing questions about business models, revenue plans, and market fit
        - Challenge weak ideas firmly but constructively
        - Use occasional emojis for emphasis (max 1-2 per message)
        - Focus on practical, actionable advice
        - Never be rude, but don't hold back honest critique
        
        Remember your goal is to help founders build viable businesses, not to make them feel good.
        """
        
        # Build conversation history
        chat = [{"role": "system", "content": system_prompt}]
        
        # Add project context if available
        if project_info:
            project_context = f"""
            Current project information:
            - Name: {project_info.get('project_name', 'Unknown')}
            - Stage: {project_info.get('stage', 'Unknown')}
            - Revenue Goal: {project_info.get('revenue_goal', 'Unknown')}
            
            Tailor your feedback to this specific project stage and goals.
            """
            chat.append({"role": "system", "content": project_context})
        
        # Add conversation history
        for message in conversation_history:
            chat.append(message)
        
        # Add the current user message
        chat.append({"role": "user", "content": user_message})
        
        # Generate response
        response = model.generate_content([msg["content"] for msg in chat])
        return response.text
    
    except Exception as e:
        logger.error(f"Error generating AI response: {e}")
        return "Sorry, I'm having trouble connecting to my brain right now. Try again in a moment. 🤔"


async def store_conversation(user_id: int, project_id: int, message: str, role: str) -> None:
    """Store conversation in the database."""
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
    """Get the latest project for a user."""
    try:
        response = supabase.table("projects").select("*").eq("user_id", user_id).order("created_at", desc=True).limit(1).execute()
        
        if response.data and len(response.data) > 0:
            return response.data[0]
        return None
    except Exception as e:
        logger.error(f"Error getting project: {e}")
        return None


async def get_conversation_history(user_id: int, limit: int = 10) -> List[Dict[str, str]]:
    """Get recent conversation history for a user."""
    try:
        response = supabase.table("conversations").select("*").eq("user_id", user_id).order("timestamp", desc=True).limit(limit).execute()
        
        conversation = []
        if response.data:
            # Convert to the format expected by the AI model
            for msg in reversed(response.data):
                conversation.append({"role": msg['role'], "content": msg['message']})
        return conversation
    except Exception as e:
        logger.error(f"Error getting conversation history: {e}")
        return []


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start conversation with the user and ask for project name."""
    user = update.effective_user
    logger.info(f"User {user.id} ({user.username}) started the bot")
    
    await update.message.reply_text(
        f"Welcome to Jeff Jr, your AI VC coach! 😎\nWhat's your project name? Be clear!"
    )
    
    return NAME


async def project_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Store project name and ask for project stage."""
    text = update.message.text
    user = update.effective_user
    
    # Store in context
    context.user_data["project_name"] = text
    
    logger.info(f"User {user.id} entered project name: {text}")
    
    # Create inline keyboard for project stages
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
    """Store project stage and ask for revenue goals."""
    query = update.callback_query
    user = query.from_user
    
    # Get selected stage from callback data
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
    """Store revenue goal and save the project to the database."""
    text = update.message.text
    user = update.effective_user
    
    # Store in context
    context.user_data["revenue_goal"] = text
    
    logger.info(f"User {user.id} entered revenue goal: {text}")
    
    # Save to database
    try:
        project_data = {
            "user_id": user.id, 
            "username": user.username,
            "project_name": context.user_data["project_name"],
            "stage": context.user_data["stage"],
            "revenue_goal": text
        }
        
        response = supabase.table("projects").insert(project_data).execute()
        project_id = response.data[0]['id']
        
        # Store the project ID in context for conversation tracking
        context.user_data["project_id"] = project_id
        
        # Store this initial conversation
        await store_conversation(
            user_id=user.id,
            project_id=project_id,
            message=f"My project is {context.user_data['project_name']} (Stage: {context.user_data['stage']}) with revenue goal: {text}",
            role="user"
        )
        
        # Get AI feedback based on the project details
        ai_prompt = f"""
        The user just told me about their project:
        - Name: {context.user_data['project_name']}
        - Stage: {context.user_data['stage']}
        - Revenue Goal: {text}
        
        Provide a brief initial assessment and ask 2-3 probing questions about their business model or strategy.
        """
        
        ai_response = await get_ai_response([], ai_prompt)
        
        # Store the AI response
        await store_conversation(
            user_id=user.id,
            project_id=project_id,
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
    """Handle ongoing conversation with the user."""
    user = update.effective_user
    text = update.message.text
    
    # Get project information
    project = await get_project_by_user_id(user.id)
    if not project:
        await update.message.reply_text(
            "I can't find your project data. Please start over with /start."
        )
        return ConversationHandler.END
    
    # Get conversation history
    conversation_history = await get_conversation_history(user.id)
    
    # Store user message
    await store_conversation(
        user_id=user.id,
        project_id=project['id'],
        message=text,
        role="user"
    )
    
    # Get AI response
    ai_response = await get_ai_response(conversation_history, text, project)
    
    # Store AI response
    await store_conversation(
        user_id=user.id,
        project_id=project['id'],
        message=ai_response,
        role="assistant"
    )
    
    await update.message.reply_text(ai_response)
    
    return FEEDBACK


async def review(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Allow user to review their project details."""
    user = update.effective_user
    
    # Get project information
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
    """Send a message when the command /help is issued."""
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
    """Cancel and end the conversation."""
    await update.message.reply_text(
        "Operation cancelled. Use /start to begin again or /help for assistance."
    )
    return ConversationHandler.END


def main() -> None:
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(os.environ["TELEGRAM_TOKEN"]).build()
    
    # Initialize database
    application.create_task(init_database())
    
    # Add conversation handler for project setup
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
    
    # Add command handlers
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("review", review))
    
    # Start the Bot
    application.run_polling()


if __name__ == "__main__":
    main()