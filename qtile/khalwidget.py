# -*- coding: utf-8 -*-
import requests as _requests
import libqtile as _qtile
import libqtile.widget as _widget
from functools import partial

from libqtile import utils

import datetime
import dateutil.parser
import subprocess
import string


class CustomKhalWidget(_widget.base.ThreadedPollText):
    """Khal calendar widget

    This widget will display the next appointment on your Khal calendar in the
    qtile status bar. Appointments within the "reminder" time will be
    highlighted.
    """
    orientations = _widget.base.ORIENTATION_HORIZONTAL
    defaults = [
        (
            'reminder_color',
            'FF0000',
            'color of calendar entries during reminder time'
        ),
        ('foreground', 'FFFF33', 'default foreground color'),
        ('remindertime', 10, 'reminder time in minutes'),
        ('lookahead', 7, 'days to look ahead in the calendar'),
    ]

    def __init__(self, **config):
        _widget.base.ThreadedPollText.__init__(self, **config)
        self.add_defaults(CustomKhalWidget.defaults)
        self.text = 'Calendar not initialized.'
        self.default_foreground = self.foreground

    def poll(self):
        # get today and tomorrow
        now = datetime.datetime.now()
        tomorrow = now + datetime.timedelta(days=1)

        # get reminder time in datetime format
        remtime = datetime.timedelta(minutes=self.remindertime)

        # parse khal output for the next seven days
        # and get the next event
        args = ['khal', 'agenda', '--days', str(self.lookahead)]
        cal = subprocess.Popen(args, stdout=subprocess.PIPE)
        output = cal.communicate()[0]
        output = output.decode()
        output = output.split('\n')
        caldate = output[0]
        try:
            if output[0] == 'Today:':
                date = str(now.month) + '/' + str(now.day) + '/' + \
                    str(now.year)
            elif output[0] == 'Tomorrow:':
                date = str(tomorrow.month) + '/' + str(tomorrow.day) + \
                    '/' + str(tomorrow.year)
            else:
                date = output[0]
        except IndexError:
            return 'No appointments scheduled'
        for i in range(1, len(output)):
            try:
                starttime = dateutil.parser.parse(date + ' ' + output[i][:5],
                                                  ignoretz=True)
                endtime = dateutil.parser.parse(date + ' ' + output[i][6:11],
                                                ignoretz=True)
            except ValueError:
                date = output[i]
                if date == 'Tomorrow:':
                    date = str(tomorrow.month) + '/' + str(tomorrow.day) + \
                           '/' + str(tomorrow.year)
                caldate = output[i]
                continue
            if endtime > now:
                data = caldate.replace(':', '') + ' ' + output[i]
                break
            else:
                data = 'No appointments in next ' + \
                    str(self.lookahead) + ' days'

        # get rid of any garbage in appointment added by khal
        data = ''.join(filter(lambda x: x in string.printable, data))

        # colorize the event if it is within reminder time
        if ((starttime - remtime) <= now) and (endtime > now):
            self.foreground = utils.hex(self.reminder_color)
        else:
            self.foreground = self.default_foreground

        return data
