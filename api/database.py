from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Adjust port if needed (5433 in your case)
DATABASE_URL = "postgresql://postgres:postgres@localhost:5433/medical_warehouse"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
