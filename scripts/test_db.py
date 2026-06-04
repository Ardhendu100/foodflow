from sqlalchemy import text

from foodflow.infrastructure.database.session import engine


with engine.connect() as connection:
    result = connection.execute(text("SELECT 1"))

    print("Database connected successfully!")
    print(result.scalar())
