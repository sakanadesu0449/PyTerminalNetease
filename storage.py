# -*- coding: utf-8 -*-

import os
import sys
import yaml

ENV_SEP = os.sep
ENV_LINESEP = os.linesep
DEVICE_NAME = os.name

class Account:

    def __init__(self):

        self.ACC_DATA_PATH = 'user'
        
        '''
        'alias' : {
            'last_method': ''
            'account': ''
            'password' : ''
            }
        '''
                
                
        if not os.path.isdir(self.ACC_DATA_PATH):
            os.mkdir(self.ACC_DATA_PATH)
        
        #本地列表是否为空
        with open(f'{self.ACC_DATA_PATH}{ENV_SEP}user_data.yml', 'r+', encoding = 'utf-8') as yml_ini:
            if not yml_ini.read():
                print('Initialized.')
                yaml.dump(['passing'],yml_ini)

        with open(f'{self.ACC_DATA_PATH}{ENV_SEP}user_data.yml', 'r', encoding = 'utf-8') as yml_f:
            ymls = yml_f.read()
            self.acc_dict = yaml.load(ymls, Loader=yaml.Loader)
        

    @property
    def get_stg_accounts(self):
        print(type(self.acc_dict))
        return self.acc_dict

    @property
    def has_login_history(self):
        return True if self.acc_dict else False


    def dump(self, alias, account,pwd = None):

        if pwd is None:
            #防止密码为空时获取上次的密码
            pwd = None

        
        account_data = {
                'alias' : alias,
                'data' : {
                    'account' : account,
                    'password' : pwd,
                    }
                }
    
        self.acc_dict.append(account_data)
    

        with open(f'{self.ACC_DATA_PATH}{ENV_SEP}user_data.yml', 'w') as yml_o:
            yaml.dump(self.acc_dict, yml_o)
                

    def del_account(self, alias):
        pass


class Playlist:

    def __init__(self):
        self.PLAYLIST_DATA_PATH = f'user{ENV_SEP}playlists'
        if not os.path.isdir(self.PLAYLIST_DATA_PATH):
            os.mkdir(self.PLAYLIST_DATA_PATH)
        '''
        storage_format = [
            {
                'id' : int
                'download' : bool
                'data' : {
                    'name' : str
                    'artist' : str
                    'coverUrl' : str
                    'lrcs' : str
                    'album' : str
                    'br' : {
                        'standard' : int
                        'higher' : int
                        'exhigh' : int
                        'lossless' : int
                        'hires' : int
                        }
                    }
                }
            ]
        '''    
    @property
    def get_local_playlists(self):
        return os.listdir(self.PLAYLIST_DATA_PATH)


    def get_playlist_detail(self, playlist_id):
        if f'{playlist_id}.yml' not in self.get_local_playlists:
            raise ValueError(f'playlist {playlist_id} not exist.')
        with open(f'{self.PLAYLIST_DATA_PATH}{ENV_SEP}{playlist_id}.yml', 'r', encoding='utf-8') as playlist_f:
            playlist_data = yaml.load(playlist_f, Loader=yaml.Loader)
        return playlist_data

    def init_playlist_detail(self, playlist_id):
        self.playlist_detail = self.get_playlist_detail(playlist_id)

    def init_playlist_ids_dict(self, playlist_id):
        playlist_d = self.get_playlist_detail(playlist_id)
        self.playlist_id_dict = {track['id'] : track for track in playlist_d}

    def update_playlist(self, playlist_id, new_data):
        if f'{playlist_id}.yml' not in self.get_local_playlists:
            #若该播放列表未本地化
            with open(f'{self.PLAYLIST_DATA_PATH}{ENV_SEP}{playlist_id}.yml', 'w') as new_f:
                yaml.dump(new_data, new_f)
            return None

        self.init_playlist_detail(playlist_id)
        self.init_playlist_ids_dict(playlist_id)
        id_dict = self.playlist_id_dict

        for tracks in new_data:
            if tracks['id'] not in id_dict:
                #以id为唯一标识符检测剔除重复歌曲
                self.playlist_detail.append(tracks)
        with open(f'{self.PLAYLIST_DATA_PATH}{ENV_SEP}{playlist_id}.yml', 'w') as update_f:
            yaml.dump(self.playlist_detail, update_f)



class UpdateDownload():

    def __init__(self, playlist_id):
        self.PLAYLIST_PATH = f'user{ENV_SEP}playlists{ENV_SEP}'
        self.playlist_id = playlist_id

    def __enter__(self):
        #上下文管理器自动保存更新项
        ids_o = Playlist()
        ids_o.init_playlist_detail(self.playlist_id)
        self.playlist_info = ids_o.get_playlist_detail(self.playlist_id)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        #以任何方式退出该上下文管理器都会执行保存，防止漏项
        with open(f'{self.PLAYLIST_PATH}{self.playlist_id}.yml', 'w')as update_f:
            yaml.dump(self.playlist_info, update_f)
        print('updated!')

    def update_download_stat(self, track_id):

        for track_c in range(0,len(self.playlist_info)):
            #遍历曲目id
            if self.playlist_info[track_c]['id'] == track_id:
                self.playlist_info[track_c]['download'] = True


