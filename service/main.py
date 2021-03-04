import os as os
import spotipy as spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#auth
#do I need to change this when working with other users?
client_id = 'c37b8f11ab1042f79eb1b6b443e52a68'
client_secret = '655ca06a0fcb4255883a11cfa4c33b0b'
user_id = '123998761' #<--enter user_id for individual - eventually get user input - login redirect would be ideal

os.environ['SPOTIPY_CLIENT_ID'] = client_id
os.environ['SPOTIPY_CLIENT_SECRET'] = client_secret

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())


#retrieve and print list of user playlists
playlist_ids = pd.DataFrame(
    data = [(i['name'], i['id']) for i in spotify.user_playlists(user_id)['items']],
    columns = ['name', 'id']
)

print()
print(playlist_ids.name.head(15))
print()

#allow user to select playlist
selected = int(input('Enter the index of the selected playlist: '))

#retrieve track and ids from playlist
playlist_id = playlist_ids.loc[selected, 'id']
playlist_name = playlist_ids.loc[selected, 'name']

print('\nYou have selected \"{}\", Retrieving playlist information...'.format(playlist_name))

#retrieve list of tracks and ids of selected playlist
playlist_tracks = pd.DataFrame(
    data=[(i['track']['name'], i['track']['id']) for i in spotify.playlist_items(playlist_id)['items']],
    columns = ['track', 'id']
)

missing_ids = playlist_tracks[playlist_tracks['id'].isna()]

if missing_ids.shape[0] > 0:
    print('\nThere are {} songs in the selected playlist for which a spotify id could not be found...'.format(missing_ids.shape[0]))
    missing_bool = input('Would you like to see a list of these songs? [y/n]: ')
    if missing_bool == 'y':
        print()
        print(missing_ids.track)

playlist_tracks = playlist_tracks[playlist_tracks['id'].notna()].reset_index(drop=True)
print('Getting track features...\n')

#create comma-separated list of track ids to pass to sp.audio_features()
a=''
for i in range(0, playlist_tracks.shape[0]):
    a += playlist_tracks.loc[i, 'id'] + ','
a = a[:-1]

#read in list of audio features as DataFrame
pl_audio_features = pd.DataFrame(spotify.audio_features(a)).iloc[:, :10]

#join audio_features with playlist_tracks
playlist_feature_matrix = playlist_tracks.join(pl_audio_features)

print()
print(playlist_feature_matrix)

ax_to_feature = {
    '00': 'danceability',
    '01': 'energy',
    '02': 'loudness',
    '10': 'speechiness',
    '11': 'acousticness',
    '12': 'instrumentalness',
    '20': 'key',
    '21': 'liveness',
    '22': 'valence'
}

fig, ax = plt.subplots(3,3)
#plt.tight_layout()

for i in range(3):
    for j in range(3):
        ax[i][j].hist(playlist_feature_matrix[ax_to_feature[str(i) + str(j)]])
        ax[i][j].set_xticks([])
        ax[i][j].set_yticks([])
        ax[i][j].set_title(ax_to_feature[str(i) + str(j)])

fig.savefig('/home/mike/test_project/' + playlist_name.replace(' ', '') + '.png')