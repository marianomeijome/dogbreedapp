import os

from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename

#from flask_sqlalchemy import SQLAlchemy
from mypup import *

UPLOAD_FOLDER = 'img/uploads/mdb'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploads/mdb/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
# homepage
@app.route('/')
def index():
    return render_template('index.html')

#dogbreed.app
@app.route('/mydogbreed', methods=['GET', 'POST'])
def mydogbreed():
    breed = None
    breedName = None
    accuracy = 0.0
    if request.method == 'POST':
        
#        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            prediction = topThree("img/uploads/mdb/"+filename)
            breedName = prediction
            return render_template('breed-results.html', **locals())
    
    return render_template('mydogbreed.html')

if __name__ == '__main__':
#    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    app.run(debug=True, host='0.0.0.0')