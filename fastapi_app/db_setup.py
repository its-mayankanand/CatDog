# db_setup.py
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

# PostgreSQL connection (replace with your user/pass if different)
DATABASE_URL = "postgresql+psycopg2://catuser:catpass@localhost:5432/catsdb"

# Create engine
engine = create_engine(DATABASE_URL, echo=True)

# Base class for models
Base = declarative_base()

# Define CatBreed model
class CatBreed(Base):
    __tablename__ = "cat_breeds"

    id = Column(Integer, primary_key=True, index=True)
    breed = Column(String, unique=True, index=True, nullable=False)
    origin = Column(String)
    type = Column(String)
    body_type = Column(String)
    coat_type_length = Column(String)
    coat_pattern = Column(String)
    image = Column(String)

# Create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

if __name__ == "__main__":
    print("📌 Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created successfully!")

    # Insert one sample cat
    db = SessionLocal()
    sample_cat = CatBreed(
        breed="Persian",
        origin="Iran",
        type="Longhair",
        body_type="Cobby",
        coat_type_length="Long",
        coat_pattern="Solid",
        image="https://example.com/persian.jpg"
    )

    db.add(sample_cat)
    db.commit()
    db.close()
    print("🐱 Sample cat breed inserted!")
