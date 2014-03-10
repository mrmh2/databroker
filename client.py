"""seed.py

Test initial data grabber idea.
"""

import os
import json
import urllib2

import requests

def get_single_file(host, port, project, filename):
    """Get single file from specified host/port and save to current directory.
    """

    request_url = 'http://%s:%d/img/%s/%s' % (host, port, project, filename)

    #print "Will request", request_url

    f_url = urllib2.urlopen(request_url)

    with open(filename, 'wb') as f:
        f.write(f_url.read())

def get_file_list(host, port, project):
    """Get list of files associated with project at host/port"""

    request_url = 'http://%s:%d/list/%s' % (host, port, project)

    file_list = json.load(urllib2.urlopen(request_url))

    return file_list

def get_all_files(host, port, project):

    file_list = get_file_list(host, port, project)

    for f in file_list['allfiles']:
        print 'Fetching', f['name']
        get_single_file(host, port, project, f['name'])

def upload_file(host, port, project, local_file):
    """Upload local file to server"""

    filename = os.path.basename(local_file)

    request_url = 'http://%s:%d/upload/%s/%s' % (host, port, project, filename)

    files = {'file': open(local_file, 'rb')}

    r = requests.post(request_url, files=files)
    
def main():

    host = "localhost"
    port = 5000

    #get_all_files(host, port, 'surfy')
    #upload_file(host, port, 'testproj', 'Gravatar.png')
    upload_file(host, port, 'testproj', '/Users/hartleym/Dropbox/Tufte.pdf')

if __name__ == "__main__":
    main()
