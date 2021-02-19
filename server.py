import os
from flask import Flask, flash, request, redirect, url_for
from flask import send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)


UPLOAD_FOLDER = './server/uploads'
DETECTIONS_FOLDER = './server/detections'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DETECTIONS_FOLDER'] = DETECTIONS_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/detect', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        print(request.files)
        if 'file' not in request.files:
            print('Falta la parte del fichero')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            print('No se ha seleccionado fichero')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            run_detect(filename)
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

@app.route('/detections/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['DETECTIONS_FOLDER'],
                               filename)

from my_detect import detect
def run_detect(filename):
    detect(os.path.join(app.config['UPLOAD_FOLDER'], filename))