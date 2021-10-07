'''
Created on Oct 7, 2021

@author: kjyeb
'''
import os
import shutil
import unittest

from pathlib import Path
from src import Playlist
from src.Playlist import Song
from src.db_lite3 import db


test_kwargs = {'music_directory' : r'C:\Users\kjyeb\Documents\Liclipse Music Directory\Playlists Creator Test',
'playlist_folder' : r'C:\Users\kjyeb\Music\Generated_Playlists', 'include_extension' : ['mp3'],
'db_name' : ':memory:'}
 
class Test(unittest.TestCase):

    def testDb_Delete(self):
        play = Playlist(test_kwargs)
        
        backup_song = play.songs_in_db[0]
        
        file_dst = r'C:\Users\kjyeb\Documents\Liclipse Music Directory\Backed up song.mp3'
        shutil.copy2(backup_song.song_path, file_dst)
        
        os.remove(backup_song.song_path)
        
        play.scan()
        
        second_scan = play.get_songs_in_db()
        
        self.assertTrue( backup_song in set(second_scan))
        
        
        
        
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testDb_Delete']
    unittest.main()