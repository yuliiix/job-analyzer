from supabase import create_client
import os
from dotenv import load_dotenv
from models import Application

load_dotenv()

supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))


def save_application(application: Application):
    result = (
        supabase.table("applications")
        .insert(
            {
                "company": application.company,
                "status": application.status,
                "match_score": application.match_score,
            }
        )
        .execute()
    )
    return result.data


def get_applications():
    result = supabase.table("applications").select("*").execute()
    return result.data


def update_status(id: int, status: str):
    result = (
        supabase.table("applications").update({"status": status}).eq("id", id).execute()
    )
    return result.data


def delete_application(id: int):
    result = supabase.table("applications").delete().eq("id", id).execute()
    return result.data
