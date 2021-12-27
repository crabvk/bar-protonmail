from subprocess import Popen
from pathlib import Path
from enum import Enum
import json

BASE_DIR = Path(__file__).resolve().parent
ICON_PATH = Path(BASE_DIR, 'icon.svg')


class OutputFormat(Enum):
    WAYBAR = 'waybar'
    POLYBAR = 'polybar'


class UrgencyLevel(Enum):
    LOW = 'low'
    NORMAL = 'normal'
    CRITICAL = 'critical'


class Output:
    def __init__(self, format: OutputFormat, badge='', sound=None,
                 urgency=UrgencyLevel.NORMAL, expire_millisecs=None):
        self.format = format
        self.badge = badge
        self.sound = sound
        self.urgency = urgency
        self.expire = expire_millisecs

    def _puts(self, text):
        try:
            print(text, flush=True)
        except BrokenPipeError:
            pass

    def info(self, count, inaccurate=False):
        text = self.badge
        classes = set()
        if inaccurate:
            classes.add('inaccurate')
        if count > 0:
            text += f' {count}'
            classes.add('unread')
        if self.format == OutputFormat.POLYBAR:
            return self._puts(text)
        s = json.dumps({'text': text, 'class': list(classes)})
        self._puts(s)

    def error(self, message):
        text = self.badge + ' ' + message
        if self.format == OutputFormat.POLYBAR:
            return self._puts(text)
        s = json.dumps({'text': text, 'class': 'error'})
        self._puts(s)

    def notify(self, notifications):
        if self.sound:
            Popen(['canberra-gtk-play', '-i', self.sound])

        for n in notifications:
            app = ['-a', 'bar-protonmail']
            cat = ['-c', 'email.arrived']
            icon = ['-i', ICON_PATH]
            urgency = ['-u', self.urgency.value] if self.urgency else []
            expire = ['-t', self.expire] if self.expire else []
            Popen(['notify-send', *app, *cat, *icon, *urgency, *expire, n['title'], n['body']])
