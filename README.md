# 🛒 Product Management API

A backend REST API built with **FastAPI** for managing products with secure **JWT authentication**, **PostgreSQL database**, and **SQLAlchemy ORM**.

The project also includes an Excel-based data seeding feature to import product data into the database.

---

## 🚀 Features

- 🔐 User Registration
- 🔑 User Login with JWT Authentication
- 🔒 Protected API Routes
- 🛍️ Product CRUD Operations
- 📦 Product Data Management
- 🗄️ PostgreSQL Database Integration
- 🧩 SQLAlchemy ORM
- 📊 Import Products from Excel
- ⚡ FastAPI REST API
- 📖 Automatic Swagger API Documentation
- 🧱 Modular Project Structure

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Programming Language |
| FastAPI | Backend Framework |
| PostgreSQL | Database |
| SQLAlchemy | ORM |
| Pydantic | Data Validation |
| JWT | Authentication |
| Passlib | Password Hashing |
| Uvicorn | ASGI Server |
| Pandas | Excel Data Processing |
| OpenPyXL | Excel File Handling |

---

## 📁 Project Structure

```text
app/
│
├── models/
│   ├── __init__.py
│   ├── product.py
│   └── user.py
│
├── routes/
│   ├── __init__.py
│   ├── auth.py
│   └── product.py
│
├── seed/
│   ├── __init__.py
│   ├── excel.py
│   └── Product_Data.xlsx
│
├── services/
│   ├── __init__.py
│   ├── auth_service.py
│   └── product_service.py
│
├── database.py
└── main.py
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md