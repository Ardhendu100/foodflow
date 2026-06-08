# This module will handle the database session management, including creating and closing sessions.
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from foodflow.shared.config.settings import settings

engine = create_engine(
    settings.DATABASE_URL,
    echo=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()
