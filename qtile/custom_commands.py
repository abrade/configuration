import os as _os

i3_exit_cmd = _os.path.expanduser('~/bin/i3exit')
browser = 'vivaldi'
dmenu = 'dmenu_run -i -b -p ">>>" -nb "#15181a" -nf "#fff" -sb "#333" -sf "#fff"'
file_manager = 'thunar'
lock_screen = _os.path.expanduser('~/bin/i3_lock')
suspend = i3_exit_cmd + " suspend"
poweroff = i3_exit_cmd + " shutdown"
reboot = i3_exit_cmd + " reboot"
screenshot = 'shutter -f'
terminal = 'xfce4-terminal'
trackpad_toggle = "synclient TouchpadOff=$(synclient -l | grep -c 'TouchpadOff.*=.*0')"
volume_up = 'amixer -q -c 1 sset Master 5dB+'
volume_down = 'amixer -q -c 1 sset Master 5dB-'
volume_toggle = 'amixer -q -D pulse sset Master 1+ toggle'
spotify = {
    'play': 'dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.PlayPause',
    'pause': 'dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Pause',
    'next': 'dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Next',
    'prev': 'dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Previous',
}
