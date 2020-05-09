# New message notifications and unread messages count from ProtonMail

## Dependencies

* python-requests
* libnotify
* ttf-font-awesome
* libcanberra (optional, notification sound)

## Install

**NOTE**: replace `waybar` with `polybar` if use Polybar.

```sh
cd ~/.config/waybar
curl -LO https://github.com/vyachkonovalov/bar-protonmail/archive/master.tar.gz
tar -zxf master.tar.gz && rm master.tar.gz
mv bar-protonmail-master bar-protonmail
```

**NOTE**: instructions may differ depending on your browser.

In Firefox go to your [ProtonMail inbox](https://mail.protonmail.com/inbox).  
Open DevTools -> Storage (`Shift`+`F9`) -> Cookies.  
Sort by last column, newer to older (`Last Accessed ⯆`).  
For the first row name starting with `AUTH-` copy it's value (double-click and `Ctrl`+`C`).  
Run `./save_auth.py VALUE`.

## Waybar config

~/.config/waybar/config
```json
"modules-right": {
  "custom/protonmail"
}
...
"custom/protonmail": {
    "exec": "$HOME/.config/waybar/bar-protonmail/bar_protonmail.py",
    "return-type": "json",
    "interval": 10,
    "tooltip": false,
    "on-click": "xdg-open https://mail.protonmail.com/inbox"
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

## Polybar config

```ini
modules-right = protonmail
...
[module/protonmail]
type = custom/script
exec = ~/.config/polybar/bar-protonmail/bar_protonmail.py -p
interval = 10
click-left = xdg-open https://mail.protonmail.com/inbox
```

## Script arguments

See `python output.py -h` for list of arguments with description.  
Possible values for `-s`, `--sound`:
```shell
ls /usr/share/sounds/freedesktop/stereo/
```
without extension, for example `-s message-new-instant`.
