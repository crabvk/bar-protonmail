from proton.api import Session
import json
import getpass


def authenticate(cache_dir, session_path):
    session = Session(
        api_url='https://api.protonmail.ch',
        log_dir_path=cache_dir,
        cache_dir_path=cache_dir
    )
    session.enable_alternative_routing = True

    username = input('Username: ')
    password = getpass.getpass()

    scope = session.authenticate(username, password)

    if 'twofactor' in scope:
        code = input('Two-factor auth: ')
        session.provide_2fa(code)

    with open(session_path, 'w') as f:
        json.dump(session.dump(), f)
