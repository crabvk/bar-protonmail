#!/usr/bin/env python

import sys
from pathlib import Path
from urllib.parse import unquote

DIR = Path(__file__).resolve().parent
AUTH_PATH = Path(DIR, 'auth.json')

with open(AUTH_PATH, 'w') as f:
    f.write(unquote(sys.argv[1]))
AUTH_PATH.chmod(0o600)
