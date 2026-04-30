from sqlalchemy import text
from database import engine

def init_db():
    sql_files = ["createTables.sql", "seedData.sql"]
    
    # Executing each SQL file to set up the database structure and seed data
    with engine.connect() as conn:
        for file_name in sql_files:
            with open(file_name, "r") as f:
                content = f.read()
                conn.execute(text(content))
        
        conn.commit()
    print("Database structure and data initialized!")

if __name__ == "__main__":
    init_db()