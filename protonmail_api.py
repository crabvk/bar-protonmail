import requests


class ApiRequestError(Exception):
    def __init__(self, message, error=None):
        super().__init__(message)
        self.error = error


class ApiResponseError(Exception):
    def __init__(self, message, error=None):
        super().__init__(message)
        self.error = error


class Api:
    def __init__(self, uid, access_token):
        self.host = 'https://api.protonmail.ch'
        self.headers = {
            'Authorization': 'Bearer ' + access_token,
            'x-pm-uid': uid,
            'x-pm-appversion': 'Web_4.0.0-beta.20'
        }

    def event_id(self):
        return self._request('/events/latest')

    def events(self, event_id):
        return self._request('/events/' + event_id)

    def messages_count(self):
        return self._request('/messages/count')

    def _request(self, path, **kwards):
        resp = None
        try:
            resp = requests.get(self.host + path, headers=self.headers, timeout=10, **kwards)
        except requests.exceptions.RequestException as e:
            import re
            words = re.findall('[A-Z][^A-Z]*', e.__class__.__name__)
            raise ApiRequestError(' '.join(words).capitalize(), e)

        json = resp.json()
        if not resp.ok or json['Code'] != 1000:
            raise ApiResponseError(json['Error'], json)
        return json
