import os
import qrcode
import base64
from io import BytesIO
from flask import Flask, render_template, jsonify, request
import threading
import socket
from datetime import datetime

app = Flask(__name__)
lock = threading.Lock()

def get_and_remove_key(filename):
    # Extract the first key from the file and delete it.
    with lock: 
        with open(filename, 'r') as file:
            lines = file.readlines()
        
        if lines:
            key = lines[0].strip()
            with open(filename, 'w') as file:
                file.writelines(lines[1:])
            return key
        else:
            return None

def generate_qr_code(key):
    """Generate a QR Code from the given key."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(key)
    qr.make(fit=True)

    img = qr.make_image(fill_color='black', back_color='white')
    buffered = BytesIO()
    img.save(buffered, format='PNG')

    img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
    return img_base64

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_code', methods=['POST'])
def generate_code():
    duration = request.get_json().get('duration')
    filepath = './keys/' + duration + '.txt'

    if not os.path.exists(filepath):
        return jsonify({'message': 'Ungültige Gültigkeitsdauer. Bitte wenden Sie sich an den Systemadministrator.', 'error': f"Die Datei {filepath} existiert nicht."}), 404
    
    key = get_and_remove_key(filepath)
    write_logfile(duration, key)
    if key:
        qr_code = generate_qr_code(key)
        return jsonify({'key': key, 'qr_code': qr_code})
    else:
        return jsonify({'message': 'Die Voucher-Codes für die gewählte Gültigkeitsdauer sind nicht mehr vorrätig. Bitte wenden Sie sich an den Systemadministrator.', 'error': f"Die Datei {filepath} enthält keine Voucher-Codes."}), 404

def write_logfile(duration, key):
    # get IP-adress from client
    client_ip = request.remote_addr
    try:
        client_hostname = socket.gethostbyaddr(client_ip)[0]
    except socket.herror:
        client_hostname = 'Hostname konnte nicht aufgelöst werden'
    os.makedirs('./logs', exist_ok=True)
    with open('./logs/client_logs.log', 'a') as logfile:
        logfile.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')} - {client_ip} - {client_hostname} - {duration} : {key}\n")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
