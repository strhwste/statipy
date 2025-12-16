import os
from zipfile import ZipFile

from .data import MyData


def _extract_data(path: str) -> None:
    if not os.path.exists('Spotify Extended Streaming History'):
        with ZipFile(path) as zip_:
            # todo: check extracted location & modifiable root path
            zip_.extractall()


def load_zipped_data(path: str = 'my_spotify_data.zip') -> MyData:
    """
    Loads a zipped Spotify Data Package into a MyData object and returns it.

    :param path: relative path to zip file ('my_spotify_data.zip' default)
    """
    _extract_data(path)
    return MyData(root_path='Spotify Extended Streaming History/')
