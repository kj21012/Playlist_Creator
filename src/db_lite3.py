'''
Created on Jun 29, 2021

@author: kjyeb
'''

import sqlite3
from pprint import pprint

class db():
    def __init__(self, name = ':memory:'):
        self.connection = sqlite3.connect(name)
        self.cursor = self.connection.cursor()
        
        self.cur = self.cursor
        
        self.tables = {}
        
    def save_to_db(self, table_name, values):
        '''
        @param table_name: (str) Table name in db
        @param values: (list) [ row for row in values]
        '''
        if table_name:
            if values:
                if isinstance(values, list):
                    question_marks = ''
                    for row in values:
                        question_marks = ','.join( '?' * len(row))
                        exe = f'INSERT INTO {table_name} VALUES ({question_marks})'
                    
                        self.cur.execute(exe, row)
                        self.connection.commit()
                else:
                    raise Exception(f'{values} is not a list')
                
            else:
                raise Exception(f'Values is empty')
            
        else:
            raise Exception('Table name is empty')
        
    def create_table(self, table_name = '', keys = [], types = [], drop_existing_table = True):
        '''
        SQLite3 types:
        NULL None 
        INTEGER int 
        REAL float 
        TEXT depends on text_factory, str by default 
        BLOB bytes 

        @param keys: tuple (str) key = column name 
        @param types: tuple (SQlite type) type
        '''    
        if not table_name:
            raise Exception('Table name is empty')
        
        if drop_existing_table and table_name in self.tables:
            dropped = self.drop_table(table_name)
            print(f'Dropped Table {table_name} {dropped}')
                
                
        key_type = ','.join([f'{key} {typed}' for key, typed in zip(keys, types)])
        key_type = '(' + key_type + ')'
        
        exe = f'''CREATE TABLE IF NOT EXISTS {table_name} {key_type}'''
        
        self.cur.execute(exe)

        self.connection.commit()
        
        self.tables[table_name] = [keys, types]
    
    def print_table(self, table_name):
        print(f'Table {table_name}')
        self.cur.execute(f'SELECT * FROM {table_name}')
        pprint(self.cur.fetchall())

    def print_db(self, tables = []):
        for table in tables:
            self.print_table(table)

