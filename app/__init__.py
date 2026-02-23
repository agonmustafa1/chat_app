from flask import Flask, current_app, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, join_room, leave_room, emit
from extensions import db, socketio, login_manager
from flask_login import LoginManager, current_user
from config import Config
from datetime import datetime
from .models import Message, User
from cryptography.fernet import Fernet
from flask_sslify import SSLify

room_messages = {
    'public': [],
    'room1': [],
    'room2': []
}

def create_app():
    app = Flask(__name__)
    sslify = SSLify(app)  # This will redirect all HTTP traffic to HTTPS
    app.config['SECRET_KEY'] = Config.SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat.db'
    
    db.init_app(app)
    socketio.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = 'main.login'

    # Generate and attach the encryption key
    encryption_key = Config.SECRET_KEY1.encode()  # Retrieve from .env
    app.fernet = Fernet(encryption_key)  # Attach the Fernet object

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .routes import main
    app.register_blueprint(main)
    
    with app.app_context():
        db.create_all()

    return app

@socketio.on('join')
def on_join(data):
    username = current_user.username if current_user.is_authenticated else "Anonymous"
    new_room = data['room']
    # Check if the user has an active room stored in the session
    old_room = session.get('current_room')
    if old_room:
        leave_room(old_room)  # Leave the old room
        socketio.emit('left', {'username': username}, to=old_room)

    # Join the new room
    session['current_room'] = new_room  # Update the session
    join_room(new_room)
    emit('messages', {'messages': room_messages[new_room]}, room=request.sid)
    socketio.emit('joined', {'username': username}, to=new_room)


@socketio.on('send_message')
def handle_message(data):
    username = current_user.username if current_user.is_authenticated else "Anonymous"
    message = data['message']
    room = data.get('room')
    timestamp = data.get('timestamp')
    user_id = current_user.id if current_user.is_authenticated else None

    # Encrypt the message content
    encrypted_message = current_app.fernet.encrypt(message.encode()).decode()

    new_message = Message(content=encrypted_message, timestamp=datetime.utcnow(), user_id=user_id, room=room)
    db.session.add(new_message)
    db.session.commit()

    decrypted_message = new_message.decrypt_content(current_app.fernet)  # For broadcast to room
    
    room_messages[room].append({'username': username, 'message': message, 'timestamp': timestamp})
    socketio.emit('message', {'username': username, 'message': decrypted_message}, to=room)

@socketio.on('get_messages')
def get_messages(data):
    room = data['room']
    messages = Message.query.filter_by(room=room).all()
    
    decrypted_messages = []
    for message in messages:
        decrypted_messages.append({
            'username': User.query.get(message.user_id).username,  # Import User correctly
            'message': message.decrypt_content(current_app.fernet),
            'timestamp': message.timestamp
        })
    
    socketio.emit('messages', {'messages': decrypted_messages}, to=room)