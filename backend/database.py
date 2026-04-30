import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Load from .env
load_dotenv()

#Create the engine that manages the connection to PostgreSQL
engine = create_engine(os.getenv("DATABASE_URL"))

# Provide a direct database connection for each request
def get_db():
    with engine.connect() as conn:
        yield conn