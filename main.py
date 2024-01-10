# -*- coding: utf-8 -*-

import login
from playlist import UserPlaylist, Playlist


netease = login.Login()
netease.start()
print(netease.get_login_status)

user_playlist = UserPlaylist().user_playlist
print(user_playlist)
counts = int(input('count:'))
playlist1 = Playlist(user_playlist[counts]['playlist_id'])
playlist1.get_playlist_detail()
with open('test.txt', 'w') as wf:
    wf.write(str(playlist1.ex_playlist))

input()
