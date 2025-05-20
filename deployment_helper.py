#!/usr/bin/env python3
"""
deployment_helper.py - A utility script to help with deployment to Railway or Render
"""

import os
import json
import subprocess
import argparse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_environment():
    """Check if all required environment variables are set"""
    required_vars = ["TELEGRAM_TOKEN", "GOOGLE_API_KEY", "SUPABASE_URL", "SUPABASE_KEY"]
    missing_vars = []
    
    for var in required_vars:
        if not os.environ.get(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"  - {var}")
        return False
    
    print("✅ All required environment variables are set")
    return True

def test_database_connection():
    """Test connection to Supabase database"""
    try:
        from supabase import create_client
        
        supabase_url = os.environ.get("SUPABASE_URL")
        supabase_key = os.environ.get("SUPABASE_KEY")
        
        # Try to connect
        supabase = create_client(supabase_url, supabase_key)
        
        # Simple test query
        response = supabase.table("projects").select("id", count="exact").limit(1).execute()
        
        print("✅ Successfully connected to Supabase")
        return True
    except Exception as e:
        print(f"❌ Failed to connect to Supabase: {e}")
        return False

def test_telegram_token():
    """Test if the Telegram token is valid"""
    try:
        import httpx
        
        token = os.environ.get("TELEGRAM_TOKEN")
        url = f"https://api.telegram.org/bot{token}/getMe"
        
        response = httpx.get(url, timeout=10.0)
        data = response.json()
        
        if data.get("ok"):
            bot_info = data.get("result", {})
            bot_name = bot_info.get("first_name", "Unknown")
            bot_username = bot_info.get("username", "Unknown")
            print(f"✅ Telegram token is valid for bot: {bot_name} (@{bot_username})")
            return True
        else:
            print(f"❌ Invalid Telegram token: {data.get('description', 'Unknown error')}")
            return False
    except Exception as e:
        print(f"❌ Failed to validate Telegram token: {e}")
        return False

def test_google_ai():
    """Test if the Google AI API key is valid"""
    try:
        import google.generativeai as genai
        
        api_key = os.environ.get("GOOGLE_API_KEY")
        genai.configure(api_key=api_key)
        
        # Simple test
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content("Say hello!")
        
        print("✅ Successfully connected to Google AI API")
        return True
    except Exception as e:
        print(f"❌ Failed to connect to Google AI API: {e}")
        return False

def generate_railway_toml():
    """Generate a railway.toml configuration file"""
    config = {
        "build": {
            "builder": "nixpacks",
            "buildCommand": "pip install -r requirements.txt"
        },
        "deploy": {
            "startCommand": "python bot.py",
            "healthcheckPath": "/",
            "healthcheckTimeout": 300,
            "restartPolicyType": "on-failure",
            "restartPolicyMaxRetries": 10
        }
    }
    
    with open("railway.toml", "w") as f:
        import toml
        toml.dump(config, f)
    
    print("✅ Generated railway.toml configuration file")

def check_dependencies():
    """Check if all required packages are installed"""
    try:
        # Run pip freeze and compare with requirements.txt
        pip_output = subprocess.check_output(["pip", "freeze"], universal_newlines=True)
        installed_packages = set(pip_output.strip().split("\n"))
        
        with open("requirements.txt", "r") as f:
            required_packages = set(f.read().strip().split("\n"))
        
        # Extract package names without versions for comparison
        installed_names = {pkg.split("==")[0].lower() for pkg in installed_packages}
        required_names = {pkg.split("==")[0].lower() for pkg in required_packages}
        
        missing = required_names - installed_names
        
        if missing:
            print("❌ Missing required packages:")
            for pkg in missing:
                print(f"  - {pkg}")
            return False
        
        print("✅ All required packages are installed")
        return True
    except Exception as e:
        print(f"❌ Failed to check dependencies: {e}")
        return False

def prepare_for_deployment(platform):
    """Run all checks and prepare for deployment"""
    print(f"\n🚀 Preparing for deployment to {platform}...\n")
    
    all_checks_passed = True
    
    # Run all checks
    if not check_environment():
        all_checks_passed = False
    
    if not check_dependencies():
        all_checks_passed = False
    
    if not test_database_connection():
        all_checks_passed = False
    
    if not test_telegram_token():
        all_checks_passed = False
    
    if not test_google_ai():
        all_checks_passed = False
    
    # Generate platform-specific files
    if platform.lower() == "railway":
        generate_railway_toml()
    
    # Final summary
    print("\n" + "="*50)
    if all_checks_passed:
        print("✅ All checks passed! Ready for deployment.")
        print(f"\nNext steps for {platform} deployment:")
        
        if platform.lower() == "railway":
            print("1. Push your code to GitHub")
            print("2. Create a new project on Railway")
            print("3. Link your GitHub repository")
            print("4. Add environment variables")
            print("5. Deploy your application")
        elif platform.lower() == "render":
            print("1. Push your code to GitHub")
            print("2. Create a new Web Service on Render")
            print("3. Connect your GitHub repository")
            print("4. Set the build command: pip install -r requirements.txt")
            print("5. Set the start command: python bot.py")
            print("6. Add environment variables")
            print("7. Deploy your application")
    else:
        print("❌ Some checks failed. Please fix the issues before deploying.")
    
    print("="*50)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Helper script for deploying Jeff Jr")
    parser.add_argument("platform", choices=["railway", "render"], help="The platform to deploy to")
    args = parser.parse_args()
    
    prepare_for_deployment(args.platform)