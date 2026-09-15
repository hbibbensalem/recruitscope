import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

USER = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")
HOST = os.getenv("DB_HOST")
PORT = os.getenv("DB_PORT")
DBNAME = os.getenv("DB_NAME")

if not all([USER, PASSWORD, HOST, PORT, DBNAME]):
    raise ValueError("Variables DB manquantes dans le fichier .env")

DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}"

# pool_pre_ping évite les connexions "mortes" (utile en prod / après veille du container DB)
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Générateur de session, à utiliser avec FastAPI plus tard (Depends(get_db))."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
