#!/usr/bin/env python
# -*- coding: utf-8 -*-

from libqtile import bar, hook, layout, widget
from libqtile.command import lazy
from libqtile.config import Drag, Group, Key, Match, Screen

import weather as _weather
import thunderbird as _thunderbird
import khalwidget as _khalwidget
import custom_commands as _commands

import subprocess, re
import os
DETACHED_PROCESS = 0x00000008

def is_running(process):
    s = subprocess.Popen(["ps", "axw"], stdout=subprocess.PIPE)
    for x in s.stdout:
        if re.search(process, x):
            return True
        return False

def execute_once(process):
    if not is_running(process):
        return subprocess.call(process.split())

@hook.subscribe.startup_once
def startup():
    home = os.path.expanduser('~/bin/start_apps')
    subprocess.call([home])

# Theme defaults
bar_defaults = dict(
    size=28,
    background=['#222222', '#111111'],
)

bottom_bar_defaults = dict(
    size=15,
    background=bar_defaults['background'],
)

layout_defaults = dict(
    border_width=1,
    margin=0,
    border_focus='#336699',
    border_normal='#333333',
    font='Source Code Pro',
    fontsize=9,
)

widget_defaults = dict(
    font='Source Code Pro',
    fontsize=14,
    padding=5,
    background=bar_defaults['background'],
    foreground=['#ffffff', '#ffffff', '#999999'],
    fontshadow='#000000',
)


class Widget(object):
    ''' Container for individual widget style options '''

    graph = dict(
        background='#000000',
        border_width=0,
        border_color='#000000',
        line_width=1,
        margin_x=0,
        margin_y=0,
        width=50,
    )

    notify_layout = dict(
        configured_keyboards=['us', 'de'],
        font='Source Code Pro',
        fontsize=12,
        padding=5,
        background=bar_defaults['background'],
        foreground=['#ffffff', '#ffffff', '#999999'],
        fontshadow='#000000',
    )

    keyboard_layout = dict(
        configured_keyboards=['us', 'de'],
        font='Source Code Pro',
        fontsize=14,
        padding=5,
        background=bar_defaults['background'],
        foreground=['#ffffff', '#ffffff', '#999999'],
        fontshadow='#000000',
    )

    groupbox = dict(
        active=widget_defaults['foreground'],
        inactive=['#444444', '#333333'],

        this_screen_border=layout_defaults['border_focus'],
        this_current_screen_border=layout_defaults['border_focus'],
        other_screen_border='#444444',

        urgent_text=widget_defaults['foreground'],
        urgent_border='#ff0000',

        highlight_method='block',
        rounded=True,

        # margin=-1,
        padding=3,
        borderwidth=2,
        disable_drag=True,
        invert_mouse_wheel=True,
    )

    sep = dict(
        foreground=layout_defaults['border_normal'],
        height_percent=100,
        padding=5,
    )

    systray = dict(
        icon_size=16,
        padding=5,
    )

    battery = dict(
       energy_now_file='charge_now',
       energy_full_file='charge_full',
       power_now_file='current_now',
    )

    battery_text = battery.copy()
    battery_text.update(
        charge_char='',  # fa-arrow-up
        discharge_char='',  # fa-arrow-down
        format='{char} {hour:d}:{min:02d}',
    )

    weather = dict(
        # woeid=642302,
#        location="Buehlertal, Germany",
        location_code='GMXX2902:1:GM',
        update_interval=60,
        metric=True,
        colorize=True,
        # format='{condition_text} {condition_temp}°',
    )


