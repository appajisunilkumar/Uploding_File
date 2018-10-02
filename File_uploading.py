from flask import Flask, url_for, send_from_directory, request, jsonify
import logging, os
from werkzeug import secure_filename
import random

app = Flask(__name__)
file_handler = logging.FileHandler('server.log')
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)

PROJECT_HOME = os.path.dirname(os.path.realpath(__file__))
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['.txt', '.pdf', '.png', '.jpg', 'jpeg', '.gif'])

def create_new_folder(local_dir):
    newpath = local_dir
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    return newpath




@app.route('/', methods = ['POST' , 'PUT'])
def api_root(): 
    #app.logger.info(PROJECT_HOME)
    if (request.method == 'POST') and ('file' in request.files):
        app.logger.info(app.cnofig['UPLOAD_FOLDER'])
        img = request.files['file']
        folder_name = request.form['username']
        folder_name = create_new_folder(UPLOAD_FOLDER+folder_name)
        status = {}
        saved_paths = []
        file_names = []
        for f in request.files.getlist("file"):
            print "Into forloop"
            img_name = secure_filename(f.filename).lower()
            
            if img_name[-4:] in ALLOWED_EXTENSIONS:
                saved_path = os.path.join(folder_name, img_name)
                app.logger.info("saving {}".format(saved_path))
                f.save(saved_path)
                saved_paths.append(saved_path)
                file_names.append(img_name)
                return jsonify({"status":"File uploaded"})
                
            else:
                return jsonify({"status":"Extension Not Allowed"})
        
        
        
        files_dict = {w:j for (w,j) in zip(saved_paths, file_names)}
        return jsonify({w for w in files_dict})

    else:
        return jsonify({"status":"Where is the File?"})

if __name__ == '__main__':
    app.run(host='0.0.0.0',port = 8800, debug=True)