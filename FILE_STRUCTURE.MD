# Project File Structure

```
jeff-jr/
├── .env                       # Environment variables configuration
├── bot.py                     # Main bot application
├── deployment_helper.py       # Deployment preparation utility
├── Dockerfile                 # Docker configuration for containerization
├── GETTING_STARTED.md         # Detailed setup and deployment guide
├── Procfile                   # Process file for Railway/Heroku deployment
├── PROJECT_OVERVIEW.md        # Technical architecture and design details
├── README.md                  # Project overview and documentation
├── requirements.txt           # Python package dependencies
├── setup_db.py               # Database initialization script
└── test_ai.py                # Utility to test AI responses
```

## File Purposes

- **bot.py**: Core application that handles Telegram interactions, database operations, and AI integration
- **.env**: Stores sensitive configuration like API keys and database credentials
- **deployment_helper.py**: Script to verify all requirements are met before deployment
- **Dockerfile**: Enables containerized deployment
- **GETTING_STARTED.md**: Step-by-step instructions for setting up the project
- **Procfile**: Specifies the command to run the application on cloud platforms
- **PROJECT_OVERVIEW.md**: Describes the technical architecture and implementation details
- **README.md**: Main project documentation with features, setup instructions, and usage
- **requirements.txt**: Lists all Python package dependencies
- **setup_db.py**: Script to initialize the database tables in Supabase
- **test_ai.py**: Utility to test the Google AI integration in isolation

## Key Relationships

- **bot.py** uses configuration from **.env**
- **bot.py** depends on tables created by **setup_db.py**
- **deployment_helper.py** checks all components before deployment
- **test_ai.py** verifies the AI integration works correctly

All these files work together to create a complete, production-ready Telegram bot with AI capabilities and persistent data storage.