#!/usr/bin/env python3
import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

# Configure Supabase
supabase_url = os.environ.get("SUPABASE_URL", "https://kztlfophuvrndahhtojs.supabase.co")
supabase_key = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

def init_database():
    """Initialize the database with required tables."""
    try:
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
        print("✅ Projects table created or already exists")
        
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
        print("✅ Conversations table created or already exists")
        
        # Optional: Create indexes for better query performance
        supabase.postgrest.schema("public").execute_sql(
            """
            CREATE INDEX IF NOT EXISTS idx_projects_user_id ON projects(user_id);
            CREATE INDEX IF NOT EXISTS idx_conversations_user_id ON conversations(user_id);
            CREATE INDEX IF NOT EXISTS idx_conversations_project_id ON conversations(project_id);
            """
        )
        print("✅ Indexes created")
        
        return True
    except Exception as e:
        print(f"❌ Error setting up database: {e}")
        return False

if __name__ == "__main__":
    print("🔄 Initializing database tables...")
    if init_database():
        print("✅ Database setup complete!")
    else:
        print("❌ Database setup failed.")