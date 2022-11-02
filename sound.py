import pygame

from setting import *

from config import conf
import lib


class __Sound(object):
    def __init__(self):

        self._sounds = {}

        for filename in SOUND_FILES:
            sound = filename.rsplit(".", 1)[0]
            self._sounds[sound] = pygame.mixer.Sound(lib.filename(filename))

    def play(self, sound, times=0):
        if conf.sound:
            try:
                self.stop(sound)
                self._sounds[sound].play(times)
            except KeyError as e:
                raise AttributeError("Invalid sound %s." % sound)

    def stop(self, sound):
        try:
            self._sounds[sound].stop()
        except KeyError as e:
            pass

    def stop_all(self):
        for k, v in self._sounds.items():
            try:
                v.stop()
            except:
                pass


sound = __Sound()
