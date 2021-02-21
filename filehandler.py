import requests
from pymongo import MongoClient, DESCENDING
import hashlib

import os
from werkzeug.utils import secure_filename


class FileAPI:

    client = MongoClient(os.getenv('APP_DB_URL'))
    files_db = client.ifringe.files
    # files_db.create_index(
    #     [("hash", DESCENDING)],
    #     unique=True
    # )

    def __init__(self, creds) -> None:
        response = requests.get('https://apiv2.gofile.io/getServer')
        self.server = response.json()['data']['server']
        self.creds = creds

    def store(self, file, name=None):
        if name == None:
            name = file.filename
        file_hash = hashlib.sha256()
        file_hash.update(file.read())
        hashed_file_name = file_hash.hexdigest()
        pre_saved = self.files_db.find_one({'hash': hashed_file_name})
        if pre_saved == None:
            filename = secure_filename(file.filename)
            files = {
                'email': (None, self.creds.email),
                'file': (name, file),
            }
            response = requests.post('https://{self.server}.gofile.io/uploadFile', files=files)
            fileKey = response['data']['code']
            fileLocation = 'https://gofile.io/d/{fileKey}'
            print('saved file to', fileLocation)
            self.files_db.insert_one({'hash': hashed_file_name, 'fileKey': fileKey, 'name': filename, 'status': 'uploaded'})
            print('Processing', fileLocation)
            # asyncio.create_task(splitter(hashed_file_name, fileLocation))
            print('created task for', fileLocation)
            # splitter.delay(hashed_file_name, fileLocation)

    def __del__(self):
        self.client.close()
