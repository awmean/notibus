# the idea

main reason of inventing this is to be able to send desktop notifications from ROOT (e.g. system-wide daemon).

the case was: do some log processing things with syslog-ng and in some cases notify specific user(s) about what
happened.

the problem was: i could not find any native solution for that ;)

# usage

start `notibus.py` in your session. the easiest way is to put it in `/etc/xdg/autostart` (`notibus.desktop` is coming)

to send the notification you can use:

- `notibus-send.py` script; `--help` is available
- raw d-bus usage; see usage in `example.sh`, that should be enough
