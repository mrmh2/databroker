"""seed.py

Test initial data grabber idea.
"""

import os
import json
import string
import random
import urllib2
import argparse
import tempfile

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

def create_proj(host, port, project):
    """Create new project"""

    request_url = 'http://%s:%d/create/%s' % (host, port, project)

    r = requests.post(request_url)

class DserverClient(object):
    
    def __init__(self, host, port):
        self.host = host
        self.port = port

        self.urlroot = 'http://%s:%d' % (host, port)

    def delete_project(self, project):
        """Delete project and all associated files"""

        request_url = self.urlroot + '/delete/%s' % project

        r = requests.delete(request_url)

    def create_project(self, project):
        """Create new project"""
	
        request_url = self.urlroot + '/create/%s' % project
	
        r = requests.post(request_url)

    def upload_file(self, project, local_file):
        """Upload local file to server"""
	
        filename = os.path.basename(local_file)
	
        request_url = self.urlroot +  '/upload/%s/%s' % (project, filename)
	
        files = {'file': open(local_file, 'rb')}
	
        r = requests.post(request_url, files=files)

    def get_file_list(self, project):
        """Get list of files associated with project at host/port"""
   
        request_url = self.urlroot + '/list/%s' % project
   
        file_list = json.load(urllib2.urlopen(request_url))
   
        return file_list

    def get_single_file(self, project, filename):
        """Get single file from specified host/port and save to current directory.
        """
    
        request_url = self.urlroot + '/img/%s/%s' % (project, filename)
    
        f_url = urllib2.urlopen(request_url)
    
        with open(filename, 'wb') as f:
            f.write(f_url.read())

    def get_all_files(self, project):
    
        file_list = self.get_file_list(project)
    
        for f in file_list['allfiles']:
            self.get_single_file(project, f['name'])

        return [f['name'] for f in file_list['allfiles']]
    
def create_test_file(test_text):

    f = tempfile.NamedTemporaryFile(delete=False)
    f.write(test_text)
    f.close()

    return f.name

def test_server(host, port):
    
    project_name = ''.join(random.choice(string.lowercase) for _ in range(10))

    # Create the client object
    dsc = DserverClient(host, port)

    # Test project creation
    dsc.create_project(project_name)

    # Test file upload
    test_text = 'hello, hello'
    test_file = create_test_file(test_text)
    dsc.upload_file(project_name, test_file)

    # Test file download
    fnames = dsc.get_all_files(project_name)
    assert open(fnames[0]).readlines()[0] == test_text
    for fn in fnames:
        os.remove(fn)

    os.remove(test_file)

    # Test project deletion
    dsc.delete_project(project_name)

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--host", help="server hostname", default="localhost")
    parser.add_argument("--port", help="server port", default=5000)
    args = parser.parse_args()

    host = args.host
    port = args.port

    test_server(host, port)

    #get_all_files(host, port, 'surfy')
    #upload_file(host, port, 'testproj', 'Gravatar.png')
    #upload_file(host, port, 'testproj', '/Users/hartleym/Dropbox/Tufte.pdf')
    #create_proj(host, port, 'newproj')

    #dsc = DserverClient(host, port)

    #dsc.delete_proj('testproj')

if __name__ == "__main__":
    main()
