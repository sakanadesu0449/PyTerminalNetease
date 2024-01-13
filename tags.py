# -*- coding: utf-8 -*-

from mutagen.flac import FLAC, Picture
from mutagen.mp3 import EasyMP3
from mutagen.id3 import ID3, APIC
import os
import sys

SEP = os.sep

class Tag:
    def __init__(self):
        self.TRACK_PATH = f'downloads{SEP}'
        self.LRC_PATH = f'downloads{SEP}lrcs{SEP}'
        self.COVER_PATH = f'downloads{SEP}covers{SEP}'

    def mp3(self, file_name, track_info):
        try:
            id3s = EasyMP3(f'{self.TRACK_PATH}{file_name}mp3')
            with open(f'{self.COVER_PATH}{file_name}jpg', 'rb') as imagef:
                image = imagef.read()

            id3s['title'] = track_info['data']['name']
            id3s['artist'] = track_info['data']['artist']
            id3s['album'] = track_info['data']['album']
            id3s.save()
            track_i = ID3(f'{self.TRACK_PATH}{file_name}mp3')
            track_i.update_to_v23()
            track_i.add(APIC(3, 'image/jpeg', 3, 'Front Cover', image))
            track_i.save(v2_version=3)

        except:
            print('fatal error')
            print(sys.exc_info())
            sys.exit()

    def flac(self, file_name, track_info):
        try:
            id3s = FLAC(f'{self.TRACK_PATH}{file_name}flac')
            with open(f'{self.LRC_PATH}{file_name}lrc', 'r') as lrcf:
                lrc = lrcf.read()
            with open(f'{self.COVER_PATH}{file_name}jpg', 'rb') as imagef:
                image = imagef.read()

            id3s['title'] = track_info['data']['name']
            id3s['artist'] = track_info['data']['artist']
            id3s['album'] = track_info['data']['album']
            id3s['lyrics'] = lrc
            
            pic = Picture()
            pic.data = image
            pic.mime = 'image/jpeg'
            id3s.add_picture(pic)
            
            id3s.save()
        except:
            print('fatal error')
            print(sys.exc_info())
            sys.exit()

    def write(self, file_name, track_info, f):
        try:
            if f == 'mp3':
                self.mp3(file_name, track_info)
            if f == 'flac':
                self.flac(file_name, track_info)

        except:
            print(sys.exc_info())



