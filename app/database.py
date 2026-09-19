import os
from sqlalchemy import create_engine


DB_HOST = os.getenv("DB_HOST", "localhost")

DATABASE_URL = (
    f"postgresql+psycopg://music_user:music_password@"
    f"{DB_HOST}:5432/music_analytics"
)

engine = create_engine(DATABASE_URL)