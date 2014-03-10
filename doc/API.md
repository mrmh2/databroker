getall

## Client

getassoc - download associated data. Works by first retrieving URLs then grabbing them all.

## Server:

### Getting a single file

GET /img/project/filename

### Listing all files associated with project

GET /list/project

List files associates with project

### Upload a file for a project

POST /upload/project/filename

Add file to project

### Delete a project

POST /create/project