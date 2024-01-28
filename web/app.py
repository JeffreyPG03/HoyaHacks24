from flask import (Flask, Response, flash, make_response, redirect,
                render_template, request, send_file, send_from_directory,
                url_for)

from werkzeug.utils import secure_filename
import os
import threading
import time
from src.lsb.lsb import lsb_encode, lsb_decode
from src.dwt_enc.dwt_enc import dwt_encode, dwt_decode
from src.dwt_wm.dwt_wm import watermark, ext_watermark

app = Flask(__name__)

app.secret_key = "Hoya Hacks 2024"
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app.config['UPLOAD_FOLDER'] = os.path.join(APP_ROOT,'images/')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
@app.route("/home") 
def home():
    return render_template('home.html')

@app.route("/about") 
def about():
    return render_template('about.html')

@app.route("/TextEncryption") 
def TextEncryption():
    return render_template('TextEncryption.html')

@app.route("/ImageStenography") 
def ImageStenography():
    return render_template('ImageStenography.html')

@app.route("/ImageWatermarking")
def ImageWatermarking():
    return render_template('ImageWatermarking.html')

@app.route('/ImageStenography', methods = ["POST"] )
def lsb():
    #gathering file from form
    uploaded_file = request.files['txt_file']
    
    #making sure its not empty
    if uploaded_file.filename != '':
        filename = ''
        target   = os.path.join(APP_ROOT,'images/')
        if uploaded_file and allowed_file(uploaded_file.filename):
            flash('Working....')
            filename    = secure_filename(uploaded_file.filename)
            destination = ''.join([target, filename])
            uploaded_file.save(destination)
            if request.form['submit_form'] == 'Encode':
                data2encode = request.form['etext']
                encodedFileName = filename.split('.')[0]
                encodedFileName = ''.join([encodedFileName, '_encoded.png'])
                encodedName     = ''.join([target, encodedFileName])
                try:
                    lsb_encode(destination, data2encode, encodedName)
                except:
                    flash('File too large')
                thread = threading.Thread(target=removeOld, args=(filename, encodedFileName))
                thread.start()
                return redirect(url_for('download_', name=encodedFileName)) #mimetype = 'image/png'))
            if request.form['submit_form'] == 'Decode':
                decodedText = lsb_decode(destination)
                thread      = threading.Thread(target=removeOld, args=(filename,))
                thread.start()
                return render_template('/ImageStenography.html',
                        PageTitle = "Landing page", decrypted_message=decodedText)
            
        else:
            flash('file not allowed')

    #This just reloads the page if no file is selected and the user tries to POST. 
    else:
        return render_template('/ImageStenography.html',
                        PageTitle = "Landing page", decrypted_message='')
    
@app.route('/ImageWatermarking', methods = ["POST"] )
def dwt_wm():
    #gathering file from form
    uploaded_file = request.files.get('txt_file')
    
    #making sure its not empty
    if uploaded_file.filename != '':
        filename = ''
        target   = os.path.join(APP_ROOT,'images/')
        if uploaded_file and allowed_file(uploaded_file.filename):
            flash('Working....')
            filename    = secure_filename(uploaded_file.filename)
            destination = ''.join([target, filename])
            uploaded_file.save(destination)
            if request.form['submit_form'] == 'Watermark':
                wm_file = request.files['wm_file']
                wm_filename = ''
                wm_filename = secure_filename(wm_file.filename)
                wm_destination = ''.join([target, wm_filename])
                wm_file.save(wm_destination)

                encodedFileName = filename.split('.')[0]
                encodedFileName = ''.join([encodedFileName, '_watermarked.png'])
                encodedName     = ''.join([target, encodedFileName])

                key_filename = 'key.txt'
                key_destination = ''.join([target, key_filename])

                try:
                    watermark(destination, wm_destination, encodedName, key_destination)
                except:
                    flash('File too large')
                thread = threading.Thread(target=removeOld, args=(filename, encodedFileName))
                thread.start()
                return redirect(url_for('download_', name=encodedFileName))
            if request.form['submit_form'] == 'Find Watermark':
                key_file = request.files['key_file']
                key_filename = ''
                key_filename = secure_filename(key_file.filename)
                key_destination = ''.join([target, key_filename])
                key_file.save(key_destination)

                watermark_name = "watermark.png"
                watermark_destination = ''.join([target, watermark_name])

                ext_watermark(destination, key_destination, watermark_destination)
                thread      = threading.Thread(target=removeOld, args=(filename,))
                thread.start()
                return redirect(url_for('download_', name=watermark_name))
            if request.form['submit_form'] == 'Get Key':
                key_filename = 'key.txt'
                thread = threading.Thread(target=removeOld, args=(filename))
                thread.start()
                return redirect(url_for('download_', name=key_filename))
            
        else:
            flash('file not allowed')

    #This just reloads the page if no file is selected and the user tries to POST. 
    else:
        return render_template('/ImageWatermarking.html',
                        PageTitle = "Landing page")
    
@app.route('/images/<name>', methods=['GET', 'POST'])
def download_(name):
    return send_from_directory(app.config['UPLOAD_FOLDER'], name, as_attachment=True)

def removeOld(*args):
    time.sleep(10)
    for file in args:
        filePath = app.config['UPLOAD_FOLDER'] + '/' + file

        os.remove(filePath)
        print('removed', file)

if __name__ == '__main__':
    app.run(debug=True)