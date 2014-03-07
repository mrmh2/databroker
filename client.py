"""seed.py

Test initial data grabber idea.
"""

import json
import urllib2

def get_single_file(host, port, filename):
    """Get single file from specified host/port and save to current directory.
    """

    request_url = 'http://' + host + ':' + str(port) + '/img?name=' + filename

    f_url = urllib2.urlopen(request_url)

    with open(filename, 'wb') as f:
        f.write(f_url.read())

def get_file_list(host, port, project):
    """Get list of files associated with project at host/port"""

    request_url = 'http://' + host + ':' + str(port) + '/list'

    file_list = json.load(urllib2.urlopen(request_url))

    return file_list

def get_all_files(host, port, project):

    file_list = get_file_list(host, port, project)

    for f in file_list['allfiles']:
        print 'Fetching', f['name']
        get_single_file(host, port, f['name'])
    
def main():

    host = "localhost"
    port = 5000



if __name__ == "__main__":
    main()
