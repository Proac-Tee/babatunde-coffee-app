from dotenv import load_dotenv
import os

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#
load_dotenv()
DB_HOST = os.getenv("DB_HOST", "127.0.0.1:5432")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PATH = f"postgresql+psycopg2://{DB_USER}:@{DB_HOST}/{DB_NAME}"


AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
ALGORITHMS = os.environ.get("RS256")
API_AUDIENCE = os.environ.get("API_AUDIENCE")
