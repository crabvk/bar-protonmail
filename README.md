# New message notifications and unread messages count from ProtonMail (Waybar/Polybar module)

## Dependencies

* proton-client >= 0.7.1
* libnotify
* ttf-font-awesome (default badge )
* libcanberra (optional, notification sound)

## Install

```sh
pip install bar-protonmail
```

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
    "on-click": "xdg-open https://mail.protonmail.com/u/0/inbox"
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
click-left = xdg-open https://mail.protonmail.com/u/0/inbox
```

## Script arguments

See `bar-protonmail -h` for the list of arguments with descriptions.  
Possible values for `-s`, `--sound` can be found with:
```shell
ls /usr/share/sounds/freedesktop/stereo/
```
without extension, for example `-s message-new-instant`.
