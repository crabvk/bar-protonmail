import json
import getpass
from pathlib import Path
from proton.api import Session
from proton.exceptions import NetworkError, ProtonAPIError


class ProtonMail:
    def __init__(self, cache_dir: Path, session_path: Path, proxies: list[[str, str]] | None):
        self.cache_dir = cache_dir
        self.session_path = session_path
        self._session = None
        if proxies:
            self.proxies = dict(proxies)
        else:
            self.proxies = None

    @property
    def session(self):
        if self._session is None:
            with open(self.session_path, 'r') as f:
                session_dump = json.loads(f.read())

            self._session = Session.load(
                dump=session_dump,
                log_dir_path=self.cache_dir,
                cache_dir_path=self.cache_dir,
                tls_pinning=not self.proxies,
                proxies=self.proxies
            )
            self._session.enable_alternative_routing = True
        return self._session

    def authenticate(self):
        session = Session(
            api_url='https://api.protonmail.ch',
            log_dir_path=self.cache_dir,
            cache_dir_path=self.cache_dir,
            tls_pinning=not self.proxies,
            proxies=self.proxies
        )
        session.enable_alternative_routing = True

        username = input('Username: ')
        password = getpass.getpass()
        scope = session.authenticate(username, password)

        if 'twofactor' in scope:
            code = input('Two-factor auth: ')
            session.provide_2fa(code)

        with open(self.session_path, 'w') as f:
            json.dump(session.dump(), f)

    def get_unread(self):
        resp = self.session.api_request('/messages/count')
        inbox = next(c for c in resp['Counts'] if c['LabelID'] == '0')
        return inbox['Unread']

    def get_latest_event(self):
        return self.session.api_request('/events/latest')

    def get_events(self, event_id: str):
        return self.session.api_request('/events/' + event_id)

    def refresh_tokens(self):
        try:
            self.session.refresh()
            with open(self.session_path, 'w') as f:
                json.dump(self.session.dump(), f)
            return (True, None)
        except (NetworkError, ProtonAPIError) as error:
            return (False, error)
