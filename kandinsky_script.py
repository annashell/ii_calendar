import requests
import json
import time
import base64
from dotenv import dotenv_values

URL = "https://api-key.fusionbrain.ai/"
config = dotenv_values(".env")
api_key = config.get('API_KEY')
secret_key = config.get('SECRET_KEY')


class KandinskyRequest:
    def __init__(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    def get_pipeline(self):
        response = requests.get(self.URL + 'key/api/v1/pipelines', headers=self.AUTH_HEADERS)
        data = response.json()
        return data[0]['id']

    def generate(self, prompt, pipeline, style="DEFAULT", images=1, width=1024, height=1024):
        params = {
            "type": "GENERATE",
            "style": style,
            "numImages": images,
            "width": width,
            "height": height,
            "generateParams": {
                "query": f'{prompt}'
            }
        }

        data = {
            'pipeline_id': (None, pipeline),
            'params': (None, json.dumps(params), 'application/json')
        }
        response = requests.post(self.URL + 'key/api/v1/pipeline/run', headers=self.AUTH_HEADERS, files=data)
        data = response.json()
        return data['uuid']

    def check_generation(self, request_id, attempts=10, delay=10):
        while attempts > 0:
            response = requests.get(self.URL + 'key/api/v1/pipeline/status/' + request_id, headers=self.AUTH_HEADERS)
            data = response.json()
            if data['status'] == 'DONE':
                return data['result']['files']

            attempts -= 1
            time.sleep(delay)


def get_pic_for_today(req):
    kr = KandinskyRequest(URL, api_key, secret_key)
    pipeline_id = kr.get_pipeline()
    uuid = kr.generate(req, pipeline_id)
    files = kr.check_generation(uuid)
    image_data = base64.b64decode(files[0])
    return image_data
