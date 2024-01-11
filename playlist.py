from storage import Playlist,UpdateDownload
from pyncm import apis


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
        '''                                                                         storage_format = [{
                'id' : int
                'download' : bool                                                           'data' : {
                    'name' : str                                                                'artist' : str                                                              'coverUrl' : str
                    'album' : str                                                               'br' : int                                             
                }
            }
        ]
        '''
        self.playlist_id = playlist_id
        self.hr_order = ['hr', 'sq', 'l', 'm', 'h']
        self.ex_playlist = []

    def get_hier_br(self, track):
        for hr in self.hr_order:
            if track[hr] is not None:
                return hr

    def get_all_artists(self, track):
        all_artist_list = []
        for artists in track['ar']:
            all_artist_list.append(artists['name'])
        return ','.join(all_artist_list)


    def get_playlist_detail(self, limits=1000):
        self.playlist_detail = apis.playlist.GetPlaylistInfo(self.playlist_id, limit=limits)

        for track in self.playlist_detail['playlist']['tracks']:
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

