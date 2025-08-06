# 📰 Real-Time News Portal (FastAPI)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)  
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)  
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-brightgreen)](https://fastapi.tiangolo.com/)  

A high-performance real-time news aggregation portal built with FastAPI that delivers live updates via WebSocket with async REST API endpoints.

---

## ✨ Key Features  
- 🔴 **Live Updates**: WebSocket-powered real-time news streaming  
- ⚡ **High Performance**: Async FastAPI with SQLAlchemy  
- 📡 **REST API**: Auto-generated OpenAPI/Swagger documentation  
- 🛠️ **Admin Tools**: Generate mock news with Faker library  
- 📱 **Responsive UI**: Modern CSS3 with animations  
- 🔐 **JWT Auth**: Secure token-based authentication with bcrypt  
- 🗄️ **SQLite Database**: Lightweight database with ORM models  

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip package manager

### Installation
```bash
# Clone repository
git clone https://github.com/yourusername/fastapi-real-time-news.git
cd fastapi-real-time-news

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Start FastAPI server
cd fastapi-news-portal
uvicorn main:app --host 0.0.0.0 --port 8010 --reload

# Frontend (in new terminal)
cd frontend
python -m http.server 8020
```

---

## 📡 API Documentation

### 🔐 Authentication Endpoints

#### Register User
```bash
curl -X POST 'http://localhost:8010/register/' \
-H 'Content-Type: application/json' \
-d '{
  "username": "admin",
  "password": "yourpassword"
}'
```

#### Login & Get Token
```bash
curl -X POST 'http://localhost:8010/token' \
-H 'Content-Type: application/json' \
-d '{
  "username": "admin", 
  "password": "yourpassword"
}'
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 📰 News Endpoints

#### Get All Articles
```bash
curl -X GET 'http://localhost:8010/api/articles/'
```

#### Generate Fake News (Protected)
```bash
curl -X POST 'http://localhost:8010/api/generate-news/' \
-H 'Authorization: Bearer YOUR_ACCESS_TOKEN'
```

### 🔌 WebSocket Connection
```javascript
const socket = new WebSocket('ws://localhost:8010/ws/news/');
```

---

## 🏗️ Project Structure

```
fastapi-news-portal/
├── main.py              # FastAPI application & routes
├── models.py            # SQLAlchemy ORM models
├── database.py          # Database connection & session
├── auth.py              # JWT authentication logic
├── requirements.txt     # Python dependencies
├── frontend/
│   ├── index.html       # Main frontend page
│   ├── style.css        # Responsive CSS styles
│   └── main.js          # WebSocket & API client
└── README.md
```

## 🛠️ Tech Stack

### Backend:
- **FastAPI** - Modern, fast web framework
- **SQLAlchemy** - Python SQL toolkit and ORM
- **Uvicorn** - ASGI server implementation
- **SQLite** - Lightweight database
- **WebSockets** - Real-time bidirectional communication
- **JWT** - JSON Web Token authentication
- **Bcrypt** - Password hashing
- **Faker** - Generate fake data for testing

### Frontend:
- **Vanilla JavaScript** - Pure JS with modern ES6+ features
- **HTML5** - Semantic markup
- **CSS3** - Modern styling with animations & grid
- **WebSocket API** - Browser native WebSocket support

---

## 🔧 Development

### Database Models
The application uses SQLAlchemy with SQLite for data persistence:
- Articles are stored with auto-incrementing IDs
- Users have bcrypt-hashed passwords
- Database is created automatically on first run

### WebSocket Broadcasting
When new articles are generated:
1. Article is saved to database
2. WebSocket manager broadcasts to all connected clients
3. Frontend receives update and adds article to DOM

---

## 🚀 Deployment

### Production Setup
```bash
# Install production server
pip install gunicorn

# Run with Gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8010

# Or with Uvicorn (recommended)
uvicorn main:app --host 0.0.0.0 --port 8010 --workers 4
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

---

## 📞 Support

- Create an issue for bug reports
- Star ⭐ the repo if you find it useful
- Follow [@yourusername](https://github.com/yourusername) for updates

---

**Made with ❤️ and FastAPI**