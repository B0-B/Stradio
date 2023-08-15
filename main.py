#!/usr/bin/env python3

import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
try:
    import vlc
    from vlc import Instance, EventType, Media, MediaPlayer, MediaParseFlag, Meta
except:
    messagebox.showwarning('VLC not installed', 'Please install VLC 64 bit!')
    quit()
import tkinter as tk
import ctypes as ct
import platform
from traceback import print_exc
from os import path
from time import sleep
from pathlib import Path

class streamPlayer:

    def __init__ (self, streamUrl:str) -> None:
        
        self.streamUrl = streamUrl
        self.channel = Instance('--input-repeat=-1', '--fullscreen')
        self.player = self.channel.media_player_new()

        self.update()

    def update (self):

        '''
        Call update to change to another stream.
        '''

        self.media = self.channel.media_new(self.streamUrl)
        self.media.get_mrl()
        self.player.set_media(self.media)
        self.media.parse()
    
    def updateStreamUrl (self, newUrl:str) -> None:

        self.stop()
        self.streamUrl = newUrl
        self.update()
    
    def play (self) -> None:

        self.player.play()
    
    def pause (self) -> None:

        self.player.pause()
    
    def stop (self) -> None:

        self.player.stop()

    def volume (self, value:int=50) -> None:

        self.player.audio_set_volume(value)

class radio (tk.Tk):

    __root__ = Path(__file__).parent

    def __init__(self, streamUrls:dict, autoplay:bool=True) -> None:

        tk.Tk.__init__(self)

        # UI style 
        self.bg = '#000'
        self.fg = '#fff'
        self.font = ('Arial', 8)
        self.dpi = 200
        self.opacity = 0.7

        # variables
        self.refresh = 100 # in ms
        self.totalStreams = len(list(streamUrls.keys()))
        self.streamUrls = streamUrls
        self.streamId = 0
        self.radioName = list(streamUrls.keys())[self.streamId]
        self.streamUrl = self.streamUrls[self.radioName]
        self.streamUrlVar = tk.StringVar(self, self.streamUrl)
        self.volumeVar = tk.IntVar(self, 70)
        
        self.songTitle = 'stream'
        self.displayVar = tk.StringVar(self, 'Hi!')

        # load stream player
        self.player = streamPlayer(self.streamUrl)

        self.buildInterface()

        if autoplay: 
            self.player.play()

        self.after(self.refresh, self.update)
        self.mainloop()

    def buildInterface (self) -> None:

        self.tk.call('tk', 'scaling', int(self.dpi/72))

        # icon in task bar
        ico = Image.open(self.__root__.joinpath('radio.ico'))
        icon = ImageTk.PhotoImage(ico)
        self.wm_iconphoto(False, icon)
        # self.iconbitmap(self.__root__.joinpath('radio.ico'))
        
        # special for windows rendering
        if platform.system() == 'Windows':
            
            DWMWA_USE_IMMERSIVE_DARK_MODE = 20
            set_window_attribute = ct.windll.dwmapi.DwmSetWindowAttribute
            get_parent = ct.windll.user32.GetParent
            hwnd = get_parent(self.winfo_id())
            rendering_policy = DWMWA_USE_IMMERSIVE_DARK_MODE
            value = 2
            value = ct.c_int(value)
            set_window_attribute(hwnd, rendering_policy, ct.byref(value),ct.sizeof(value))
        
        self.title(' Stradio | '+self.radioName)
        self.configure(bg=self.bg) 
        self.geometry('600x80')
        self.attributes('-alpha', self.opacity)
        
        # logo = tk.Label(self, image=display)
        # logo.pack()

        width = 3
        height = 3

        prevButton = tk.Button(self,bg=self.bg, width=width, height=height, fg=self.fg, text='◀', command=self.prev, borderwidth=0, highlightthickness=0)
        prevButton.pack(side=tk.LEFT)

        lab = tk.Label(self, textvariable=self.displayVar, font=self.font,
            fg=self.fg, bg=self.bg, height=height, width=50)
        lab.pack(side=tk.LEFT)

        nextButton = tk.Button(self,bg=self.bg, fg=self.fg, width=width, height=height, text='▶', command=self.next, borderwidth=0, highlightthickness=0)
        nextButton.pack(side=tk.RIGHT)

        style = ttk.Style()
        style.configure("TScale", background="#000")
        volumeSlider = ttk.Scale(self, from_=0, to=100, variable=self.volumeVar, orient=tk.HORIZONTAL, style="TScale")
        volumeSlider.pack(side=tk.RIGHT)

        
    
    def getMetaData (self) -> str:

        '''
        draws the current song meta data from stream.
        If not applicable will return 
        '''

        m = self.player.media.get_meta(12) # vlc.Meta 12: 'NowPlaying',
        print('meta', m)
        if not m:
            return self.radioName
        return m

    def next (self) -> None:

        '''
        Changes to the next stream.
        '''

        self.streamId = (self.streamId + 1) % self.totalStreams
        self.radioName = list(self.streamUrls.keys())[self.streamId]
        self.title('Stradio | '+self.radioName)
        self.streamUrl = self.streamUrls[self.radioName]
        self.streamUrlVar.set(self.radioName)
        self.player.updateStreamUrl(self.streamUrl)
        self.player.play()
    
    def prev (self) -> None:

        '''
        Changes to the previous stream.
        '''

        self.streamId = (self.streamId - 1) % self.totalStreams
        self.radioName = list(self.streamUrls.keys())[self.streamId]
        self.title('Stradio | '+self.radioName)
        self.streamUrl = self.streamUrls[self.radioName]
        self.streamUrlVar.set(self.radioName)
        self.player.updateStreamUrl(self.streamUrl)
        self.player.play()

    def update (self) -> None:
        try:

            # update song title meta data
            meta = self.getMetaData()
            if meta != self.songTitle:
                self.songTitle = meta
                self.displayVar.set(self.songTitle)

            # parse volume
            self.player.volume(self.volumeVar.get())
            # self.display.set(self.currentTime2Text())
        except Exception as e:
            print_exc()
        finally:
            self.after(self.refresh, self.update)
        
if __name__ == '__main__':

    streams = {
        'Naxi Love Radio': 'https://naxidigital-love128ssl.streaming.rs:8102/;stream.nsv',
        'MNM High': "http://icecast.vrtcdn.be/mnm-high.mp3",
        'BlueRock': 'http://prem1.rockradio.com:80/bluesrock?9555ae7caa92404c73cade1d'
    }
    radio(streams)

