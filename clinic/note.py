import datetime
class Note:
    
    def __init__(self, code, text):
        """
        Constructor for a note

        """
        self.code = code
        self.text = text
        
        now = datetime.datetime.now()
        self.timestamp = now.strftime("%H:%M, %d, %B, %Y")
        
    def update_note(self, text):
        """
        updates a note with new text and changes the timestamp of the note

        Returns:
            True if note could be updated
        """
        self.text = text
        
        now = datetime.datetime.now()
        self.timestamp = now.strftime("%H:%M, %d, %B, %Y")
        return True
        
    def __eq__(self, other):
        """
        Notes are equal if 
        Code is the same
        Text is the same

        Returns:
            True if notes are the same
            False if notes are not the same
        """
        return self.code == other.code and self.text == other.text
    
    def __str__(self):

        return f"Note #{self.code}, '{self.text}', Timestamp: {self.timestamp}"

    def __repr__(self):

        return f"Note(code={self.code!r}, text={self.text!r}, timestamp={self.timestamp!r})"