from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os, sys

def _get_db_path():
    if getattr(sys, "frozen", False):
        exe_dir = os.path.dirname(sys.executable)
    else:
        exe_dir = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(exe_dir, "data.db")

DB_FILE = _get_db_path()
DB_URL = f"sqlite:///{DB_FILE}"

engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def init_db():
    Base.metadata.create_all(bind=engine)

def get_session():
    return SessionLocal()
