# Jeff Jr: AI Venture Capitalist Telegram Bot 🚀

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg) ![Telegram](https://img.shields.io/badge/Telegram-Bot_API-brightgreen.svg) ![Supabase](https://img.shields.io/badge/Supabase-Database-blue.svg) ![Google AI](https://img.shields.io/badge/Google-Gemini_AI-orange.svg) ![Railway](https://img.shields.io/badge/Railway-Deployed-purple.svg) ![Render](https://img.shields.io/badge/Render-Alternative-blue.svg)

**Jeff Jr**  is a Telegram bot that acts as a no-nonsense venture capitalist, guiding startup founders to refine their MVPs and revenue plans with blunt, constructive feedback. Built in just less than 10 hours, it demonstrates proficiency in Python, API integration, database management, and cloud deployment on free-tier platforms. Jeff Jr remembers user projects, asks tough questions, and provides actionable advice to stand out in the startup ecosystem.

## 🎯 Project Goals
- **Mentor Developers**: Helps users build market-ready MVPs with direct, no-sugarcoating feedback.
- **Persistent Memory**: Stores user profiles and project details using Supabase Postgres.
- **Unique Persona**: Delivers blunt yet professional critiques, informed by blockchain expertise.
- **Scalable Design**: Supports concurrent users on free-tier Railway or Render.
- **Portfolio Showcase**: Highlights skills in Python, bot development, and AI integration.

## ✨ Features
- **Interactive Q&A**: Engages users via Telegram with probing questions (e.g., "What's your revenue model? Be specific!").
- **Blunt Yet Polite Tone**: Challenges ideas firmly but professionally (e.g., "Your plan needs clarity. What's your edge?").
- **Project Memory**: Saves project details (name, stage, revenue goals) in Supabase database.
- **AI-Powered Responses**: Uses Google's Gemini AI for context-aware replies.
- **Review Command**: View saved project details with `/review`.
- **Cloud Deployment**: Runs 24/7 on Railway or Render's free tier.

## 🛠️ Tech Stack
- **Python 3.9+**: Core programming language.
- **python-telegram-bot**: Asynchronous library for Telegram Bot API.
- **Supabase Postgres**: Persistent storage for user and project data.
- **Google Gemini AI**: State-of-the-art conversational AI.
- **Railway/Render**: Free-tier hosting for continuous operation.
- **dotenv**: Secure management of API keys.

## 🚀 Getting Started

### Prerequisites
- Python 3.9+ installed.
- Telegram bot token from [BotFather](https://telegram.me/BotFather).
- Google AI API key from [Google AI Studio](https://ai.google.dev/).
- Supabase account with a project (the URL and key are already provided in the .env template).

### Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/vivek-jami/jeff-jr
   cd jeff-jr
   ```
2. **Set Up Virtual Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. **Configure Environment Variables**:
   - Edit the `.env` file with your credentials:
     - Add your Google AI API key
     - Verify the Supabase URL and key

4. **Run Locally**:
   ```bash
   python bot.py
   ```
   Find your bot on Telegram using the handle you set up with BotFather and start with `/start`.

## 🌟 Usage
- **Start**: Use `/start` to describe your project.
- **Provide Details**: Answer prompts about project name, stage, and revenue goals.
- **Review**: Use `/review` to view saved project details.
- **Get Feedback**: Receive blunt, actionable advice (e.g., "Your revenue plan is weak. How will you scale?").

### Example Interaction
**User**: `/start`  
**Jeff Jr**: Welcome to Jeff Jr, your AI VC coach! 😎 What's your project name? Be clear!  
**User**: CryptoWallet  
**Jeff Jr**: CryptoWallet, huh? Alright:  
- What stage is it at? (Idea, Development, Launched)  
**User**: (Taps "Idea" button)  
**Jeff Jr**: An idea-stage crypto wallet? Noted. What's your revenue goal? Be specific or I'll assume you're not serious!  
**User**: $10K/month via transaction fees  
**Jeff Jr**: Saved. A crypto wallet with transaction fees? Let's dig in:  
- What's your unique edge over MetaMask?  
- Have you audited your smart contracts?  
- How will you attract your first 100 users?  
**User**: `/review`  
**Jeff Jr**: Here's your project:  
- Name: CryptoWallet  
- Stage: Idea  
- Revenue Goal: $10K/month via transaction fees  
Need to refine it? Type `/start` or ask away!

## 🚢 Deployment
Deploy Jeff Jr on **Railway** or **Render** for 24/7 operation:
1. **Push to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/jeff-jr.git
   git push origin main
   ```
2. **Railway Deployment**:
   - Sign up at [Railway](https://railway.app/).
   - Create a new project, link your GitHub repo, and select the `jeff-jr` repository.
   - Set environment variables from your `.env` file.
   - Set start command: `python bot.py`.
   - Deploy and check logs.

3. **Render Deployment** (Alternative):
   - Sign up at [Render](https://render.com/).
   - Create a new Web Service, connect your GitHub repo, and select Python runtime.
   - Set start command: `python bot.py`.
   - Add environment variables from your `.env` file.
   - Deploy and monitor logs.

## 🔍 Technical Details

### Database Schema
The application uses two main tables in Supabase:

1. **Projects Table**:
   - `id`: Serial primary key
   - `user_id`: Telegram user ID
   - `username`: Telegram username (optional)
   - `project_name`: Name of the startup project
   - `stage`: Current stage (Idea, Development, Launched)
   - `revenue_goal`: Financial targets and model
   - `created_at`: Timestamp of creation
   - `updated_at`: Timestamp of last update

2. **Conversations Table**:
   - `id`: Serial primary key
   - `user_id`: Telegram user ID
   - `project_id`: Foreign key to projects table
   - `message`: The actual message content
   - `role`: Either "user" or "assistant"
   - `timestamp`: When the message was sent

### AI Integration
The bot uses Google's Gemini Pro model, which provides:
- Context awareness through conversation history
- Project-specific insights based on stored data
- Natural, conversational responses with the Jeff Jr persona

## 📝 Future Enhancements
- **Analytics Dashboard**: Track user engagement and project progression.
- **Multi-Project Support**: Allow users to manage multiple startup ideas.
- **Expert Networks**: Connect founders with similar interests or complementary skills.
- **Investment Simulation**: Gamified investment scenarios to test business model resilience.

## 👨‍💻 About the Developer
Vivek Jami is a software engineer with expertise in Python, JavaScript, Solidity, and full-stack development. With hackathon wins (e.g., RollAppOraft, Solana Hackathon) and projects like SolStripe, I excel at building innovative solutions. Connect on [LinkedIn](https://linkedin.com/in/vivek-jami) or [GitHub](https://github.com/vivek-jami).

## 📬 Contact
Reach out at j.vivekvams@gmail.com or open a GitHub issue for feedback or collaboration.

---

⭐ **Star this repo** if Jeff Jr helped you refine your MVP!  
💼 **Hiring?** This project showcases my ability to deliver complete solutions. Let's talk!