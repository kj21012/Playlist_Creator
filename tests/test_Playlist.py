'''
Created on Aug 18, 2021

@author: kjyeb
'''
import os
from pathlib import Path
from pprint import pprint
import unittest

from src.Playlist import Playlist, Song


test_kwargs = {'music_directory' : r'C:\Users\kjyeb\Documents\Liclipse Music Directory\Playlists Creator Test',
    'playlist_folder' : r'C:\Users\kjyeb\Music\Generated_Playlists', 'include_extension' : ['mp3'],
    'db_name' : ':memory:'}
     
    
class Test(unittest.TestCase):
            
    def test_get_single_artist(self):
        test_artist = ['Yelawolf']
        play = Playlist(test_kwargs)
        
        fin = []
        for root, dirs, files in os.walk(play.music_directory):
            if files:
                fin = [ Song(os.path.join(root,file)) for file in files]
        fin = set(fin)
        self.assertSetEqual(set(play.get_artists(test_artist)), fin)
        
    def test_get_all_artists(self):
        play = Playlist(test_kwargs)
    
        end = []
        for root, dirs, files in os.walk(play.music_directory):
            if files:
                end.extend([ Song(os.path.join(root,file)) for file in files])
            
                
        self.assertSetEqual(set(play.get_all_artists()), set(end))
    
        
    def test_get_albums(self):
        play = Playlist(test_kwargs)
        albums = ['Trunk Muzik', 'Single']
        end = []
        for root, dirs, files in os.walk(play.music_directory):
            if files:
                end.extend([ Song(Path(root,file)) for file in files])
                
        
        ans = set( path for path in play.get_albums(albums))
        self.assertSetEqual( ans, set(end))
    
            

    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_scan']
    unittest.main()