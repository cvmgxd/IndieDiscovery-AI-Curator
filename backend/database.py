import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

class DatabaseManager:
    def __init__(self):
        url = os.environ.get("SUPABASE_URL")
        key = os.environ.get("SUPABASE_KEY")
        if url and key:
            self.supabase: Client = create_client(url, key)
        else:
            self.supabase = None
            print("Supabase credentials not found. Running in ephemeral mode.")

    def save_game(self, game_data: dict):
        if self.supabase:
            return self.supabase.table("games").insert(game_data).execute()
        return None

    def get_top_games(self, limit: int = 20):
        if self.supabase:
            return self.supabase.table("games").select("*").order("smart_score", desc=True).limit(limit).execute()
        return []

db = DatabaseManager()
