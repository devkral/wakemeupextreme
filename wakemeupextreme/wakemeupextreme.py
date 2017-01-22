
__license__ = "MIT"
__author__ = "Alexander K."

import datetime
import enum
import functools
import logging
import subprocess
import random
import time
import gc
import threading
import configparser
import os
import importlib

from LED import LED
from calculations import questions
import guis


default_update_check_interval = 5
min_seconds_diff = datetime.timedelta(seconds=10)
default_sources = \
{
    "radio1": "http://dir.xiph.org/listen/585332/listen.m3u"
}
process = ["/usr/bin/mpv", "--no-video", "--volume=100"]




@functools.total_ordering
class dateob(object):
    weekday = None
    hour = None
    minute = None
    
    class weekdays(enum.IntEnum):
        every = 0
        jeden = 0
        monday = 1
        montag = 1
        tuesday = 2
        dienstag = 2
        wednesday = 3
        mittwoch = 3
        thursday = 4
        donnerstag = 4
        friday = 5
        freitag = 5
        saturday = 6
        samstag = 6
        sunday = 7
        sonntag = 7
        
        @classmethod
        def isin(cls, item):
            if isinstance(item, str):
                return cls[item.lower()] in cls
            else:
                return item in cls
    
    def __init__(self, weekday=weekdays.every, hour=8, minute=0):
        self.weekday = weekday
        self.hour = hour
        self.minute = minute
    
    def __eq__(self, other):
        if not isinstance(other, dateob):
            raise TypeError()
        if self.weekday == other.weekday and self.hour == other.hour and self.minute == other.minute:
            return True
        else:
            return False
    
    def __lt__(self, other):
        if not isinstance(other, dateob):
            raise TypeError()
        now = datetime.datetime.today()+min_seconds_diff
        today = now.isoweekday()
        wday = int(self.weekday)
        if wday == 0:
            if (self.hour, self.minute) < (now.hour, now.minute):
                wday = today + 1
            else:
                wday = today
        elif wday < today or (today==wday and (self.hour, self.minute) < (now.hour, now.minute)):
            wday += 7

        wdayo = int(other.weekday)
        if wdayo == 0:
            if (other.hour, other.minute) < (now.hour, now.minute):
                wdayo = today + 1
            else:
                wdayo = today
        elif wdayo < today or (today==wdayo and (other.hour, other.minute) < (now.hour, now.minute)):
            wdayo += 7
        if (wday, self.hour, self.minute) < (wdayo, other.hour, other.minute):
            return True
        else:
            return False
    
    def total_seconds(self):
        now = datetime.datetime.today()
        today = now.isoweekday()
        wday = int(self.weekday)
        t = datetime.datetime(year=now.year, month=now.month, day=now.day, hour=self.hour, minute=self.minute)
        if wday == 0:
            if t<now:
                t += datetime.timedelta(days=1)
        elif wday < today or (today==wday and t<now):
            t += datetime.timedelta(days=7)
        return int((t-now).total_seconds())

    @classmethod
    def create(cls, dstring):
        splitted = dstring.split("-")
        if len(splitted) == 1:
            if splitted[0].isdecimal():
                h = int(splitted[0])
                if h>=0 and h<24:
                    return cls(hour=h)
            elif cls.weekdays.isin(splitted[0]):
                return cls(weekday=cls.weekdays[splitted[0]])
        elif len(splitted) == 2:
            if splitted[0].isdecimal() and splitted[1].isdecimal():
                h, m = int(splitted[0]), int(splitted[1])
                if h>=0 and h<24 and m>=0 and m<60:
                    return cls(hour=h, minute=m)
            elif cls.weekdays.isin(splitted[0]) and splitted[1].isdecimal():
                h = int(splitted[1])
                if h>=0 and h<24:
                    return cls(weekday=cls.weekdays[splitted[0]], hour=h)
        elif len(splitted) == 3:
            if cls.weekdays.isin(splitted[0]) and splitted[1].isdecimal() and splitted[2].isdecimal():
                h, m = int(splitted[1]), int(splitted[2])
                if h>=0 and h<24 and m>=0 and m<60:
                    return cls(weekday=cls.weekdays[splitted[0]], hour=h, minute=m)
        # DO NOT USE else:
        return None