# Keybindings
mod = 'mod4'
keys = [
    # Window Manager Controls
    Key([mod, 'control'], 'r', lazy.restart()),
    Key([mod, 'control'], 'q', lazy.shutdown()),
    Key([mod, 'control'], 'l', lazy.spawn(_commands.lock_screen)),
    Key([mod, 'control'], 'k', lazy.spawn(_commands.suspend)),
    Key([mod, 'control'], 'j', lazy.spawn(_commands.poweroff)),
    Key([mod, 'control'], 'h', lazy.spawn(_commands.reboot)),

    # Window Controls
    Key([mod], 'w', lazy.window.kill()),
    Key([mod], 'f', lazy.window.toggle_floating()),
    Key([mod, 'shift'], 'f', lazy.window.toggle_fullscreen()),

    # Layout, group, and screen modifiers
    Key([mod], 'j', lazy.layout.up()),
    Key([mod], 'k', lazy.layout.down()),
    # Key([mod, 'shift'], 'j', lazy.layout.shuffle_up()),
    # Key([mod, 'shift'], 'k', lazy.layout.shuffle_down()),
    Key([mod, 'shift'], 'g', lazy.layout.grow()),
    Key([mod, 'shift'], 's', lazy.layout.shrink()),
    Key([mod, 'shift'], 'n', lazy.layout.normalize()),
    Key([mod, 'shift'], 'm', lazy.layout.maximize()),

    Key([mod, "shift"], "h", lazy.layout.swap_left()),
    Key([mod, "shift"], "l", lazy.layout.swap_right()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),

    Key([mod, 'shift'], 'space', lazy.layout.flip()),
    Key([mod, 'control'], 'space', lazy.layout.rotate()),

    # Switch groups
    Key([mod], 'Left', lazy.screen.prevgroup()),
    Key([mod], 'Right', lazy.screen.nextgroup()),

    # Cycle layouts
    Key([mod], 'Up', lazy.nextlayout()),
    Key([mod], 'Down', lazy.prevlayout()),

    # Change window focus
    Key([mod], 'Tab', lazy.layout.next()),
    Key([mod, 'shift'], 'Tab', lazy.layout.previous()),

    # Switch focus to other screens
    Key([mod], 'h', lazy.to_screen(0)),  # left
    Key([mod], 'l', lazy.to_screen(1)),  # right

    # Commands: Application Launchers
    Key([mod], 'space', lazy.spawn(_commands.dmenu)),
    Key([mod], 'n', lazy.spawn(_commands.browser)),
    Key([mod], 'e', lazy.spawn(_commands.file_manager)),
    Key([mod], 'Return', lazy.spawn(_commands.terminal)),

    # Commands: Volume Controls
    Key([], 'XF86AudioRaiseVolume', lazy.spawn(_commands.volume_up)),
    Key([], 'XF86AudioLowerVolume', lazy.spawn(_commands.volume_down)),
    Key([], 'XF86AudioMute', lazy.spawn(_commands.volume_toggle)),
    Key([mod, 'shift'], 'Left', lazy.spawn(_commands.spotify['prev'])),
    Key([mod, 'shift'], 'Right', lazy.spawn(_commands.spotify['next'])),
    Key([mod, 'shift'], 'Up', lazy.spawn(_commands.spotify['pause'])),
    Key([mod, 'shift'], 'Down', lazy.spawn(_commands.spotify['play'])),

    Key([], 'XF86TouchpadToggle', lazy.spawn(_commands.trackpad_toggle)),

    # TODO: What does the PrtSc button map to?
    Key([mod], 'p', lazy.spawn(_commands.screenshot)),
]


# Groups
group_setup = (
    ('', {  # fa-globe
        'layout': 'max',
        'matches': [Match(wm_class=('Firefox', 'Google-chrome', "google-chrome", "google-chrome", "vivaldi-stable",))],
    }),
    ('', {  # fa-code
        'layout': 'max',
        'matches': [Match(wm_class=('Emacs', 'emacs',))],
    }),
    ('', { # fa-terminal
        'layout': 'monadtall',
        'matches': [Match(wm_class=('xfce4-terminal', 'Xfce4-terminal', 'tmux',))],
    }),
    ('', {'layout': 'monadtall'}),
    ('', {  # fa-book
        'layout': 'max',
        'matches': [Match(wm_class=('VirtualBox',))],
    }),
    ('', {  # fa-medical
        'layout': 'monadtall',
        'matches': [Match(wm_class=('Steam',))],
    }),
    ('', {  # fa-envelope-o
        'layout': 'max',
        'matches': [Match(wm_class=('Icedove', 'Thunderbird', 'Mail',))],
    }),
    ('', {}),  # fa-circle-o
#    ('', {}),  # fa-dot-circle-o
    ('', {  # fa-music
        'layout': 'max',
        'matches': [Match(wm_class=("spotify", "Spotify", "vlc", "Vlc",))],
    }),
)

groups = []
for idx, (label, config) in enumerate(group_setup):
    hotkey = str(idx + 1)
    config.setdefault('layout', 'tile')
    groups.append(Group(label, **config))

    # mod + hotkey = switch to group
    keys.append(Key([mod], hotkey, lazy.group[label].toscreen()))

    # mod + shift + hotkey = move focused window to group
    keys.append(Key([mod, 'shift'], hotkey, lazy.window.togroup(label)))


