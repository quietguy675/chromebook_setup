#!/usr/bin python3

import vlc
import threading
from math import ceil
from time import sleep

def threaded(fn):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return wrapper

class VLC_Thread():
    def __init__(self):
        self.threads = []
        self.vlc_instance = vlc.Instance()
        self.vlc_player = self.vlc_instance.media_player_new()
        self.vlc_media = self.vlc_instance.media_new('')

    def stage_media_and_get_time_left(self, media, position=0):
        self.vlc_media = self.vlc_instance.media_new(media)
        self.vlc_player.set_media(self.vlc_media)
        self.vlc_player.play()
        sleep(1)
        self.vlc_player.set_position(position)
        position = self.vlc_player.get_time()
        length = self.vlc_player.get_length()
        self.vlc_player.pause()
        # Number of seconds left
        return ceil((length-position)/1000)

    @threaded
    def start_vlc(self):
        print(threading.currentThread().getName(), 'Starting')
        self.vlc_player.play()
        self.vlc_player.set_fullscreen(True)
        while self.vlc_player.get_position() < 0.999 and self.vlc_player.get_position() >= 0.00:
            sleep(1)
        self.vlc_player.set_fullscreen(False)
        self.vlc_player.stop()
        print(threading.currentThread().getName(), 'Exiting')

