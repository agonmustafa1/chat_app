# Chat Web App

A real-time chat web application built with Flask that allows users to register, log in, and communicate securely in different chat rooms.

## Features

- User registration and authentication
- Secure login system
- Multiple chat rooms
- Real-time messaging using WebSockets
- End-to-end message encryption using Fernet
- Password hashing using PBKDF2
- Messages securely stored in a database
- Self-signed HTTPS configuration for secure connections during development

---

## Technologies Used

- Python
- Flask
- Flask-SocketIO (WebSockets)
- Fernet (symmetric encryption)
- PBKDF2 (password hashing)
- SQLAlchemy / Database
- HTML, CSS, JavaScript

---

## Security Features

### Password Security
User passwords are hashed using **PBKDF2**, ensuring secure storage and resistance against brute-force attacks.

### Message Encryption
All messages are encrypted using **Fernet symmetric encryption** before being stored in the database.

### HTTPS
The app uses a **self-signed SSL certificate** for secure HTTPS connections in development.

---

## Installation

### 1 Clone the repository

```bash
git clone https://github.com/agonmustafa1/chat_app.git
cd chat_app
```

### 2 Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

**Windows:**
```bash
.venv\Scripts\activate
```

**Mac/Linux:**
```bash
source .venv/bin/activate
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Application

```bash
python run.py
```

Then open your browser and go to:

```
https://127.0.0.1:5000
```

> Note: You may see a browser warning for the self-signed certificate — this is expected in a local development environment.

---

## 💬 How It Works

1. Users register an account.
2. Passwords are securely hashed using PBKDF2.
3. Users log in and join chat rooms.
4. Messages are sent in real time using WebSockets.
5. Messages are encrypted with Fernet before being stored in the database.
6. Encrypted messages are decrypted when displayed to authorized users.

---

## 🧠 Future Improvements

- Private messaging
- User profile management
- Message search
- Docker deployment
- Production-ready configuration

---

## 📜 License

This project is for educational purposes.