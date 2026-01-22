# Customer Management System

A full-stack customer management app with **React** (frontend) and **FastAPI** (backend).

## Prerequisites

- Python 3.10+
- Node.js 18+
- Docker (for MySQL database)

## Quick Start

### 1. Start Database

```bash
cd docker
docker-compose up -d
docker exec -it my-mysql mysql -u myuser -p mydatabase
```

### 2. Start Server

```bash
# From project root
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cd server/app
python main.py
```

Server runs at: **http://127.0.0.1:8000**

### 3. Start Client

```bash
cd client
npm install
npm run dev
```

Client runs at: **http://localhost:5173**

## API Docs

Swagger UI available at: http://127.0.0.1:8000/docs