# Mouse
mouse = (
    Drag([mod], 'Button1', lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], 'Button3', lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
)

bring_front_click = True


# Screens
screens = [
    Screen(
        top=bar.Bar(widgets=[
            widget.GroupBox(**Widget.groupbox),
            widget.WindowName(),
            widget.CurrentLayout(),
            widget.Sep(**Widget.sep),
            widget.Clock(format='%a %d %b %H:%M:%S'),
        ], **bar_defaults),
        bottom=bar.Bar(widgets=[
            widget.Notify(**Widget.notify_layout),
            widget.Spacer(),
            widget.Sep(**Widget.sep),
#            _khalwidget.CustomKhalWidget(),
        ], **bottom_bar_defaults),
    ),
    Screen(
        # bottom=bar.Bar(widgets=[Powerline()], **bar_defaults),
        top=bar.Bar(widgets=[
            widget.GroupBox(**Widget.groupbox),
            widget.WindowName(),

            widget.CPUGraph(graph_color='#18BAEB', fill_color='#1667EB.3', **Widget.graph),
            widget.MemoryGraph(graph_color='#00FE81', fill_color='#00B25B.3', **Widget.graph),
            widget.NetGraph(graph_color='#ffff00', fill_color='#4d4d00', interface='eth0', **Widget.graph),
            widget.HDDBusyGraph(device='sda', **Widget.graph),
            widget.DF(),

            widget.ThermalSensor(metric=True, threshold=158),
            widget.Sep(**Widget.sep),

            widget.CurrentLayout(),
            widget.Sep(**Widget.sep),
            widget.KeyboardLayout(**Widget.keyboard_layout),
            widget.Sep(**Widget.sep),
            widget.Systray(**Widget.systray),
#            widget.BatteryIcon(**Widget.battery),
            # widget.Battery(**Widget.battery_text),
            widget.Volume(cardid=1),
            # widget.YahooWeather(**Widget.weather),
            widget.Sep(**Widget.sep),
            _weather.WeatherComWidget(**Widget.weather),
            widget.Sep(**Widget.sep),
            _thunderbird.ThunderbirdWidget(**Widget.weather),
            widget.Sep(**Widget.sep),
            widget.Clock(format='%a %d %b %H:%M:%S'),
            ], **bar_defaults),
        # bottom=bar.Bar(widgets=[
        #     widget.Notify(**Widget.notify_layout),
        # ], **bottom_bar_defaults),
    )
]


# Layouts
layouts = (
    layout.Tile(ratio=0.5, **layout_defaults),
    layout.Max(**layout_defaults),
    layout.RatioTile(**layout_defaults),
    layout.Matrix(**layout_defaults),
    layout.MonadTall(**layout_defaults),
    layout.Stack(stacks=4,**layout_defaults),
    layout.Zoomy(**layout_defaults),
    layout.TreeTab(sections=['Work', 'Messaging', 'Docs', 'Util', 'Other']),
    # layout.Slice('right', 256, name='pidgin', role='buddy_list',
    #              fallback=layout.Stack(stacks=2, border_width=1)),
)

floating_layout = layout.floating.Floating(
    auto_float_types=(
        'notification',
        'toolbar',
        'splash',
        'dialog',
    ),
    float_rules=[{'wmclass': x} for x in (
        'audacious',
        'Download',
        'dropbox',
        'file_progress',
        'file-roller',
        'gimp',
        'Komodo_confirm_repl',
        'Komodo_find2',
        'pidgin',
        'skype',
        'Transmission',
        'Update',  # Komodo update window
        'Xephyr',
    )],
    **layout_defaults
)


def main(qtile):
    pass


def get_group_index(group_name):
    for group in xrange(len(groups)):
        if groups[group].name == group_name:
            return group

@hook.subscribe.client_new
def floating_dialogs(window):
    dialog = window.window.get_wm_type() == 'dialog'
    transient = window.window.get_wm_transient_for()
    alarm = window.window.get_wm_window_role() == "AlarmWindow"
    if dialog or transient or alarm:
        window.floating = True

        # c = Client()
        # current_group = c.group.info()['name']
        # window.togroup(current_group)
