from pathlib import Path
from dotenv import load_dotenv
import os

BASE_DIR = Path(__file__).resolve().parents[1]
load_dotenv(BASE_DIR / '.env')

APP_NAME = os.getenv('APP_NAME', 'Radar Financeiro Backend')
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
DATABASE_URL = os.getenv('DATABASE_URL', f'sqlite:///{BASE_DIR / "data" / "radar_financeiro_backend.db"}')
ALLOWED_ORIGINS = [origin.strip() for origin in os.getenv('CORS_ORIGINS', '').split(',') if origin.strip()]
