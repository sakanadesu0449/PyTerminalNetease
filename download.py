import wget
import os
import re
from storage import UpdateDownload
from pyncm import apis

class Download:
    def __init__(self):
        self.pattern = r"[\/\\\:\*\?\"\<\>\|]"
        self.level = 'hires'

    def rm_unavail_char(self, old_name):
        new_title = re.sub(self.pattern, "", old_name)
        return new_title

    def download_single_track(self, url, f_name):
        file_name = rm_unavail_char(f_name)
        wget(url, f'download{os.pathsep}{file_name}')

    def get_track_detail(self, track_id):
        track_detail = apis.track.GetTrackAudioV1(track_id,level=self.level)
        url = track_detail['data'][0]['url']
        outsider = track_detail['data'][0]['type']
        return url,outsider

    def download_playlist(self, playlist_id, playlist):
        with UpdateDownload(playlist_id) as updates:
            for track in playlist:
                if track['download']:
                    continue
                track_url, outsider = get_track_detail(track['id'])
                file_name = '{0}-{1}'.format(
                        track['data']['artist'],
                        track['data']['name']
                        )

