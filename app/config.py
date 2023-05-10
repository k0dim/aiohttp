import os

from dotenv import load_dotenv

load_dotenv()

DB = os.getenv('PG_DB')
USER = os.getenv('PG_USER')
PASSWORD = os.getenv('PG_PASSWORD')
HOST = os.getenv('PG_HOST')
PORT = os.getenv('PG_PORT')

DNS = f"postgresql+asyncpg://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}"
TOKEN_TTL = int(os.getenv("TOKEN_TTL", 60 * 60 * 24))