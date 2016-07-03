# -*- coding: utf-8 -*-
import requests as _requests
import libqtile as _qtile
import libqtile.widget as _widget

from urllib.request import urlopen
import re
import xml.etree.ElementTree as ElementTree

WEATHER_COM_URL = 'http://wxdata.weather.com/wxdata/weather/local/%s?unit=%s&dayf=1&cc=*'

class WeatherComWidget(_widget.base.ThreadedPollText):
    """
    Custom Widget to request from weather informations from
    weather.com
    """

    orientations = _widget.base.ORIENTATION_HORIZONTAL
    defaults=[
        ('location_code', None, 'Location Code for weather.com'),
        ('units', 'm', 'Unit for weather'),
        ('colorize', False, 'show icons'),
        ('foreground', 'FFFFFF', 'default foreground color'),
    ]
    color_icons = {
        "Fair": (u"\u2600", "#FFCC00"),
        "Cloudy": (u"\u2601", "#F8F8FF"),
        "Partly Cloudy": (u"\u2601", "#F8F8FF"),  # \u26c5 is not in many fonts
        "Rainy": (u"\u2614", "#CBD2C0"),
        "Sunny": (u"\u263C", "#FFFF00"),
        "Snow": (u"\u2603", "#FFFFFF"),
        "default": ("", None),
    }

    def __init__(self, **config):
        _widget.base.ThreadedPollText.__init__(self, **config)
        self.add_defaults(WeatherComWidget.defaults)
        self.text = "--°C"
        self.default_foreground = self.foreground

    def get_current_weather(self):
        pass

    def poll(self):
        result = self.fetch_weather()
        conditions = result["current_conditions"]
        temperature = conditions["temperature"]
        humidity = conditions["humidity"]
        wind = conditions["wind"]
        units = result["units"]
        color = None
        current_temp = "{t}°{d}".format(t=temperature, d=units["temperature"])
        min_temp = "{t}°{d}".format(t=result["today"]["min_temperature"], d=units["temperature"])
        max_temp = "{t}°{d}".format(t=result["today"]["max_temperature"], d=units["temperature"])
        current_wind = "{t} {s}{d}".format(t=wind["text"], s=wind["speed"], d=units["speed"])

        if self.colorize:
            icon, color = self.color_icons.get(conditions["text"],
                                               self.color_icons["default"])
            current_temp = "{t}°{d} {i}".format(t=temperature,
                                                d=units["temperature"],
                                                i=icon)
            color = color

        data = "%s" % current_temp
        if color is not None:
            self.foreground = color
        return data

    def fetch_weather(self):
        '''Fetches the current weather from wxdata.weather.com service.'''
        unit = '' if self.units == 'i' or self.units == '' else 'm'
        url = WEATHER_COM_URL % (self.location_code, unit)
        with urlopen(url) as handler:
            try:
                content_type = dict(handler.getheaders())['Content-Type']
                charset = re.search(r'charset=(.*)', content_type).group(1)
            except AttributeError:
                charset = 'utf-8'
            xml = handler.read().decode(charset)
        doc = ElementTree.XML(xml)
        return dict(
            current_conditions=dict(
                text=doc.findtext('cc/t'),
                temperature=doc.findtext('cc/tmp'),
                humidity=doc.findtext('cc/hmid'),
                wind=dict(
                    text=doc.findtext('cc/wind/t'),
                    speed=doc.findtext('cc/wind/s'),
                ),
            ),
            today=dict(
                min_temperature=doc.findtext('dayf/day[@d="0"]/low'),
                max_temperature=doc.findtext('dayf/day[@d="0"]/hi'),
            ),
            units=dict(
                temperature=doc.findtext('head/ut'),
                speed=doc.findtext('head/us'),
            ),
        )
