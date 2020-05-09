import json
import argparse
from subprocess import Popen
from pathlib import Path

DIR = Path(__file__).resolve().parent
ICON_PATH = Path(DIR, 'icon.svg')

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--polybar', action='store_true', help='Print output in Polybar format instead of Waybar.')
parser.add_argument('-i', '--icon', default='\uf0e0')
parser.add_argument('-s', '--sound', help='Notification sound (event sound ID of canberra-gtk-play).')
parser.add_argument('-u', '--urgency', choices=['low', 'normal', 'critical'], help='Notification urgency level.')
parser.add_argument('-t', '--expire-time', type=int, help='Notification timeout in milliseconds.')
parser.add_argument('-n', '--max-notify', type=int, help='Limit number of notifications.')
args = parser.parse_args()


def puts(count, inaccurate=False):
    text = args.icon
    classes = set()
    if inaccurate:
        classes.add('inaccurate')
    if count > 0:
        text += f' {count}'
        classes.add('unread')
    if args.polybar:
        return print(text, flush=True)
    s = json.dumps({'text': text, 'class': list(classes)})
    print(s, flush=True)


def error(message):
    text = args.icon + ' ' + message
    if args.polybar:
        return print(text, flush=True)
    s = json.dumps({'text': text, 'class': 'error'})
    print(s, flush=True)


def notify(messages):
    if args.sound:
        Popen(['canberra-gtk-play', '-i', args.sound])
    for msg in messages[0:args.max_notify]:
        m = msg['Message']
        header = m.get('SenderName') or m.get('SenderAddress')
        body = m['Subject']
        app = ['-a', 'bar-protonmail']
        cat = ['-c', 'email.arrived']
        icon = ['-i', ICON_PATH]
        urgency = ['-u', args.urgency] if args.urgency else []
        expire = ['-t', args.expire_time] if args.expire_time else []
        Popen(['notify-send', *app, *cat, *icon, *urgency, *expire, header, body])
