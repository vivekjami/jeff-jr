#!/usr/bin/env python3
import os
import argparse
import asyncio
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Google AI
google_api_key = os.environ.get("GOOGLE_API_KEY")
genai.configure(api_key=google_api_key)
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config={
        "temperature": 0.7,
        "top_p": 0.9,
        "top_k": 40,
        "max_output_tokens": 1024,
    }
)

async def test_ai_response(prompt: str):
    """Test the AI response to a given prompt."""
    
    # Jeff Jr persona for testing
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
    
    try:
        # Create a mock project for testing
        example_project = {
            "project_name": "CryptoWallet",
            "stage": "Idea",
            "revenue_goal": "$10K/month via transaction fees"
        }
        
        # Build conversation
        chat = [
            {"role": "system", "content": system_prompt},
            {"role": "system", "content": f"Project context: {example_project}"},
            {"role": "user", "content": prompt}
        ]
        
        # Generate response
        response = model.generate_content([msg["content"] for msg in chat])
        
        # Display results
        print("\n=== TEST RESULTS ===")
        print(f"📝 Prompt: \"{prompt}\"")
        print("\n🤖 Jeff Jr Response:")
        print(response.text)
        print("\n===================")
        
    except Exception as e:
        print(f"❌ Error testing AI: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test the Jeff Jr AI responses")
    parser.add_argument("prompt", help="The prompt to test with the AI")
    args = parser.parse_args()
    
    asyncio.run(test_ai_response(args.prompt))