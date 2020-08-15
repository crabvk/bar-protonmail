#!/usr/bin/env python

import argparse
import json
from pathlib import Path
from urllib.parse import unquote

parser = argparse.ArgumentParser(description='Saves your credentials from ProtonMail')
parser.add_argument('auth', help='AUTH token')
parser.add_argument('refresh', help='REFRESH data')
args = parser.parse_args()

DIR = Path(__file__).resolve().parent
AUTH_PATH = Path(DIR, 'auth.json')

try:
    creds = json.loads(unquote(args.refresh))
    if 'UID' not in creds.keys():
        print('Refresh data has no required key UID')
        exit(2)
    auth = json.dumps({'UID': creds['UID'], 'AccessToken': args.auth})
    with open(AUTH_PATH, 'w') as f:
        f.write(auth)
    AUTH_PATH.chmod(0o600)
except (json.decoder.JSONDecodeError, AttributeError):
    print('Invalid refresh data format')
    exit(1)
