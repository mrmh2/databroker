"""dserver.py

Data server.
"""

import os

from flask import send_file, Flask, request
from flask import jsonify, abort

from itemise import itemise

app = Flask(__name__)

@app.route('/img')
def index():
    img_dir = 'img'

    requested_file = request.args.get('name')
    full_path = os.path.join(img_dir, requested_file)

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
    app.run(debug=True)

if __name__ == "__main__":
    main()
