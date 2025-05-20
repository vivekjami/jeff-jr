# Jeff Jr: AI Venture Capitalist Telegram Bot 🚀

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg) ![Telegram](https://img.shields.io/badge/Telegram-Bot_API-brightgreen.svg) ![SQLite](https://img.shields.io/badge/SQLite-Database-blue.svg) ![Hugging Face](https://img.shields.io/badge/Hugging_Face-AI-orange.svg) ![Heroku](https://img.shields.io/badge/Heroku-Deployed-purple.svg)

**Jeff Jr** is a Telegram bot that plays the role of a no-nonsense venture capitalist, pushing startup founders to refine their MVPs and revenue plans with blunt, constructive feedback. Built in just 8 hours, it showcases expertise in Python, API integration, database management, and cloud deployment. Jeff Jr remembers users' projects, asks tough questions, and provides actionable advice to stand out in the competitive startup landscape.

## 🎯 Project Goals
- **Mentor Developers**: Guides users to build market-ready MVPs with direct, no-sugarcoating feedback.
- **Persistent Memory**: Tracks user profiles and project details across sessions using SQLite or PostgreSQL.
- **Unique Persona**: Combines blunt, analytical critiques with polite, professional responses.
- **Scalable Design**: Supports ~30 concurrent users on free-tier infrastructure.
- **Portfolio Showcase**: Demonstrates skills in Python, bot development, and AI integration.

## ✨ Features
- **Interactive Q&A**: Engages users via Telegram with probing questions (e.g., "What's your revenue model? Be specific!").
- **Blunt Yet Polite Tone**: Challenges ideas firmly but professionally (e.g., "Your idea needs work. What's your unique edge?").
- **Project Memory**: Stores user profiles and project details (name, stage, revenue goals) in a database.
- **AI-Powered Responses**: Leverages Hugging Face’s free Inference API for intelligent, context-aware replies.
- **Review Command**: Allows users to review saved project details with `/review`.
- **Cloud Deployment**: Runs 24/7 on Heroku’s free tier, accessible globally.

## 🛠️ Tech Stack
- **Python 3.9+**: Core programming language for bot logic.
- **python-telegram-bot**: Asynchronous library for Telegram Bot API integration.
- **SQLite/Heroku Postgres**: Stores user and project data for persistent memory.
- **Hugging Face Inference API**: Free-tier conversational AI for dynamic responses.
- **Heroku**: Free-tier hosting for continuous operation.
- **dotenv**: Secure management of API keys and environment variables.

## 🚀 Getting Started

### Prerequisites
- Python 3.9+ installed.
- Telegram account and bot token from [BotFather](https://telegram.me/BotFather).
- Hugging Face account and API key from [Hugging Face](https://huggingface.co/).

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
   - Create a `.env` file in the project root:
     ```bash
     TELEGRAM_TOKEN=your_telegram_bot_token
     HF_API_KEY=your_hugging_face_api_key
     ```
   - Replace `your_telegram_bot_token` with the token from BotFather.
   - Replace `your_hugging_face_api_key` with your Hugging Face API key.

4. **Initialize the Database**:
   - The bot auto-creates an SQLite database (`projects.db`) on first run.
   - For Heroku deployment, use Heroku Postgres (see deployment steps).

5. **Run Locally**:
   ```bash
   python bot.py
   ```
   Search for `@JeffJrBot` on Telegram and start with `/start`.

## 🌟 Usage
- **Start Interaction**: Use `/start` to begin describing your project.
- **Provide Details**: Answer prompts about your project name, stage, and revenue goals.
- **Review Projects**: Use `/review` to view saved project details.
- **Get Feedback**: Receive blunt, constructive advice to refine your MVP (e.g., "Your revenue plan is weak. How will you scale?").

### Example Interaction
**User**: `/start`  
**Jeff Jr**: Welcome to Jeff Jr, your AI VC coach! 😎 What's your project name? Be clear!  
**User**: My project is a fitness app for seniors.  
**Jeff Jr**: A fitness app for seniors? Interesting, but I need specifics:  
1. Who exactly is your target audience?  
2. Why will they choose you over Fitbit?  
3. What's your revenue model? Don't be vague!  

**User**: `/review`  
**Jeff Jr**: Here's your project:  
- Name: SeniorFit  
- Stage: Idea  
- Revenue Goal: Subscription-based, $10/month  
Need to discuss next steps? Type `/start` or ask away!

## ☁️ Deployment
To run Jeff Jr 24/7, deploy to Heroku:
1. **Create a Heroku App**:
   ```bash
   heroku create jeff-jr-bot
   heroku addons:create heroku-postgresql:hobby-dev
   ```
2. **Push Code**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git push heroku main
   ```
3. **Set Environment Variables**:
   ```bash
   heroku config:set TELEGRAM_TOKEN=your_token HF_API_KEY=your_key
   ```
4. **Scale the App**:
   ```bash
   heroku ps:scale web=1
   ```

## 🏆 Developer Skills Showcased
- **Python Programming**: Clean, asynchronous bot logic with `python-telegram-bot`.
- **AI Integration**: Prompt engineering with Hugging Face’s Inference API for unique VC persona.
- **Database Management**: SQLite/PostgreSQL for persistent user and project data.
- **Cloud Deployment**: Heroku setup with environment variables and database integration.
- **Blockchain Context**: Leverages my Solidity and Solana experience to inform crypto-related advice.

## 🔍 Challenges and Learnings
- **Challenge**: Building a functional bot in 8 hours required rapid prioritization.
- **Solution**: Focused on core features (conversation flow, database) and used free-tier tools.
- **Learning**: Mastered Telegram Bot API, async programming, and AI prompt design.

## 👨‍💻 About the Developer
Vivek Jami is a passionate software engineer with expertise in Python, JavaScript, Solidity, and full-stack development. With a track record of winning hackathons (e.g., RollAppOraft, Solana Hackathon) and building decentralized apps like SolStripe, I thrive on solving complex problems. Connect with me on [LinkedIn](https://linkedin.com/in/vivek-jami) or [GitHub](https://github.com/vivek-jami).

## 📬 Contact
For feedback or collaboration, reach out at j.vivekvams@gmail.com or open an issue on GitHub.

---

⭐ **Star this repo** if Jeff Jr helped you refine your MVP!  
💼 **Hiring?** This project showcases my ability to deliver under tight deadlines. Let’s talk!