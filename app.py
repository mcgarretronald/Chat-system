from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, join_room, leave_room, send
import random
import string

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

def generate_room_code():
    return ''.join(random.choices(string.ascii_uppercase, k=4))

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/chat', methods=['POST'])
def chat():
    username = request.form['username']
    room_code = request.form.get('room_code') or generate_room_code()
    return render_template('chat.html', username=username, room_code=room_code)

@socketio.on('join')
def handle_join(data):
    join_room(data['room'])
    send({'username': data['username'], 'message': f"{data['username']} has joined the room."}, to=data['room'])

@socketio.on('leave')
def handle_leave(data):
    leave_room(data['room'])
    send({'username': data['username'], 'message': f"{data['username']} has left the room."}, to=data['room'])

@socketio.on('message')
def handle_message(data):
    message_data = {
        'username': data['username'],
        'message': data['message']
    }
    send(message_data, to=data['room'])

if __name__ == '__main__':
    socketio.run(app, debug=True)
