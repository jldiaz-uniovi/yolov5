import os
from flask import Flask, request, redirect, url_for, flash, render_template_string
from flask import send_from_directory
from flask.json import jsonify
from werkzeug.utils import secure_filename
from mini_detect import label_image, load_model, detect, get_meta

# Some constants
UPLOAD_FOLDER = './server/uploads'
DETECTIONS_FOLDER = './server/detections'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}


# Create app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DETECTIONS_FOLDER'] = DETECTIONS_FOLDER
app.config['SECRET_KEY'] = "replace-me"

# Prepare Yolo model
model = load_model("yolov5m")

# Utility functions
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def detect_and_label_image(filename):
    _in = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    _out = app.config['DETECTIONS_FOLDER']
    r = detect(_in, model)
    label_image(_in, r, _out)


def detect_and_get_meta(filename):
    _in = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    r = detect(_in, model)
    return get_meta(r)

# FLASK routes
@app.route('/detect', methods=['GET', 'POST'])
def upload_file():
    if request.method == "GET":
        return render_template_string('''
        <!doctype html>
        <head>
        <title>YOLO5 - Subir imagen</title>
        <style>
        ul.flashes {
            background-color: #f0d0d0;
            color: #804040;
            list-style-type: none;
            width: 25%;
        }
        </style>
        </head>
        <body>
        <h1>YOLO5 - Subir imagen</h1>
        {% with messages = get_flashed_messages() %}
        {% if messages %}
            <ul class=flashes>
            {% for message in messages %}
            <li>{{ message }}</li>
            {% endfor %}
            </ul>
        {% endif %}
        {% endwith %}        
        <form method=post enctype=multipart/form-data>
            <input type="file" name="file" id="file" aria-label="File browser example">
            <input type=submit value=Subir>
            <p>Tipo de resultado</p>
            <input type=radio id=imagen name=tipo value=imagen checked>
            <label for=imagen>Imagen etiquetada</label>
            <input type=radio id=json name=tipo value=json> 
            <label for=json>JSON</label>
        </form>
        </body>
        ''')
    if 'file' not in request.files or not request.files["file"]:
        flash('No se ha subido ningún fichero')
        return redirect(request.url)
    file = request.files['file']
    if not file or not allowed_file(file.filename):
        flash("Tipo de fichero no admitido (solo jpg o png)")
        return redirect(request.url)
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    if request.form["tipo"] == "imagen":
        detect_and_label_image(filename)
        return redirect(url_for('uploaded_file',
                                filename=filename))
    else:
        metadata = detect_and_get_meta(filename)
        return jsonify(metadata)



@app.route('/detections/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['DETECTIONS_FOLDER'],
                               filename)
