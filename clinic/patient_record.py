from .note import Note
from clinic.dao.note_dao_pickle import NoteDAOPickle
class PatientRecord:
    
    def __init__(self, PHN, autosave=False):
        """
        Constructor for a patients record
        """

        self.notes_dao = NoteDAOPickle(PHN, autosave)
        
    def search_note(self, code):
        """
        Searches for a note based off the code

        Returns:
            The note if could be found
            None if no note with code could be found
        """
        
        return self.notes_dao.search_note(code)
        
    def create_note(self, text):
        """
        creates a note and adds to patients record

        Returns:
            Note if note could be created
        """
        
        return self.notes_dao.create_note(text)
    
    def retrieve_notes(self, text):
        """
        retrieves notes with a certain text within the note

        Returns:
            A list of notes
        """
        
        return self.notes_dao.retrieve_notes(text)
    
    def update_note(self, code, text):
        """
        updates note with new text


        Returns:
            False if note could not be updated
            True if note could be updated
        """
        
        return self.notes_dao.update_note(code, text)
        
    def delete_note(self, code):
        """
        deletes note from patient's record
        
        Returns:
            False if note could not be deleted
            True if note could be deleted
        """
        
        return self.notes_dao.delete_note(code)
    
    def list_notes(self):
        """
        gets a list of notes from patients record

        Returns:
            A list of notes from highest code to lowest code
        """

        return self.notes_dao.list_notes()
        