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
Value of the first row with Name starting with `AUTH-` is your `AUTH` token,
and with Name starting with `REFRESH-` is your `REFRESH` data (including UID).  
Run `./save_auth.py AUTH REFRESH` to save your credentials.

**NOTE**: access token expires in 10 days (you'll see "Invalid access token" error). After that,
you'll need to get a new token the same way.

I tried to refresh expired `access token` with corresponding `refresh token`,
but always got 401 "Invalid refresh token". Maybe this is because only latest refresh token is valid.

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

See `./bar_protonmail.py -h` for list of arguments with description.  
Possible values for `-s`, `--sound`:
```shell
ls /usr/share/sounds/freedesktop/stereo/
```
without extension, for example `-s message-new-instant`.
