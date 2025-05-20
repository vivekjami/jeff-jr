# Jeff Jr: AI Venture Capitalist Telegram Bot 🚀

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg) ![Telegram](https://img.shields.io/badge/Telegram-Bot_API-brightgreen.svg) ![SQLite](https://img.shields.io/badge/SQLite-Database-blue.svg) ![Hugging Face](https://img.shields.io/badge/Hugging_Face-AI-orange.svg) ![Railway](https://img.shields.io/badge/Railway-Deployed-purple.svg) ![Render](https://img.shields.io/badge/Render-Alternative-blue.svg)

**Jeff Jr** is a Telegram bot that acts as a no-nonsense venture capitalist, guiding startup founders to refine their MVPs and revenue plans with blunt, constructive feedback. Built in just 15 hours, it demonstrates proficiency in Python, API integration, database management, and cloud deployment on free-tier platforms. Jeff Jr remembers user projects, asks tough questions, and provides actionable advice to stand out in the startup ecosystem.

## 🎯 Project Goals
- **Mentor Developers**: Helps users build market-ready MVPs with direct, no-sugarcoating feedback.
- **Persistent Memory**: Stores user profiles and project details using SQLite or Supabase Postgres.
- **Unique Persona**: Delivers blunt yet professional critiques, informed by blockchain expertise.
- **Scalable Design**: Supports ~30 concurrent users on free-tier Railway or Render.
- **Portfolio Showcase**: Highlights skills in Python, bot development, and AI integration.

## ✨ Features
- **Interactive Q&A**: Engages users via Telegram with probing questions (e.g., "What's your revenue model? Be specific!").
- **Blunt Yet Polite Tone**: Challenges ideas firmly but professionally (e.g., "Your plan needs clarity. What's your edge?").
- **Project Memory**: Saves project details (name, stage, revenue goals) in a database.
- **AI-Powered Responses**: Uses Hugging Face’s free Inference API for context-aware replies.
- **Review Command**: View saved project details with `/review`.
- **Cloud Deployment**: Runs 24/7 on Railway or Render’s free tier.

## 🛠️ Tech Stack
- **Python 3.9+**: Core programming language.
- **python-telegram-bot**: Asynchronous library for Telegram Bot API.
- **SQLite/Supabase Postgres**: Persistent storage for user and project data.
- **Hugging Face Inference API**: Free-tier conversational AI.
- **Railway/Render**: Free-tier hosting for continuous operation.
- **dotenv**: Secure management of API keys.

## 🚀 Getting Started

### Prerequisites
- Python 3.9+ installed.
- Telegram bot token from [BotFather](https://telegram.me/BotFather).
- Hugging Face API key from [Hugging Face](https://huggingface.co/).
- (Optional) Supabase account for Postgres database.

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
   - Create a `.env` file:
     ```bash
     echo -e "TELEGRAM_TOKEN=your_telegram_bot_token\nHF_API_KEY=your_hugging_face_api_key\nDATABASE_URL=sqlite:///projects.db" > .env
     ```
   - Replace `your_telegram_bot_token` with your @JeffJrBot token.
   - Replace `your_hugging_face_api_key` with your Hugging Face API key.
   - For Supabase Postgres, update `DATABASE_URL` with the provided connection string.

4. **Initialize the Database**:
   - SQLite auto-creates `projects.db` on first run.
   - For Supabase, configure the Postgres connection (see deployment steps).

5. **Run Locally**:
   ```bash
   python bot.py
   ```
   Find `@JeffJrBot` on Telegram and start with `/start`.

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
**User**: Idea  
**Jeff Jr**: An idea-stage crypto wallet? Noted. What's your revenue goal? Be specific or I’ll assume you’re not serious!  
**User**: $10K/month via transaction fees  
**Jeff Jr**: Saved. A crypto wallet with transaction fees? Let’s dig in:  
- What’s your unique edge over MetaMask?  
- Have you audited your smart contracts?  
- How will you attract your first 100 users?  
**User**: `/review`  
**Jeff Jr**: Here's your project:  
- Name: CryptoWallet  
- Stage: Idea  
- Revenue Goal: $10K/month via transaction fees  
Need to refine it? Type `/start` or ask away!

## � Προ Deployment
Deploy Jeff Jr on **Railway** or **Render** for 24/7 operation:
1. **Push to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/vivek-jami/jeff-jr.git
   git push origin main
   ```
2. **Railway Deployment**:
   - Sign up at [Railway](https://railway.app/).
   - Create a new project, link your GitHub repo, and select the `jeff-jr` repository.
   - Set environment variables: `TELEGRAM_TOKEN`, `HF_API_KEY`, `DATABASE_URL` (use `sqlite:///projects.db` or Supabase Postgres URL).
   - Set start command: `python bot.py`.
   - Deploy and check logs.

3. **Render Deployment** (Alternative):
   - Sign up at [Render](https://render.com/).
   - Create a new Web Service, connect your GitHub repo, and select Python runtime.
   - Set start command: `python bot.py`.
   - Add environment variables: `TELEGRAM_TOKEN`, `HF_API_KEY`, `DATABASE_URL`.
   - Note: Render’s filesystem is ephemeral; use Supabase Postgres for persistence.
   - Deploy and monitor logs.

## 🏆 Developer Skills Showcased
- **Python Programming**: Clean, asynchronous bot logic with `python-telegram-bot`.
- **AI Integration**: Prompt engineering with Hugging Face for a unique VC persona.
- **Database Management**: SQLite/Supabase Postgres for persistent storage.
- **Cloud Deployment**: Railway/Render setup with environment variables.
- **Blockchain Context**: Informed by Solidity and Solana experience for crypto-related advice.

## 🔍 Challenges and Learnings
- **Challenge**: Building a bot required rapid prioritization as this is relatively new to me.
- **Solution**: Leveraged `python-telegram-bot` and SQLite for simplicity, with Supabase as a backup.
- **Learning**: Mastered Telegram Bot API, async programming, and cloud deployment.

## 👨‍💻 About the Developer
Vivek Jami is a software engineer with expertise in Python, JavaScript, Solidity, and full-stack development. With hackathon wins (e.g., RollAppOraft, Solana Hackathon) and projects like SolStripe, I excel at building innovative solutions. Connect on [LinkedIn](https://linkedin.com/in/vivek-jami) or [GitHub](https://github.com/vivek-jami).

## 📬 Contact
Reach out at j.vivekvams@gmail.com or open a GitHub issue for feedback or collaboration.

---

⭐ **Star this repo** if Jeff Jr helped you refine your MVP!  
💼 **Hiring?** This project showcases my ability to deliver under tight deadlines. Let’s talk!