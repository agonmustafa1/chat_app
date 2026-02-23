from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from cryptography.fernet import Fernet

def load_encryption_key():
    from dotenv import load_dotenv
    import os

    load_dotenv()
    return os.getenv('SECRET_KEY1')

encryption_key = load_encryption_key()
fernet = Fernet(encryption_key)  # Create the fernet instance with the loaded key

db = SQLAlchemy()
socketio = SocketIO()
login_manager = LoginManager()
jwt = JWTManager()
