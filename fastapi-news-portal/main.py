from fastapi import FastAPI, Depends, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.responses import JSONResponse
from models import Article, User
from database import get_db, engine
from sqlalchemy.orm import Session
from auth import create_access_token, get_current_user, Token, get_password_hash, verify_password
from faker import Faker
import random
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8020"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db_session():
    db = next(get_db())
    try:
        yield db
    finally:
        db.close()

# Pydantic models
class UserCreate(BaseModel):
    username: str
    password: str

class ArticleResponse(BaseModel):
    id: int
    title: str
    summary: str
    publication_date: datetime  # Changed to datetime
    author: str | None = None
    image: str | None = None

    class Config:
        orm_mode = True  # Enables Pydantic to read data from ORM models

@app.post("/register/")
async def register(user: UserCreate, db: Session = Depends(get_db_session)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(user.password)
    new_user = User(username=user.username, password_hash=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created successfully"}

@app.post("/token", response_model=Token)
async def login(user: UserCreate, db: Session = Depends(get_db_session)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token({"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/articles/", response_model=list[ArticleResponse])
async def get_articles(db: Session = Depends(get_db_session)):
    articles = db.query(Article).all()
    return articles

@app.post("/api/generate-news/", response_model=ArticleResponse)
async def generate_news(current_user: User = Depends(get_current_user), db: Session = Depends(get_db_session)):
    fake = Faker()
    random_image_url = f"https://picsum.photos/seed/{random.randint(1, 10000)}/600/400"
    article = Article(
        title=fake.sentence(),
        summary=fake.paragraph(nb_sentences=10),
        author=fake.name() if random.choice([True, False]) else None,
        image=random_image_url
    )
    db.add(article)
    db.commit()
    db.refresh(article)
    # Broadcast the new article to all WebSocket clients
    await manager.broadcast({"article": {"id": article.id, "title": article.title, "image": article.image}})
    return article

# WebSocket Manager and Endpoint
class ConnectionManager:
    def __init__(self):
        self.active_connections = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)

manager = ConnectionManager()

@app.websocket("/ws/news/")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    db = next(get_db())
    try:
        # Send existing articles on connection
        articles = db.query(Article).order_by(Article.id.desc()).all()
        for article in articles:
            await websocket.send_json({"article": {"id": article.id, "title": article.title, "image": article.image}})
        while True:
            data = await websocket.receive_text()
            await manager.broadcast({"message": data})
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    finally:
        db.close()