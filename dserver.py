"""dserver.py

Data server.
"""

import os

from flask import send_file, Flask, request
from flask import jsonify

app = Flask(__name__)

@app.route('/img')
def index():
    img_dir = 'img'

    requested_file = request.args.get('name')
    full_path = os.path.join(img_dir, requested_file)

    return send_file(full_path, mimetype='image/png')

allfiles = [
    { 'name' : 'projection1.png',
      'type' : 'png' },
    { 'name' : 'projection2.png',
      'type' : 'png' },
]
    
@app.route('/list')
def getlist():
    return jsonify( { 'allfiles' : allfiles } )

@app.route('/wurble/<project>')
def wurble(project):
    return 'wurlble!' + project

def main():
    app.run(debug=True)

if __name__ == "__main__":
    main()
