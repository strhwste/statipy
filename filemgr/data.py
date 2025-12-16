import json
from dataclasses import dataclass
from datetime import timedelta
from os import listdir
from typing import Optional

from time import strptime

from .types import History, PlayList


@dataclass
class _MyLibrary:
    liked_songs: list
    liked_albums: list
    liked_shows: list
    liked_episodes: list
    following_artists: list


class MyData:
    _streaming_history: list[History]
    _playlists: list[PlayList]
    _user: None
    _library: _MyLibrary

    def __init__(self, root_path: Optional[str] = None):
        self._root = 'MyData/' if root_path is None else root_path

        self._streaming_history = self._load_streaming_history()
        self._playlists = self._load_playlists()
        self._user = None
        self._library = _MyLibrary(
                *self._load_my_library()
        )

    @property
    def streaming_history(self):
        return self._streaming_history

    @property
    def playlists(self):
        return self._playlists

    @property
    def user(self):
        raise NotImplementedError('Todo')

    @property
    def my_library(self):
        return self._library

    # data loaders (from file)
    def _load_streaming_history(self):
        files = list(filter(lambda x: x.startswith('Streaming_History'), listdir(self._root)))
        files.sort()

        all_ = []
        for file in files:
            with open(self._root + file, encoding='UTF-8') as f:
                data = json.load(f)
                for item in data:
                    # Filter out podcasts and audiobooks
                    if (item.get('master_metadata_track_name') 
                        and not item.get('episode_name') 
                        and not item.get('audiobook_title')):
                        
                        all_.append({
                            'endTime': item['ts'],
                            'artistName': item['master_metadata_album_artist_name'],
                            'albumName': item['master_metadata_album_album_name'],
                            'trackName': item['master_metadata_track_name'],
                            'msPlayed': item['ms_played'],
                            'platform': item['platform'],
                            'connCountry': item['conn_country'],
                            'reasonStart': item['reason_start'],
                            'reasonEnd': item['reason_end'],
                            'shuffle': item['shuffle'],
                            'skipped': item['skipped']
                        })

        # Convert string timestamps to time objects
        for h in all_:
            h['endTime'] = strptime(h['endTime'], '%Y-%m-%dT%H:%M:%SZ')
            h['msPlayed'] = timedelta(milliseconds=h['msPlayed'])

        return all_

    def _load_playlists(self):
        files = list(filter(lambda x: x.startswith('Playlist'), listdir(self._root)))
        files.sort()

        all_ = []
        for file in files:
            with open(self._root + file, encoding='UTF-8') as f:
                all_ += eval(f.read().replace('null', 'None'))['playlists']

        # Convert string timestamps to time objects
        for p in all_:
            p['lastModifiedDate'] = strptime(p['lastModifiedDate'], '%Y-%m-%d')
            for i in p['items']:
                i['addedDate'] = strptime(i['addedDate'], '%Y-%m-%d')

        return all_

    def _load_my_library(self):
        try:
            with open(self._root + 'YourLibrary.json', encoding='UTF-8') as f:
                all_ = eval(f.read())
            return all_['tracks'], all_['albums'], all_['shows'], all_['episodes'], all_['artists']
        except FileNotFoundError:
            return [], [], [], [], []
