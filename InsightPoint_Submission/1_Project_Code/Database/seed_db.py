import os
import json
from pymongo import MongoClient

def get_mongodb_connection():
    # Attempt to read from env or fallback to local
    mongodb_uri = "mongodb://localhost:27017/"
    db_name = "news_sentiment_intelligence_db"
    
    # Try to load env if available from different possible depths
    try:
        from dotenv import load_dotenv
        
        # Check standard depths - dev folder first
        base_dir = os.path.dirname(os.path.abspath(__file__))
        possible_envs = [
            os.path.join(base_dir, '..', '..', 'Backend', '.env'), # LAST_YEAR_PROJECT/Backend/.env (Atlas URI)
            os.path.join(base_dir, '..', 'Backend', '.env'), # 1_Project_Code/Backend/.env (Local fallback)
            os.path.join(base_dir, 'Backend', '.env'), # Parent sibling
        ]
        
        for env_path in possible_envs:
            if os.path.exists(env_path):
                load_dotenv(env_path)
                print(f"INFO: Loaded environment from {os.path.abspath(env_path)}")
                break
        
        mongodb_uri = os.getenv("MONGODB_URI", mongodb_uri)
        db_name = os.getenv("MONGODB_DB_NAME", db_name)
    except Exception as e:
        print(f"INFO: Env load fallback: {e}")
        
    return mongodb_uri, db_name

def seed():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    seed_json_path = os.path.join(base_dir, 'seed_data.json')
    
    if not os.path.exists(seed_json_path):
        print(f"ERROR: Seed file not found at {seed_json_path}")
        return
        
    print("--------------------------------------------------")
    print("INFO: InsightPoint Database Seeder Starting...")
    print("--------------------------------------------------")
    
    uri, db_name = get_mongodb_connection()
    # Mask username/password for logging
    masked_uri = uri
    if "@" in uri:
        parts = uri.split("@")
        prefix = parts[0].split("//")
        if len(prefix) > 1:
            masked_uri = f"{prefix[0]}//***:***@{parts[1]}"
            
    print(f"Connecting to MongoDB: {masked_uri}")
    print(f"Target Database: {db_name}")
    
    try:
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        db = client[db_name]
        
        # Test connection
        client.admin.command('ping')
        print("SUCCESS: MongoDB connection verified successfully!")
        
        # Load seed data
        with open(seed_json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # 1. Seed Users
        if 'users' in data:
            print("\nSeeding Users...")
            db.users.drop()  # Drop old entries
            users_list = data['users']
            result = db.users.insert_many(users_list)
            print(f"   Success: Seeded {len(result.inserted_ids)} users.")
            print("   Available Accounts:")
            for u in users_list:
                print(f"   - Username: '{u['username']}' | Role: '{u['role']}'")
                
        # 2. Seed News Dataset
        if 'news_dataset' in data:
            print("\nSeeding News Articles...")
            db.news_dataset.drop()
            articles_list = data['news_dataset']
            result = db.news_dataset.insert_many(articles_list)
            print(f"   Success: Seeded {len(result.inserted_ids)} news articles.")
            
        # 3. Seed Documents
        if 'documents' in data:
            print("\nSeeding Documents...")
            db.documents.drop()
            docs_list = data['documents']
            result = db.documents.insert_many(docs_list)
            print(f"   Success: Seeded {len(result.inserted_ids)} uploaded documents.")
            
        print("\n--------------------------------------------------")
        print("SUCCESS: Database seeding completed successfully!")
        print("--------------------------------------------------")
        
    except Exception as e:
        print(f"\nERROR: Database seeding failed: {e}")
        print("Please ensure MongoDB is running locally or check your MONGODB_URI in the .env file.")

if __name__ == '__main__':
    seed()
