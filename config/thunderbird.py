# -*- coding: utf-8 -*-
import requests as _requests
import libqtile as _qtile
import libqtile.widget as _widget
from functools import partial

import dbus
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GObject



class ThunderbirdWidget(_widget.TextBox):
    """
    Custom Widget to request from weather informations from
    weather.com
    """

    orientations = _widget.base.ORIENTATION_HORIZONTAL
    defaults=[]
    _unread = set()

    def __init__(self, **config):
        _widget.TextBox.__init__(self, **config)
        self.add_defaults(ThunderbirdWidget.defaults)
        self._update_text()

        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        bus = dbus.SessionBus()
        bus.add_signal_receiver(self.new_msg,
                                dbus_interface="org.mozilla.thunderbird.DBus",
                                signal_name="NewMessageSignal")
        bus.add_signal_receiver(self.changed_msg,
                                dbus_interface="org.mozilla.thunderbird.DBus",
                                signal_name="ChangedMessageSignal")
        loop = GObject.MainLoop()
        dbus.mainloop.glib.threads_init()
        self.context = loop.get_context()

        self.run = partial(self.context.iteration, False)

    def _update_text(self):
        unread_length = len(self._unread)
        if unread_length:
            self.foreground = "ff0000"
        else:
            self.foreground = "ffffff"
        self.text = "%s " % len(self._unread)

    def update(self):
        self._update_text()
        self.bar.draw()

    def new_msg(self, id, author, subject):
        if id not in self._unread:
            self._unread.add(id)
        self.update()

    def changed_msg(self, id, event):
        if event == "read" and id in self._unread:
            self._unread.remove(id)
        self.update()

    @property
    def unread(self):
        self.run()
        return len(self._unread)
