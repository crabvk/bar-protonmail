#!/usr/bin/env python

import json
from pathlib import Path
import output
from protonmail_api import Api, ApiRequestError, ApiResponseError

DIR = Path(__file__).resolve().parent
AUTH_PATH = Path(DIR, 'auth.json')

try:
    if not AUTH_PATH.is_file():
        output.error('auth.json not found')
        exit()

    with open(AUTH_PATH, 'r') as f:
        auth = json.load(f)

    api = Api(auth['UID'], auth['AccessToken'])
    session, unread = None, None
    SESSION_PATH = Path(DIR, 'session.json')
    if SESSION_PATH.is_file():
        with open(SESSION_PATH, 'r') as f:
            session = json.load(f)
            event_id = session['event_id']
            unread = session['unread']
    else:
        event_id = api.event_id()['EventID']

    resp = api.events(event_id)
    messages = resp.get('Messages', [])

    if messages:
        inbox = next(c for c in resp['MessageCounts'] if c['LabelID'] == '0')
        unread = inbox['Unread']

        unread_messages = list(filter(lambda m: m['Action'] == 1 and m['Message']['Unread'], messages))
        output.notify(unread_messages)

        event_id = api.event_id()['EventID']
    elif unread == None:
        resp = api.messages_count()
        inbox = next(c for c in resp['Counts'] if c['LabelID'] == '0')
        unread = inbox['Unread']

    output.puts(unread)

    if not session or session['unread'] != unread or messages:
        with open(SESSION_PATH, 'w') as f:
            json.dump({'event_id': event_id, 'unread': unread}, f, separators=(',', ':'))

    if not session:
        SESSION_PATH.chmod(0o600)

except ApiRequestError:
    output.puts(unread or 0, True)
except ApiResponseError as e:
    output.error(str(e))
