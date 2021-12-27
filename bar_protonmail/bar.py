from proton.api import Session
from proton.exceptions import NetworkError, ProtonAPIError
from pathlib import Path
import json


class Bar:
    def __init__(self, cache_dir, session_path, unread_path, output):
        self.cache_dir = cache_dir
        self.session_path = session_path
        self.unread_path = unread_path
        self.output = output
        self._load_session()
        self._load_unread()

    @staticmethod
    def _message_to_notification(message):
        m = message['Message']
        return {
            'title': m.get('SenderName') or m.get('SenderAddress'),
            'body': m['Subject']
        }

    def _load_session(self):
        with open(self.session_path, 'r') as f:
            session_dump = json.loads(f.read())

        self.session = Session.load(
            dump=session_dump,
            log_dir_path=self.cache_dir,
            cache_dir_path=self.cache_dir
        )
        self.session.enable_alternative_routing = True

    def _load_unread(self):
        if self.unread_path.is_file():
            with open(self.unread_path, 'r') as f:
                self.unread_obj = json.load(f)
                self.unread = self.unread_obj['Unread']
                self.event_id = self.unread_obj['EventID']
        else:
            self.unread_obj = None
            self.unread = None
            self.event_id = None

    def get_unread(self):
        resp = self.session.api_request('/messages/count')
        inbox = next(c for c in resp['Counts'] if c['LabelID'] == '0')
        return inbox['Unread']

    def refresh_tokens(self):
        try:
            self.session.refresh()
            with open(self.session_path, 'w') as f:
                json.dump(self.session.dump(), f)
            return True
        except (NetworkError, ProtonAPIError) as e:
            self.output.error(str(e))

    def check(self):
        try:
            if not self.event_id:
                latest = self.session.api_request('/events/latest')
                self.event_id = latest['EventID']

            events = self.session.api_request('/events/' + self.event_id)
            messages = events.get('Messages', [])

            if messages:
                new_messages = filter(lambda m: m['Action'] ==
                                      1 and m['Message']['Unread'], messages)
                new_messages = list(map(self._message_to_notification, new_messages))
                self.event_id = events['EventID']
                self.output.notify(new_messages)

            self.unread = self.get_unread()
            self.output.info(self.unread)

            if not self.unread_obj or self.unread_obj['Unread'] != self.unread or messages:
                with open(self.unread_path, 'w') as f:
                    json.dump({'EventID': self.event_id, 'Unread': self.unread}, f)

        except NetworkError:
            self.output.info(self.unread or 0, inaccurate=True)

        except ProtonAPIError as e:
            # Code 401: Invalid access token
            if e.code == 401:
                if self.refresh_tokens():
                    self.check()
            else:
                self.output.error(str(e))
