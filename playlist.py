# -*- coding: utf-8 -*-

import storage
from pyncm import apis
from download import Download

class UserPlaylist:
    def __init__(self, user_id=0):
        self.user_id = user_id

    @property
    def user_playlist(self):
        self.get_user_playlists()
        return self.playlists_info

    def get_user_playlists(self):
        self.playlists_info = []
        usr_playlist = apis.user.GetUserPlaylists(self.user_id)

        for playlist in usr_playlist["playlist"]:
            self.playlists_info.append({
                'name' : playlist["name"],
                'playlist_id' : playlist['id'],
                'count' : playlist["trackCount"],
                'creator' : playlist["creator"]["nickname"]
                }
            )
                


class Playlist:
    def __init__(self, playlist_id):
        self.local_playlist = storage.Playlist()
        self.playlist_id = playlist_id
        self.hr_order = ['hr', 'sq', 'h', 'm', 'l'] #音质级别从高到底保证获取最高音质
        self.ex_playlist = []

    def get_hier_br(self, track):
        #获取最高音质
        for hr in self.hr_order:
            if track[hr] is not None:
                return hr

    def get_all_artists(self, track):
        #拼接多个艺术家名称，以逗号链接
        all_artist_list = []
        for artists in track['ar']:
            all_artist_list.append(artists['name'])
        return ','.join(all_artist_list)


    def get_playlist_detail(self, limits=1000):
        self.playlist_detail = apis.playlist.GetPlaylistInfo(self.playlist_id, limit=limits)

        for track in self.playlist_detail['playlist']['tracks']:
            #构造单曲数据
            track_details = {
                    'id' : track['id'],
                    'download' : False,
                    'data' : {
                        'name' : track['name'],
                        'artist' : self.get_all_artists(track),
                        'coverUrl' : track['al']['picUrl'],
                        'album' : track['al']['name'],
                        'br' : track[self.get_hier_br(track)]['size']
                        }
                    }
            self.ex_playlist.append(track_details)
        self.local_playlist.update_playlist(self.playlist_id, self.ex_playlist)

    def start(self):
        self.get_playlist_detail()
        d_st = lambda x : '√' if x else 'x'
        local_playlist = self.local_playlist.get_playlist_detail(self.playlist_id)
        for track in local_playlist:
            print('{0}   {1} {2:.1f}m {3}'.format(
                track['data']['name'],
                track['data']['artist'],
                (track['data']['br']/1000000),
                d_st(track['download'])
                )
            )
        if input('download this playlist?[y/n]') == 'y':
            download = Download()
            download.download_playlist(self.playlist_id, local_playlist)


