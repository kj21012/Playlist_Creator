'''
Created on Aug 18, 2021

@author: kjyeb
'''
import os
from pathlib import Path
from pprint import pprint

from music_tag import load_file

from src.db_lite3 import db


class Song():
    def __init__(self, song_path):
        self.song_path = Path(song_path)
        
        artist, album, title = Path(song_path).parts[-3:]
        
        self.artist = artist
        self.album = album
        self.title = title
        
        self.track_number = load_file(song_path)['tracknumber'].value

    def __str__(self):
        return f'{self.path}\n{self.artist} - {self.album} - {self.track_number}. {self.title}'
    
class Playlist():
   
    def __init__(self, params):
        '''
        @param param: (dict)  
        '''
        self.params = params
         
        if not params['music_directory']:
            raise Exception('Music Directory path is empty')
        
        if not params['playlist_folder']:
            params['playlist_folder'] = Path(os.getcwd(), 'Playlist_Folder')
            
        required_variables = { param : list() for param in ['include_extension', 'exclude_folder']}

        
        required_variables.update(self.params)
        
        for var, value in required_variables.items():
            
            if value:
                setattr(self, var, value)
            else:
                setattr(self, var, list())
        
        self.table_name = 'Songs'
        
        
        self.db = db()
        
        self.keys = ['track_number', 'path', 'artist', 'album', 'title' ]
        text_types = ['text' for i in range(4)]
        self.types = ['integer']
        self.types.extend(text_types)
        
        self.db.create_table(self.table_name, self.keys, self.types)
        self.db.cur.execute('SELECT path FROM SONGS')
        self.in_db = list(self.db.cur.fetchall())
        
        self.scan()

        
    def scan(self):

        songs = []
        for root, dirs, files in os.walk(self.music_directory):
            if files:

                for file in files:
                    extension = file.split('.')[1]
                    
                    if not root in self.exclude_folder:
                        if extension in self.include_extension:
                            path = os.path.join(root, file)
                            songs.append(path)
                            
                            
        songs = [Song(path) for path in songs]
        compare_songs = songs.copy()       
        
        for db_value, song_value in zip(self.in_db, compare_songs):
            if db_value == song_value.path:
                del(db_value)
                del(song_value)              
        
        if not len(self.in_db) > 0:
        
            values = [ (song.track_number, song.path, song.artist, song.album, song.title) for song in songs]
            self.db.save_to_db('Songs', values)
    
    def get_all_artists(self):
        
        return self.get_artists([artist for artist in os.listdir(self.music_directory)])

    def get_artists(self, artists = []):
        songs = []
        
        for artist in artists:
            tup_artist = (artist,)
            song_paths = self.db.cur.execute('SELECT path FROM SONGS WHERE artist = ?', tup_artist)
            songs.extend(song_paths)
        
        return [Song(path[0]) for path in songs]
    
    def get_albums(self, albums = []):
        songs = []
        
        for album in albums:
            tup_album = (album,)
            song_paths = self.db.cur.execute('SELECT path FROM SONGS WHERE album = ?', tup_album)
            songs.extend(song_paths)
        
        return [Song(path[0]) for path in songs]
    
    def generate_playlist(self, output_directory, playlist_name, song_path = '..', songs = []):
        '''
        @param (str) playlist_name
        @param (str) playlist_folder - Defaults to relative directory unless absolute path is given
        @param (list(Song)) songs
        @return True on success
        '''
        out_path = Path(output_directory)
        
        
        if not out_path.exists():
            os.makedirs(out_path, 777, exist_ok = True)
        
        entries = []
        for song in songs:
            path = str(Path(song_path, '/'.join(song.song_path.parts[-3:])))
            entries.append(path)
            
        playlist_file = str(out_path.joinpath(playlist_name)) + '.m3u'
        
        with open(playlist_file, 'w') as writer:
            writer.writelines([ song + '\n' for song in entries])
        
        if os.path.exists(playlist_file):
            return True 
        else:
            return False
        
