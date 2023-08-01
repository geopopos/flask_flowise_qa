import os
from flask import Flask, request, redirect, url_for, render_template, session, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'mysecretkey'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

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

@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if the POST request has the file part
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    # If the user does not select a file, the browser submits an empty file
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        # Create the uploads directory if it does not exist
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        file.save(filepath)
        session['uploaded_file'] = filename
        return redirect(url_for('index'))
    else:
        return redirect(request.url)