from flask import Flask, render_template, request, jsonify, session, send_from_directory
from flask_session import Session
from werkzeug.utils import secure_filename
from requests_toolbelt.multipart.encoder import MultipartEncoder
from dotenv import load_dotenv
import requests
import uuid
import os
import json

load_dotenv()

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'md'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SESSION_TYPE'] = 'filesystem'  # You can choose others like 'redis', but for simplicity, we'll use 'filesystem'
app.config['UPLOAD_FOLDER'] = 'uploads'

Session(app)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# @app.route('/api_url')
# def api_url():
#     return jsonify({"api_url": os.getenv('FLOWISE_API_URL')})

@app.route('/')
def index():
    # Check if a UUID exists for the session, if not, create one
    if 'uuid' not in session:
        session['uuid'] = str(uuid.uuid4())
    session.permanent = True  # Make the session permanent
    if 'uploaded_file' in session:
        uploaded_file = session['uploaded_file']
    else:
        uploaded_file = ""
    return render_template('index.html', uploaded_file=uploaded_file)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/get_uuid')
def get_uuid():
    return jsonify({"uuid": session['uuid']})

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    question = data['question']

    request_body = {
        'question': question,
        'overrideConfig': {
            'sessionId': data['uuid']
        }
    }
    headers = {
        'Content-Type': 'application/json',
    }

    API_URL = os.getenv('FLOWISE_API_URL')
    if 'uploaded_file' in session:
        # use form data to upload files
        form_data = {
            "files": (session['uploaded_file'], open(session['uploaded_file'], 'rb')),
        }

        body_data = {
            "question": question
        }

        response = requests.post(API_URL, files=form_data, data=body_data)
    else:
        response = requests.post(API_URL, headers=headers, json=request_body)

    return jsonify(response.json())


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        file.save(filepath)
        
        # Store the filepath in the user's session data
        session['uploaded_file'] = filepath
        
        return jsonify({"message": "File uploaded successfully"}), 200
    else:
        return jsonify({"error": "File type not allowed"}), 400

if __name__ == "__main__":
    app.run(debug=True, port=5001)
