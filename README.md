 FastAPI TODO Backend

This repository contains the **backend-only implementation** of a TODO application built using **FastAPI**.

There is **no frontend/UI** included in this project.  
The backend exposes REST APIs that can be consumed by any frontend (React, Angular, Mobile app, etc.).

---

## 🚀 Tech Stack

- **FastAPI** – Backend framework
- **PostgreSQL** – Database
- **SQLAlchemy** – ORM
- **JWT (OAuth2 Password Flow)** – Authentication
- **Passlib (Argon2)** – Password hashing
- **Uvicorn** – ASGI server

---

## ✅ Features

### 🔹 Authentication
- User registration
- User login with JWT
- Protected routes using OAuth2

### 🔹 TODO Management
- Create TODOs
- View user-specific TODOs
- Mark TODOs as completed
- Filter TODOs using query parameters (`completed=true/false`)

### 🔹 Backend Capabilities
- PostgreSQL database integration
- User-specific data isolation
- Background tasks (email notification simulation)
- RESTful API design

---


---

## ▶️ Running the Project

### 1️⃣ Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
