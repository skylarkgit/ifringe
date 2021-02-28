from filehandler import FileAPI
from dotenv import load_dotenv
import os
from flask import Flask, request, jsonify
from flask_restful import Resource, Api

# Environment Setup
load_dotenv(override=True)


# Flask Server
app = Flask('ifringe')
api = Api(app)
class FilesServer(Resource):
    fileAPI = FileAPI({
        'email': os.getenv('FILE_API_EMAIL')
    })

    def get(filename):
        return {'hello': 'world'}

    def post(self):
        print(1, __name__)
        self.fileAPI.store(request.files['image'])
        resp = jsonify({'message': 'File successfully uploaded'})
        resp.status_code = 201
        return resp

api.add_resource(FilesServer, '/')

# logs_db.insert_one({'event': 'start', 'on': time.time()})

print('started')

if __name__ == '__main__':
    app.run(threaded=True,host='0.0.0.0', port=5533)