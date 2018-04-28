import requests

REQUEST_URL_FORMAT = 'https://vision.googleapis.com/v1/{}?key={}'


class VisionApi:
    def __init__(self, api_key):
        self.api_key = api_key

    def post(self, method, data):
        endpoint = REQUEST_URL_FORMAT.format(method, self.api_key)
        return requests.post(endpoint, json=data).json()

    def get_text_from_image_uri(self, image_uri):
        data = {'requests': [{'image': {'source': {'imageUri': image_uri}}, 
                    'features': {'type': 'DOCUMENT_TEXT_DETECTION'}}]}
        response = self.post('images:annotate', data)
        return ''.join([t['description'] for t in response['responses'][0]['textAnnotations']])
