# New message notifications and unread messages count from ProtonMail (Waybar/Polybar module)

## Dependencies

* proton-client >= 0.7.1 ([not available on pypi.org](https://github.com/ProtonMail/proton-python-client/issues/36))
* ttf-font-awesome (default badge: )
* libnotify (new email notifications, can be disabled with `-dn` flag)
* libcanberra (optional, notification sound)

To display notifications you must have a [notification daemon](https://wiki.archlinux.org/title/Desktop_notifications#Notification_servers) running on your system.

## Install

### ArchLinux and derivatives

[AUR package](https://aur.archlinux.org/packages/bar-protonmail/)

### Other distros

```sh
git clone https://github.com/crabvk/bar-protonmail.git
# WARN: Checkout to the latest tag, don't use master branch.
pip install -e .
```

And now you can execute *~/.local/bin/bar-protonmail*

## Use

First, you need to authenticate the client:

```sh
bar-protonmail auth
```

then just run `bar-protonmail` or `bar-protonmail -f polybar`.
Session, cache and log are stored in ~/.cache/bar-protonmail.

## Waybar config example

~/.config/waybar/config
```json
"modules-right": {
    "custom/protonmail"
}

"custom/protonmail": {
    "exec": "bar-protonmail",
    "return-type": "json",
    "interval": 10,
    "tooltip": false,
    "on-click": "xdg-open https://mail.proton.me/u/0/inbox"
}
```
~/.config/waybar/style.css
```css
#custom-protonmail.unread {
    color: white;
}
#custom-protonmail.inaccurate {
    color: darkorange;
}
#custom-protonmail.error {
    color: darkred;
}
```

## Polybar config example

```ini
modules-right = protonmail
...
[module/protonmail]
type = custom/script
exec = bar-protonmail -f polybar
interval = 10
click-left = xdg-open https://mail.proton.me/u/0/inbox
```

## Script arguments

See `bar-protonmail -h` for the list of arguments with descriptions.  
Possible values for `-s`, `--sound` can be found with:
```shell
ls /usr/share/sounds/freedesktop/stereo/ | cut -d. -f1
```
for example `-s message-new-instant`.
