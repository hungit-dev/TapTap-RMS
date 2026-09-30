from pathlib import Path
import firebase_admin
from firebase_admin import credentials

BASE_DIR = Path(__file__).resolve().parent.parent
cred = credentials.Certificate(
    BASE_DIR / "firebase-service-account.json"
)
firebase_admin.initialize_app(cred)