import os
from pickle import load, dump
from .note_dao import NoteDAO
from clinic.note import Note

class NoteDAOPickle(NoteDAO):
    
    def __init__(self, PHN, autosave=False):
        
        self.autosave = autosave
        
        self.autocounter = 0
        self.notes = {}
        self.PHN = PHN
        self.file = os.path.join(os.getcwd(), 'clinic/records/', f'{PHN}.dat')
        
        if self.autosave:
            try:
                with open(self.file, 'rb') as file:
                    self.notes = load(file)
                self.autocounter = len(self.notes)
            except FileNotFoundError:
                self.notes = {}
        else:
            self.notes = {}
        
        
    def search_note(self, key):
        if not key in self.notes:
            return None
        
        return self.notes[key]
    
    def create_note(self, text):
        
        self.autocounter += 1
        key = self.autocounter
        
        self.notes[key] = Note(key, text)
        
        if self.autocounter:
            with open(self.file, 'wb') as file:
                dump(self.notes, file)
                
        return self.notes[key]
    
    def retrieve_notes(self, search_string):
        note_list = []
        
        for note in self.notes.values():
            if search_string in note.text:
                note_list.append(note)
        
        return note_list
    
    def update_note(self, key, text):
        if not key in self.notes:
            return False
        
        self.notes[key].update_note(text)
        
        if self.autosave:
            with open(self.file, 'wb') as file:
                dump(self.notes, file)
        
        return self.notes[key]
    
    def delete_note(self, key):
        
        if not self.search_note(key):
            return False
        
        del self.notes[key]
        
        if self.autosave:
            with open(self.file, 'wb') as file:
                dump(self.notes, file)
        
        return True
    
    def list_notes(self):
        
        return list(self.notes.values())[::-1]