class MyParser():
    thread = None
    config_path = None
    config = None
    def __init__(self, config_path):
        self.config_path = config_path
        self.config = self.read_config()

    def read_config(self):
        config = configparser.ConfigParser()
        if os.path.exists(self.config_path):
            with open(self.config_path, "r") as wfo:
                config.read_file(wfo)
            needsupdate = False
        else:
            needsupdate = True
        if not config.has_section("other"):
            config.add_section("other")
            needsupdate = True
        if "check_interval" not in config["other"]:
            config.set('other', "check_interval", str(default_update_check_interval))
            needsupdate = True
        if "gui" not in config["other"]:
            config.set('other', "gui", "tk")
            needsupdate = True
        if "exclude_questions" not in config["other"]:
            config.set('other', "exclude_questions", "")
            needsupdate = True
        if "led_timing" not in config["other"]:
            config.set('other', "led_timing", str(0.2))
            needsupdate = True
        if not config.has_section("leds"):
            config.add_section("leds")
            needsupdate = True
        if not config.has_section("alarms"):
            config.add_section("alarms")
            needsupdate = True
        if not config.has_section("sources"):
            config.add_section("sources")
            config['sources'] = default_sources
            needsupdate = True
        if needsupdate:
            with open(self.config_path, "w") as wfo:
                config.write(wfo)
        return config
    
    def notify_changes(self, **ufuncs):
        if not self.thread:
            self.thread = threading.Thread(target=self._notify_changes, kwargs=ufuncs, daemon=True)
            self.thread.start()
    
    def _notify_changes(self, **ufuncs):
        while True:
            time.sleep(self.config.getint("other","check_interval", fallback=default_update_check_interval))
            try:
                cnew = self.read_config()
            except:
                continue
            for section in ["leds", "alarms", "sources", "other"]:
                needsupdate = False
                for source, dest in [(self.config, cnew), (cnew, self.config)]:
                    for key, val in source[section].items():
                        if key not in dest[section] or dest[section][key] != val:
                            needsupdate = True
                            break
                    if needsupdate:
                        break
                if needsupdate:
                    logging.info("%s is updated", section)
                    try:
                        ufuncs.get(section, lambda config: None)(cnew)
                    except Exception as exc:
                        logging.exception(exc)

            self.config = cnew
                

class WakeMeUpExtreme(object):
    timetable = None
    sources = None
    leds = None
    exclude_questions = None
    
    nextevent = None
    subproc = None
    led_timing = 1
    gui = None
    

    def __init__(self, config):
        self.config = config
        self.timetable = []
        self.sources = []
        self.leds = []
        self.exclude_questions = set()
        self.open_gui()
        if not self.gui:
            raise
        self.update_sources(self.config.config)
        self.update_other(self.config.config)
        self.update_leds(self.config.config)
        self.update_timetable(self.config.config)
        self.config.notify_changes(leds=self.update_leds, alarms=self.update_timetable, sources=self.update_sources, other=self.update_other)

    @classmethod
    def create(cls, config_path):
        config = MyParser(config_path)
        return cls(config)
    
    def __del__(self):
        if self.nextevent:
            self.nextevent.cancel()
        if self.subproc:
            self.subproc.terminate()

    def open_gui(self):
        _guis = self.config.config.get("other", "gui").split(",")
        for elem in _guis:
            modname = "guis.{}".format(elem.strip().rstrip())
            try:
                _tgui = importlib.import_module(modname)
                self.gui = _tgui.Gui(self.alarm_stop)
            except ImportError:
                logging.info("Couldn't import gui: %s", modname)

    def update_timetable(self, config):
        t = []
        for key2 in config['alarms']:
            v = dateob.create(config['alarms'][key2])
            if v:
                t.append(v)
            else:
                logging.warning("invalid value for key: %s", key2)
        if self.nextevent:
            self.nextevent.cancel()
            self.nextevent = None
        self.timetable = t
        self.run_timetable()

    def run_timetable(self):
        if len(self.timetable) == 0:
            return
        self.timetable.sort()
        ob = self.timetable[0]
        seconds = ob.total_seconds()
        logging.debug("next: %s", seconds)
        self.nextevent = threading.Timer(seconds, self.alarm)
        self.nextevent.start()

    def update_sources(self, config):
        self.sources = []
        for key2 in config['sources']:
            self.sources.append(config['sources'][key2])
    
    def update_leds(self, config):
        if not LED:
            return
        for led in self.leds:
            led.close()
        self.leds = []
        for key2 in config['leds']:
            self.leds.append(LED(config.getint('leds',key2)))

    def update_other(self, config):
        self.exclude_questions = set(e.strip().rstrip() for e in config.get("other", "exclude_questions").split(","))
        self.exclude_questions.remove("")
        self.led_timing = config.getfloat("other", "led_timing")

    def alarm(self):
        if self.gui.alarmactive:
            return
        self.gui.alarmactive = True
        self.gui.alarm_start(random.choice(filter(lambda x: x.__name__ not in self.exclude_questions, questions))())
        for elem in self.leds:
            elem.blink(on_time=self.led_timing, off_time=self.led_timing)
        threading.Thread(target=self._alarm, daemon=True).start()
        return False

    def _alarm(self):
        while len(self.sources) > 0 and self.gui.alarmactive:
            try:
                subp = subprocess.Popen(process+[random.choice(self.sources)])
                self.subproc = subp
            except Exception as exc:
                logging.exception(exc)
            if self.subproc:
                self.subproc.wait()
            if self.alarmactive:
                time.sleep(1)

    def alarm_stop(self):
        self.gui.alarmactive = False
        for elem in self.leds:
            elem.off()
        if self.subproc:
            self.subproc.terminate()
        self.run_timetable()

