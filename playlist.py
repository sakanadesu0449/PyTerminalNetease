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

        for playlist_ser in range(0,len(usr_playlist["playlist"])):
            self.playlists_info.append(
                {
                    'name' : usr_playlist["playlist"][playlist_ser]["name"],
                    'playlist_id' : usr_playlist["playlist"][playlist_ser]["id"],
                    'count' : usr_playlist["playlist"][playlist_ser]["trackCount"],
                    'creator' : usr_playlist["playlist"][playlist_ser]["creator"]["nickname"]
                    }
                )
                


class Playlist:
    def __init__(self, playlist_id):
        '''                                                                         storage_format = [                                                              {
                'id' : int
                'download' : bool                                                           'data' : {
                    'name' : str                                                                'artist' : str                                                              'coverUrl' : str                                                            'lrcs' : str
                    'album' : str                                                               'br' : {
                        'standard' : int                                                            'higher' : int
                        'exhigh' : int                                                              'lossless' : int
                        'hires' : int                                                               }                                                                       }
                }
            ]
        '''
        self.playlist_id = playlist_id

    def get_playlist_detail(self, limits=1000):
        self.playlist_detail = apis.playlist.GetPlaylistInfo(playlist_id,limit=limits)
