import requests

class TraktApiClient:
    def __init__(self, config):
        self.config = config

    def get(self, url: str):
        print("unimplemented: GET request to the trakt api")

    def post(self, url: str, data: any):
        print("POST request to the trakt api")
        result = requests.post(
            url,
            headers={
                "Content-Type": "application/json",
                'trakt-api-version': "2",
                'trakt-api-key': self.config.client_id,
                'Authorization': "Bearer %s" % self.config.access_token,
            },
            json=data,
       )
        print(data)
        return result.status_code, result.json() if result.status_code == 200 else result.text

    def delete(self):
        print("unimplemented: DELETE request to the trakt api")
