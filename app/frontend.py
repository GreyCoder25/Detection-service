import os
from flask import Flask, Blueprint, request, redirect, url_for, send_from_directory, render_template
from werkzeug.utils import secure_filename
from .detection import detect

INPUT_FOLDER = '/static/input-images'
OUTPUT_FOLDER = '/static/output-images'

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
INPUT_FILE_PATH = ''
DETECTION_RESULT = ''

frontend = Blueprint('frontend', __name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@frontend.route('/', methods=['GET', 'POST'])
def upload_file():
    from . import app
    global INPUT_FILE_PATH
    global DETECTION_RESULT
    if request.method == 'POST':
        if request.files.get('file', None) is not None:
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                INPUT_FILE_PATH = os.path.join(app.config['INPUT_FOLDER'], filename)
                print(INPUT_FILE_PATH)
                file.save(os.path.join('./app', INPUT_FILE_PATH[1:]))
                DETECTION_RESULT = os.path.join(app.config['OUTPUT_FOLDER'], filename)
                detect(os.path.join('./app', INPUT_FILE_PATH[1:]), os.path.join('./app', DETECTION_RESULT[1:]))
                return render_template('home.html', user_image=INPUT_FILE_PATH, detection_result=DETECTION_RESULT)
        
    return render_template('home.html', user_image=INPUT_FILE_PATH, detection_result=DETECTION_RESULT)

if __name__ == "__main__":
    app.run(debug=True)
