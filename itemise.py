"""itemise.py

Read directory structure and construct data structure to pass to server"""

import os
from pprint import pprint

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

def itemise_file(filename):
    filetype = 'png'
    return { 'name' : filename,
             'type' : filetype }

def itemise_dir(full_path):
    return [itemise_file(f) for f in os.listdir(full_path)]

def itemise(root_path):
    return {project : itemise_dir(os.path.join(root_path, project))
           for project in os.listdir(root_path)}

def main():
    pprint(all_projects)
    pprint(itemise('img'))

if __name__ == '__main__':
    main()
