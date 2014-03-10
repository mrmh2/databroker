"""dserver.py

Data server.
"""

import os
import logging

from flask import send_file, Flask, request
from flask import jsonify, abort

from itemise import itemise

app = Flask(__name__)

@app.route('/img/<project>/<filename>')
def index(project, filename):
    img_dir = 'img'

    full_path = os.path.join(img_dir, project, filename)
    logging.debug('Client requested ' + full_path)

    return send_file(full_path, mimetype='image/png')

comp_im = [
    { 'name' : 'projection1.png',
      'type' : 'png' },
    { 'name' : 'projection2.png',
      'type' : 'png' },
]

surfy = [
    { 'name' : 'surface.png',
      'type' : 'png' }
]

all_projects = {
    'compimg' : comp_im,
    'surfy' : surfy
}

all_projects = itemise('img')
    
@app.route('/list/<project>')
def getlist(project):
    if project in all_projects:
        return jsonify( { 'allfiles' : all_projects[project] } )
    else:
        abort(404)

@app.route('/wurble/<project>')
def wurble(project):
    return 'wurlble!' + project

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
