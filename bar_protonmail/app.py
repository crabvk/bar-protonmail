import os
import json
from enum import Enum
from pathlib import Path
from subprocess import Popen
from gi.repository import GLib
from dasbus.connection import SessionMessageBus
from dasbus.error import DBusError
from proton.exceptions import NetworkError, ProtonAPIError
from bar_protonmail.printer import WaybarPrinter, PolybarPrinter
from bar_protonmail.protonmail import ProtonMail

APP_NAME = 'Bar ProtonMail'
NOTIFICATION_CATEGORY = 'email.arrived'
BASE_DIR = Path(__file__).resolve().parent
PROTONMAIL_ICON_PATH = Path(BASE_DIR, 'icon.svg')


class UrgencyLevel(Enum):
    LOW = 0
    NORMAL = 1
    CRITICAL = 2


class Application:
    def __init__(self, unread_path: Path, protonmail: ProtonMail,
                 printer: WaybarPrinter | PolybarPrinter, sound_id: str,
                 urgency_level: UrgencyLevel, expire_timeout: int, is_notify: bool):
        self.unread_path = unread_path
        self.protonmail = protonmail
        self.printer = printer
        self.sound_id = sound_id
        self.urgency_level = urgency_level
        self.expire_timeout = expire_timeout
        self.is_notify = is_notify

    @staticmethod
    def _message_to_notification(message):
        m = message['Message']
        return {
            'title': m.get('SenderName') or m.get('SenderAddress'),
            'body': m['Subject']
        }

    def _play_sound(self):
        try:
            Popen(['canberra-gtk-play', '-i', self.sound_id], stderr=open(os.devnull, 'wb'))
        except FileNotFoundError:
            pass

    def _send_notifications(self, messages):
        try:
            bus = SessionMessageBus()
            proxy = bus.get_proxy(
                'org.freedesktop.Notifications',
                '/org/freedesktop/Notifications'
            )

            app_icon = str(PROTONMAIL_ICON_PATH)
            replaces_id = 0
            actions = []

            # https://lazka.github.io/pgi-docs/GLib-2.0/classes/VariantType.html#GLib.VariantType
            hints = {
                'category': GLib.Variant('s', NOTIFICATION_CATEGORY),
                'urgency': GLib.Variant('y', self.urgency_level.value),
            }

            for message in messages:
                summary = message['title']
                body = message['body']

                # https://specifications.freedesktop.org/notification-spec/notification-spec-latest.html
                proxy.Notify(APP_NAME, replaces_id, app_icon, summary,
                             body, actions, hints, self.expire_timeout)
        except DBusError:
            pass

    def run(self):
        try:
            if self.unread_path.is_file():
                with open(self.unread_path, 'r') as f:
                    data = json.load(f)
                    unread_prev = data['Unread']
                    event_id = data['EventID']
            else:
                unread_prev = None
                latest = self.protonmail.get_latest_event()
                event_id = latest['EventID']

            events = self.protonmail.get_events(event_id)
            event_id = events['EventID']
            messages = events.get('Messages', [])

            if messages:
                new_messages = filter(
                    lambda m: m['Action'] == 1 and m['Message']['Unread'], messages)
                new_messages = list(map(self._message_to_notification, new_messages))
                if len(new_messages) > 0:
                    if self.sound_id:
                        self._play_sound()
                    if self.is_notify:
                        self._send_notifications(new_messages)

            unread = self.protonmail.get_unread()
            self.printer.print(unread)

            if unread_prev != unread or messages:
                with open(self.unread_path, 'w') as f:
                    json.dump({'EventID': event_id, 'Unread': unread}, f)

        except NetworkError:
            self.printer.print(unread_prev or 0, inaccurate=True)

        except ProtonAPIError as e:
            # Code 401: Invalid access token.
            if e.code == 401:
                is_success, error = self.protonmail.refresh_tokens()
                if is_success:
                    self.run()
                else:
                    self.printer.error(str(error))
            else:
                self.printer.error(str(e))
