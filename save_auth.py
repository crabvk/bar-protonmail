#!/usr/bin/env python

import argparse
import json
from pathlib import Path
from urllib.parse import unquote

parser = argparse.ArgumentParser(description='Saves your credentials from ProtonMail')
parser.add_argument('auth', help='AUTH-\u2026 cookie value')
args = parser.parse_args()

DIR = Path(__file__).resolve().parent
AUTH_PATH = Path(DIR, 'auth.json')

with open(AUTH_PATH, 'w') as f:
    auth = unquote(args.auth)
    try:
        creds = json.loads(auth)
        if 'UID' not in creds.keys() or 'AccessToken' not in creds.keys():
            print('Auth value has no required keys: UID and AccessToken')
            exit(2)
    except (json.decoder.JSONDecodeError, AttributeError):
        print('Invalid auth value format')
        exit(1)
    f.write(auth)
AUTH_PATH.chmod(0o600)
