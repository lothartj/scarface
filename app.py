from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from scanner import WebsitePathScanner
import threading

app = Flask(__name__)
app.config['SECRET_KEY'] = 'scarface-secret-key'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

def scan_website_background(url, delay=0.1, workers=5):
    scanner = WebsitePathScanner(url, delay, workers)
    
    def progress_callback(status, message, path=None, code=None):
        data = {
            'status': status,
            'message': message,
            'path': path,
            'code': code
        }
        socketio.emit('scan_update', data)
    
    scanner.set_callback(progress_callback)
    scanner.scan_website()

@socketio.on('start_scan')
def handle_scan_start(data):
    url = data.get('url')
    if not url:
        emit('scan_update', {'status': 'error', 'message': 'URL is required'})
        return
    
    threading.Thread(target=scan_website_background, args=(url,)).start()
    emit('scan_update', {'status': 'started', 'message': f'Starting scan of {url}'})

if __name__ == '__main__':
    socketio.run(app, debug=True) 