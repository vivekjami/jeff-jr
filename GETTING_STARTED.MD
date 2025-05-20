# Getting Started with Jeff Jr

This guide provides step-by-step instructions to set up and deploy your Jeff Jr AI Venture Capitalist Telegram bot.

## Prerequisites

Before you begin, make sure you have:

1. **Python 3.9+** installed on your system
2. A **Telegram account** to create and test your bot
3. A **Google AI API key** for the Gemini model
4. Your **Supabase** project details (URL and service key)

## Step 1: Create a Telegram Bot

1. Open Telegram and search for **@BotFather**
2. Start a chat and send the command `/newbot`
3. Follow the prompts to name your bot and set its username
4. **Save the API token** provided by BotFather - you'll need this later

## Step 2: Set Up Your Local Environment

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/jeff-jr.git
   cd jeff-jr
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Step 3: Configure Environment Variables

1. **Open the `.env` file** and update with your credentials:
   ```
   # Replace with your actual tokens and keys
   TELEGRAM_TOKEN="your_telegram_bot_token"
   GOOGLE_API_KEY="your_google_api_key"
   SUPABASE_URL="https://kztlfophuvrndahhtojs.supabase.co"
   SUPABASE_KEY="your_supabase_service_key"
   ```

2. **Save the file** with your changes

## Step 4: Initialize the Database

1. **Run the database setup script**
   ```bash
   python setup_db.py
   ```

2. **Verify the output** shows successful table creation

## Step 5: Test the AI Integration

1. **Test the AI model** to ensure your Google AI key is working:
   ```bash
   python test_ai.py "I'm building a new fintech app for small businesses"
   ```

2. **Check the response** - you should see Jeff Jr's reply to your prompt

## Step 6: Run the Bot Locally

1. **Start the bot**
   ```bash
   python bot.py
   ```

2. **Open Telegram** and find your bot by its username
3. **Start a conversation** with the `/start` command
4. **Test the full interaction flow** by adding a project

## Step 7: Deploy to Production

### Option 1: Railway Deployment

1. **Create a Railway account** at [railway.app](https://railway.app)
2. **Create a new project** in Railway
3. **Connect your GitHub repository**
4. **Add environment variables** from your `.env` file
5. **Deploy the application**

### Option 2: Render Deployment

1. **Create a Render account** at [render.com](https://render.com)
2. **Create a new Web Service**
3. **Connect your GitHub repository**
4. **Configure build settings**:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python bot.py`
5. **Add environment variables** from your `.env` file
6. **Deploy the application**

## Step 8: Verify Production Deployment

1. **Check deployment logs** for any errors
2. **Test your bot on Telegram** to ensure it's responding correctly
3. **Monitor the application** for any issues

## Troubleshooting

### Common Issues

1. **Bot Not Responding**
   - Check deployment logs
   - Verify your Telegram token is correct
   - Ensure the bot is running

2. **Database Connection Issues**
   - Verify your Supabase URL and key
   - Check network connectivity
   - Run `setup_db.py` to ensure tables exist

3. **AI Not Working**
   - Verify your Google AI API key
   - Check usage limits
   - Test with `test_ai.py` to isolate the issue

### Getting Help

If you encounter issues not covered here, try:
- Checking the logs for specific error messages
- Reviewing the [python-telegram-bot documentation](https://python-telegram-bot.readthedocs.io/)
- Opening an issue on the project GitHub repository

## Next Steps

After successfully deploying Jeff Jr, consider:
- Customizing the AI prompts to refine the bot's personality
- Adding more detailed analytics for user interactions
- Implementing additional commands for specific startup advice
- Creating a feedback mechanism to improve responses over time

Happy building! 🚀