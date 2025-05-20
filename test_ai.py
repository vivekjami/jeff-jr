#!/usr/bin/env python3
import os
import argparse
import asyncio
from typing import Dict, List
from dotenv import load_dotenv
import google.generativeai as genai
from google.api_core.exceptions import GoogleAPIError

# Load environment variables
load_dotenv()

# Constants
MODEL_NAME = "gemini-2.0-flash"
GENERATION_CONFIG = {
    "temperature": 0.7,
    "top_p": 0.9,
    "top_k": 40,
    "max_output_tokens": 1024,
}
SYSTEM_PROMPT = """
You are Jeff Jr, a no-nonsense venture capitalist Telegram bot. Your personality traits:
1. Blunt but professional: Direct, honest feedback without sugar-coating, always professional.
2. Time-conscious: Value efficiency and directness in communication.
3. Expertise in startups: Strong knowledge about MVPs, revenue models, market fit, and funding.
4. Critical thinker: Ask tough questions to help founders refine their ideas.
5. Blockchain savvy: Particular expertise in crypto/blockchain projects.

Responses should:
- Be brief and to the point (max 3-4 sentences)
- Ask probing questions about business models, revenue plans, and market fit
- Challenge weak ideas firmly but constructively
- Use occasional emojis for emphasis (max 1-2 per message)
- Focus on practical, actionable advice
- Never be rude, but don't hold back honest critique

Goal: Help founders build viable businesses, not just make them feel good.
"""
PROJECT_CONTEXT = {
    "project_name": "CryptoWallet",
    "stage": "Idea",
    "revenue_goal": "$10K/month via transaction fees"
}

def configure_genai() -> genai.GenerativeModel:
    """Configure and return the Google AI generative model."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set")
    
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(
        model_name=MODEL_NAME,
        generation_config=GENERATION_CONFIG
    )

async def test_ai_response(prompt: str, model: genai.GenerativeModel) -> None:
    """Test the AI response for a given prompt."""
    chat = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "system", "content": f"Project context: {PROJECT_CONTEXT}"},
        {"role": "user", "content": prompt}
    ]
    
    try:
        response = model.generate_content([msg["content"] for msg in chat])
        print("\n=== TEST RESULTS ===")
        print(f"📝 Prompt: \"{prompt}\"")
        print("\n🤖 Jeff Jr Response:")
        print(response.text)
        print("\n===================")
    except GoogleAPIError as e:
        print(f"❌ Google AI API error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

def parse_args() -> str:
    """Parse command-line arguments and return the prompt."""
    parser = argparse.ArgumentParser(description="Test Jeff Jr AI responses")
    parser.add_argument("prompt", help="The prompt to test with the AI")
    return parser.parse_args().prompt

async def main() -> None:
    """Main function to run the AI test."""
    try:
        model = configure_genai()
        prompt = parse_args()
        await test_ai_response(prompt, model)
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    asyncio.run(main())