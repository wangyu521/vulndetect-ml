#!/usr/bin/env python3
from flask import request
from flask_cors import CORS
from predictor import AppWithOptionalPredictor

model_path = '../../save_temp.h5'
encoder_path = '../../train_encoder.subwords'

app = AppWithOptionalPredictor(__name__)
CORS(app)

STATUS_CODES = {
    200: '200 OK',
    201: '201 Created',
    400: '400 Bad Request',
    404: '404 Not Found',
    500: '500 Internal Server Error',
}


class APIResponse(object):
    def __init__(self):
        self._statusCode: str = None
        self._message: str = None
    
    @property
    def statusCode(self):
        return self._statusCode
    
    @statusCode.setter
    def statusCode(self, value: int):
        if value in STATUS_CODES:
            self._statusCode = STATUS_CODES[value]
        else:
            self._statusCode = '501 Not Implemented'

    def with_statusCode(self, value: int):
        self.statusCode = value
        return self

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, value: str):
        self._message = str(value)

    def with_message(self, value: str):
        self.message = value
        return self
    
    def build(self):
        return {
            'status': self.statusCode,
            'message': self.message
        }


@app.route('/api/heartbeat', methods=['GET'])
def heartbeat():
    return APIResponse().with_message('Heartbeat').with_statusCode(200).build()


@app.route('/api/predict', methods=['POST'])
def predict():
    code_text = request.form.get('file', None)

    retr_str = 'Got '
    if 'file' not in request.files:
        print('No files uploaded')
        retr_str += code_text
    else:
        file = request.files['file']
        print(file.name)
        file.seek(0)
        file_data = file.read().decode('utf-8')
        retr_str += 'file with data %s' % str(file_data)

    return APIResponse().with_message(retr_str).with_statusCode(200).build()
