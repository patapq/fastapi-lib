import os
from dotenv import load_dotenv

from supabase import create_client, Client


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

supabase: Client = create_client(url, key)


def find_all_books():
    data = supabase.table("books").select("*").execute()
    # Equivalent for SQL Query "SELECT * FROM;"
    if data:
        return data
    else:
        return 'No records found'



def full_text_search(prompt):
    result = supabase.rpc("my_test", params={'prompt': prompt}).execute()
    return result


def get_books_by_type(prompt):
    result = supabase.rpc("get_books_by_type", params={'type': prompt}).execute()
    return result


def get_books_by_author(prompt):
    result = supabase.rpc("get_books_by_author_name", params={'name': prompt}).execute()
    return result


def get_books_by_category(prompt):
    result = supabase.rpc("get_books_by_category_name", params={'name': prompt}).execute()
    return result