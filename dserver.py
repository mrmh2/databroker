"""dserver.py

Data server.
"""

import os
import shutil
import logging

from flask import send_file, Flask, request
from flask import jsonify, abort
from werkzeug.utils import secure_filename

from itemise import itemise

app = Flask(__name__)

data_root = 'img'

all_projects = itemise(data_root)

@app.route('/img/<project>/<filename>')
def get_file(project, filename):
    full_path = os.path.join(data_root, project, filename)
    logging.debug('Client requested ' + full_path)

    return send_file(full_path, mimetype='image/png')

    
@app.route('/list/<project>')
def get_list(project):

    all_projects = itemise(data_root)

    if project in all_projects:
        return jsonify( { 'allfiles' : all_projects[project] } )
    else:
        abort(404)

@app.route('/upload/<project>/<filename>', methods=['POST'])
def upload(project, filename):

    data_dir = os.path.join(data_root, project)

    filename = secure_filename(filename)
    file = request.files['file']
    dest_path = os.path.join(data_dir, filename)
    logging.debug('Will save POSTed data to ' + dest_path)
    file.save(dest_path)

    return 'Success'

@app.route('/create/<project>', methods=['POST'])
def create(project):

    project_dir = os.path.join(data_root, project)

    try:
        os.mkdir(project_dir)
    except OSError, e:
        if e.errno == 17:
            pass
        else:
            raise e

    return 'Success' # TODO: Failure

@app.route('/delete/<project>', methods=['DELETE'])
def delete(project):
    
    project_dir = os.path.join(data_root, project)

    logging.debug('Will delete ' + project_dir)

    try:
        shutil.rmtree(project_dir)
    except OSError, e:
        print e

    return 'Success' # TODO: More failure

def main():

    try:
        os.mkdir('log')
    except OSError, e:
        if e.errno == 17: # Directory exists
            pass
        else:
            raise e

    logging.basicConfig(filename='log/dserver.log', level=logging.DEBUG)
    app.run(debug=True)

if __name__ == "__main__":
    main()
