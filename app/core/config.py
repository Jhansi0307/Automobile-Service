import os
from datetime import timezone, datetime
from dotenv import load_dotenv

# --- LOAD .env FILE ---
# This ensures DATABASE_URL is loaded correctly
load_dotenv()

# --- READ ENVIRONMENT VARIABLES ---
DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY", "replace_with_secure_random")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

# --- CONSTANTS ---
ALLOWED_STATUSES = {"Pending", "In-Progress", "Completed"}
ALLOWED_CURRENCIES = {"INR", "USD", "EUR"}

def now_date():
    return datetime.now(timezone.utc).date()
