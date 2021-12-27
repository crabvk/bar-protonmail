#!/usr/bin/env python

from pathlib import Path
from bar_protonmail.output import Output, OutputFormat, UrgencyLevel
from bar_protonmail.bar import Bar
from bar_protonmail import auth
import argparse


def cli():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='subcommand')
    subparsers.add_parser('auth', help='Authentication.')
    parser.add_argument('-f', '--format', choices=['waybar', 'polybar'], default='waybar',
                        help='Print output in specified format [default: waybar].')
    parser.add_argument('-b', '--badge', default='',
                        help='Badge to display in the bar [default: ].')
    parser.add_argument('-s', '--sound',
                        help='Notification sound (event sound ID from canberra-gtk-play).')
    parser.add_argument('-u', '--urgency', choices=['low', 'normal', 'critical'],
                        default='normal', help='Notification urgency level [default: normal].')
    parser.add_argument('-t', '--expire-time', type=int,
                        help='Notification timeout in milliseconds.')
    args = parser.parse_args()

    CACHE_DIR = Path(Path.home(), '.cache/bar-protonmail')
    SESSION_PATH = Path(CACHE_DIR, 'session.json')
    UNREAD_PATH = Path(CACHE_DIR, 'unread.json')

    if not CACHE_DIR.is_dir():
        CACHE_DIR.mkdir(exist_ok=True)

    if args.subcommand == 'auth':
        auth.authenticate(CACHE_DIR, SESSION_PATH)
        print('Session saved successfully.')
        exit()

    output = Output(format=OutputFormat(args.format), badge=args.badge, sound=args.sound,
                    urgency=UrgencyLevel(args.urgency), expire_millisecs=args.expire_time)

    if not SESSION_PATH.is_file():
        output.error('session.json not found')
        exit()

    bar = Bar(CACHE_DIR, SESSION_PATH, UNREAD_PATH, output)
    bar.check()


if __name__ == '__main__':
    cli()
