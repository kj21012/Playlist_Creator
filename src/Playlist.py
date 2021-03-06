'''
Created on Aug 18, 2021

@author: Kwadwo Yeboah
'''
import os
from pathlib import Path
from src.db_lite3 import db

class Song():
    def __init__(self, song_path):
        self.song_path = Path(song_path)
        
        artist, album, title = Path(song_path).parts[-3:]

        self.artist = artist
        self.album = album
        self.title = title
        
    def __str__(self):
        return f'{self.path}\n{self.artist} - {self.album} - {self.track_number}. {self.title}'
    
    def __eq__(self, value):
    
        return self.song_path == value.song_path
    
    def __lt__(self, other):
        return self.__eq__(other)
    
    def __hash__(self):
        return hash((self.song_path))

class Playlist():
    def __init__(self, params):
        '''
        @param (dict) params: Paramaters for Playlist
                            (str) music_directory -> path to music directory
                            (str) playlist_folder -> Folder to 
        '''
        self.params = params
        self.table_name = 'Songs'
         
        if not self.params['music_directory']:
            raise Exception('Music Directory path is empty')

        required_variables = { param : list() for param in ['include_extension', 'exclude_folder']}
        
        required_variables.update(self.params)
        
        for var, value in required_variables.items():
            
            if value:
                setattr(self, var, value)
            else:
                setattr(self, var, list())
        
        self.db = db()
        try:
            self.db = db(params['db_name'])
        except:
            pass
        
        self.keys = ['path', 'artist', 'album', 'title']
        self.types = ['text' for i in range(4)]
        
        self.db.create_table(self.table_name, self.keys, self.types)
        
        self.songs = self.scan()
        self.new_songs = self.updated_db()
        self.db.save_to_db('Songs', self.new_songs)
        
    def scan(self):
        songs = []
        for root, dirs, files in os.walk(self.music_directory):
            if files:
                for file in files:
                    extension = file.split('.')[1]
                    
                    if not root in self.exclude_folder and extension in self.include_extension:
                        path = os.path.join(root, file)
                        songs.append(path)
                            
        return songs
    
    def get_songs_in_db(self):
        self.db.cur.execute('SELECT path FROM Songs')
        paths = list(self.db.cur.fetchall())
        
        return { Song(song_path[0]) : index for index, song_path in enumerate(paths)}
            
    def updated_db(self):
        songs = { Song(path) : index for index, path in enumerate(self.songs)}
        
        diff = songs.keys() - self.get_songs_in_db().keys()
        sorted_difference = list(sorted({ index : song for song, index in enumerate(diff)}))
        
        return [(str(song.song_path), song.artist, song.album, song.title) for song in sorted_difference]
    
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
            song_paths = self.db.cur.execute('SELECT path FROM Songs WHERE album = ?', tup_album)
            songs.extend(song_paths)
        
        return [Song(path[0]) for path in songs]
    
    
    def generate_playlist(self, output_directory, playlist_name, song_path = '..', songs = []):
        '''
        @param (str) playlist_name
        @param (str) output_directory - Defaults to relative directory unless absolute path is given
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
        
        