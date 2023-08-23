import requests


class API:
    @staticmethod
    def get_request(url):
        resp = requests.get(url)
        try:
            return resp.json()
        except:
            raise Exception('Json cannot be returned')
