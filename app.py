from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from scanner import WebsitePathScanner
import threading

app = Flask(__name__)
app.config['SECRET_KEY'] = 'scarface-secret-key'
socketio = SocketIO(app)

# Add this global variable at the top of the file
active_scanner = None

@app.route('/')
def index():
    return render_template('index.html')

def scan_website_background(url, delay=0.1, workers=5, wordlists=None):
    global active_scanner
    scanner = WebsitePathScanner(url, delay, workers)
    active_scanner = scanner
    
    scanner.wordlists = wordlists or {}
    
    def progress_callback(status, message, path=None, code=None, counts=None):
        data = {
            'status': status,
            'message': message,
            'path': path,
            'code': code,
            'baseUrl': url
        }
        if counts:
            data['counts'] = counts
        socketio.emit('scan_update', data)
    
    scanner.set_callback(progress_callback)
    scanner.scan_website()
    active_scanner = None

@socketio.on('start_scan')
def handle_scan_start(data):
    url = data.get('url')
    wordlists = data.get('wordlists', {})
    
    if not url:
        emit('scan_update', {'status': 'error', 'message': 'URL is required'})
        return
    
    threading.Thread(
        target=scan_website_background,
        args=(url,),
        kwargs={'wordlists': wordlists}
    ).start()
    
    emit('scan_update', {'status': 'started', 'message': f'Starting scan of {url}'})

@socketio.on('stop_scan')
def handle_stop_scan():
    global active_scanner
    if active_scanner:
        active_scanner.stop_scan()
        emit('scan_update', {'status': 'stopped', 'message': 'Scan stopped by user'})

if __name__ == '__main__':
    socketio.run(app, debug=True) 