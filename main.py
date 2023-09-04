import os
import json
import socket
from datetime import datetime
from flask import Flask, request, render_template

app = Flask(__name__)

# F. for processing data and record it from data.json
def save_data_to_json(data):
    try:
        with open('storage/data.json', 'r') as file:
            data_dict = json.load(file)
    except FileNotFoundError:
        data_dict = {}
    
    timestamp = str(datetime.now())
    data_dict[timestamp] = data

    with open('storage/data.json', 'w') as file:
        json.dump(data_dict, file, indent=4)

# F. for sending data to Socket service
def send_data_to_socket(data):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.sendto(json.dumps(data).encode(), ('localhost', 5000))
    except Exception as e:
        print(f"Error sending data to socket server: {e}")

# Main page
@app.route('/')
def index():
    return render_template('index.html')

# Form page
@app.route('/message', methods=['GET', 'POST'])
def message():
    if request.method == 'POST':
        username = request.form.get('username')
        message = request.form.get('message')
        
        if username and message:
            data = {
                'username': username,
                'message': message
            }
            save_data_to_json(data)
            send_data_to_socket(data)
            return 'Message sent successfully!'
    
    return render_template('message.html')

# Error 404
@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html'), 404

if __name__ == '__main__':
    # Перевірка наявності папки storage
    if not os.path.exists('storage'):
        os.makedirs('storage')
    
    # Running HTTP server and Socket server in d. threads
    import threading
    from werkzeug.serving import run_simple

    def run_flask():
        run_simple('localhost', 3000, app)

    def run_socket_server():
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.bind(('localhost', 5000))
            while True:
                data, _ = sock.recvfrom(1024)
                try:
                    data_dict = json.loads(data.decode())
                    save_data_to_json(data_dict)
                except json.JSONDecodeError as e:
                    print(f"Error decoding data: {e}")

    flask_thread = threading.Thread(target=run_flask)
    socket_thread = threading.Thread(target=run_socket_server)

    flask_thread.start()
    socket_thread.start()

    flask_thread.join()
    socket_thread.join()
