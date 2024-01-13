import wget
import os
import re
import tags
import time
import sys
from storage import UpdateDownload
from pyncm import apis

SEP = os.sep

def GeneralDownloadError(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except:
            print('fatal error!')
            print(sys.exc_info())

    return wrapper

class Download:
    def __init__(self):

        self.pattern = r'[\/\\\:\*\?\"\<\>\|]'
        self.level = 'hires'
        self.tag = tags.Tag()
        self.TRACK_PATH = f'downloads{SEP}'
        self.LRC_PATH = f'downloads{SEP}lrcs{SEP}'
        self.COVER_PATH = f'downloads{SEP}covers{SEP}'
        
        for path_t in self.TRACK_PATH, self.LRC_PATH, self.COVER_PATH:
            if not os.path.isdir(path_t):
                os.mkdir(path_t)

    def rm_unavail_char(self, old_name):
        new_title = re.sub(self.pattern, "", old_name)
        return new_title

    @GeneralDownloadError
    def download_cover(self, url, f_name):
        print(url)
        wget.download(url, f'{self.COVER_PATH}{f_name}')

    @GeneralDownloadError
    def download_single_track(self, url, f_name):
        print(url)
        wget.download(url, f'{self.TRACK_PATH}{f_name}')

    def get_track_detail(self, track_id):
        track_detail = apis.track.GetTrackAudioV1(track_id,level=self.level)
        url = track_detail['data'][0]['url']
        outsider = track_detail['data'][0]['type']
        return url,outsider

    @GeneralDownloadError
    def download_lrc(self, track_id, f_name):
        lrc_data = apis.track.GetTrackLyrics(str(track_id))
        lrc = lrc_data['lrc']['lyric']
        with open(f'{self.LRC_PATH}{f_name}', 'w') as lrc_f:
            lrc_f.write(lrc)

    def download_playlist(self, playlist_id, playlist):
        with UpdateDownload(playlist_id) as updates:
            for track in playlist:
                if track['download']:
                    continue
                track_url, outsider = self.get_track_detail(track['id'])
                if not track_url:
                    continue
                file_name = self.rm_unavail_char('{0}-{1}.'.format(
                        track['data']['artist'],
                        track['data']['name']
                        )
                    )
                self.download_single_track(track_url, f'{file_name}{outsider}')
                self.download_cover(track['data']['coverUrl'], f'{file_name}jpg')
                self.download_lrc(track['id'], f'{file_name}lrc')
                updates.update_download_stat(track['id'])

                self.tag.write(file_name, track, outsider)
                time.sleep(15)
                



