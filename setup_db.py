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

def check_tables_exist():
    """Check if required tables exist in the database."""
    try:
        # Try to query the tables to verify they exist
        projects_exist = True
        conversations_exist = True
        
        try:
            supabase.table("projects").select("id", count="exact").limit(1).execute()
            print("✅ Projects table exists")
        except Exception as e:
            projects_exist = False
            print(f"❌ Projects table does not exist: {e}")
        
        try:
            supabase.table("conversations").select("id", count="exact").limit(1).execute()
            print("✅ Conversations table exists")
        except Exception as e:
            conversations_exist = False
            print(f"❌ Conversations table does not exist: {e}")
        
        return projects_exist and conversations_exist
    
    except Exception as e:
        print(f"❌ Error checking tables: {e}")
        return False

def print_sql_instructions():
    """Print SQL instructions for manual table creation."""
    print("\n==== MANUAL SQL SETUP INSTRUCTIONS ====")
    print("To create the necessary tables, follow these steps:")
    print("1. Log in to your Supabase dashboard")
    print("2. Go to the SQL Editor")
    print("3. Run the following SQL:")
    print("""
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
    
    CREATE TABLE IF NOT EXISTS conversations (
        id SERIAL PRIMARY KEY,
        user_id BIGINT NOT NULL,
        project_id INTEGER REFERENCES projects(id),
        message TEXT NOT NULL,
        role TEXT NOT NULL,
        timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    );
    
    CREATE INDEX IF NOT EXISTS idx_projects_user_id ON projects(user_id);
    CREATE INDEX IF NOT EXISTS idx_conversations_user_id ON conversations(user_id);
    CREATE INDEX IF NOT EXISTS idx_conversations_project_id ON conversations(project_id);
    """)
    print("4. Run this script again to verify the tables exist")
    print("=====================================")

if __name__ == "__main__":
    print("🔄 Checking database tables...")
    
    if check_tables_exist():
        print("\n✅ All required tables exist. Database setup is complete!")
    else:
        print("\n❌ Some required tables are missing.")
        print_sql_instructions()