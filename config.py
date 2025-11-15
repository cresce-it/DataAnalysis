import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv(
    "MONGODB_URI",
    "mongodb+srv://n8n:00XVDe1yOeWhBqAz@web.dxlnz.mongodb.net/main"
)

EXCLUDED_USER_IDS = [
    "68e7e7c09e5d01bd097bece9",
    "68e4fb9483ed084323c39240"
]

GLUE_WEBHOOK_URL = os.getenv("GLUE_WEBHOOK_URL", "")
GLUE_TARGET = os.getenv("GLUE_TARGET", "")

