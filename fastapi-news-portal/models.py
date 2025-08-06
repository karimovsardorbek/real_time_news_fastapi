from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

# User model for the database
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


# Article model for the database
class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    summary = Column(String, nullable=False)
    publication_date = Column(DateTime, default=datetime.utcnow)
    author = Column(String(100), nullable=True)
    image = Column(String(255), nullable=True)  # URL field

    def __repr__(self):
        return f"<Article(title={self.title})>"