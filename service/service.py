import os as os
import spotipy as spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class Service:


    def __init__(self, user_token):
        self.sp = spotipy.Spotify(auth = user_token)

    def get_my_playlists(self):
        playlist_ids = pd.DataFrame(
        data = [(i['name'], i['id']) for i in self.sp.current_user_playlists()['items']],
        columns = ['name', 'id']
        )
        return playlist_ids