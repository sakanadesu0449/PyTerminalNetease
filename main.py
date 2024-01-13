# -*- coding: utf-8 -*-

import login
from playlist import UserPlaylist, Playlist
from download import Download

def mainloop():
    up = UserPlaylist()
    user_playlist = up.user_playlist
    for playlist_count in range(0,len(user_playlist)):
        print('{0} {1}    {2}   {3}'.format(
            playlist_count,
            user_playlist[playlist_count]['name'],
            user_playlist[playlist_count]['creator'],
            user_playlist[playlist_count]['count']
            )
        )
    selects = int(input('choice a playlist:'))
    playlist = Playlist(user_playlist[selects]['playlist_id'])
    playlist.start()
        
if __name__ == '__main__':

    netease = login.Login()
    netease.start()
    print(netease.get_login_status)
    mainloop()


