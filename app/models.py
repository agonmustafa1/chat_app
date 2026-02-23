from extensions import db, fernet
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)

    messages = db.relationship('Message', backref='user', lazy=True)  # Relationship with messages

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)  # Message body
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())  # Auto timestamp
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Sender's user ID
    room = db.Column(db.String(100), nullable=False)  # Chat room name

    def encrypt_content(self, fernet):
        """Encrypt the message content using Fernet."""
        self.content = fernet.encrypt(self.content.encode()).decode()

    def decrypt_content(self, fernet):
        """Decrypt the message content using Fernet."""
        return fernet.decrypt(self.content.encode()).decode()

