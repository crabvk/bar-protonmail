import sys
import argparse
from pathlib import Path
from bar_protonmail.app import Application, UrgencyLevel
from bar_protonmail.printer import WaybarPrinter, PolybarPrinter
from bar_protonmail.protonmail import ProtonMail


def cli():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='subcommand')
    subparsers.add_parser('auth', help='Authentication.')
    parser.add_argument('-f', '--format', choices=['waybar', 'polybar'], default='waybar',
                        help='Print output in specified format [default: waybar].')
    parser.add_argument('-b', '--badge', default='',
                        help='Badge to display in the bar [default: ].')
    parser.add_argument('-c', '--color',
                        help='Text foreground color (only for Polybar).')
    parser.add_argument('-s', '--sound',
                        help='Notification sound (event sound ID from canberra-gtk-play).')
    parser.add_argument('-u', '--urgency', choices=['low', 'normal', 'critical'],
                        default='normal', help='Notification urgency level [default: normal].')
    parser.add_argument('-t', '--expire-timeout', type=int, default=0,
                        help='The duration, in milliseconds, for the notification to appear on screen.')
    parser.add_argument('-dn', '--no-notify', action='store_true',
                        help='Disable new email notifications.')
    parser.add_argument('-p', '--proxy', action='append', nargs=2, metavar=('PROTOCOL', 'URL'),
                        help='Protocol and URL of the proxy (e.g. "https socks5://user:password@host:port").')
    args = parser.parse_args()

    if args.color is not None and args.format != 'polybar':
        parser.error(
            '`--color COLOR` can be used only with `--format polybar`.')

    cache_dir = Path(Path.home(), '.cache/bar-protonmail')
    session_path = Path(cache_dir, 'session.json')
    unread_path = Path(cache_dir, 'unread.json')

    if not cache_dir.is_dir():
        cache_dir.mkdir(exist_ok=True)

    protonmail = ProtonMail(cache_dir, session_path, proxies=args.proxy)

    if args.subcommand == 'auth':
        protonmail.authenticate()
        print('Session saved successfully.')
        sys.exit()

    if args.format == 'waybar':
        printer = WaybarPrinter(badge=args.badge)
    elif args.format == 'polybar':
        printer = PolybarPrinter(badge=args.badge, color=args.color)

    if not session_path.is_file():
        printer.error('Authentication required')
        sys.exit()

    app = Application(unread_path, protonmail, printer,
                      sound_id=args.sound,
                      urgency_level=UrgencyLevel[args.urgency.upper()],
                      expire_timeout=args.expire_timeout,
                      is_notify=not args.no_notify)
    app.run()


if __name__ == '__main__':
    cli()
