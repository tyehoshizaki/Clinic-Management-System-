from unittest import TestCase
from unittest import main
from clinic.note import *

class NoteTests(TestCase):
    
    def setUp(self):
        self.note = Note
        
    def test_equal_notes(self):
        
        expected_note_1 = Note(1, "Patient comes with headache and high blood pressure.")
        expected_note_1a = Note(1, "Patient comes with headache and high blood pressure.")
        expected_note_2 = Note(2, "Patient complains of a strong headache on the back of neck.")
        expected_note_3 = Note(3, "Patient is taking medicines to control blood pressure.")
        
        self.assertEqual(expected_note_1, expected_note_1a, "two note that are equal")
        self.assertNotEqual(expected_note_2, expected_note_3, "two notes that are not equal")
        self.assertEqual(expected_note_3, expected_note_3, "The same note twice")
        
        
    def test_create_note(self):
        
        expected_note_1 = Note(1, "Patient comes with headache and high blood pressure.")
        expected_note_2 = Note(2, "Patient complains of a strong headache on the back of neck")
        
        self.assertIsNotNone(Note(1, "Patient comes with headache and high blood pressure."), "A new note is not None")
        
        self.assertEqual(Note(1, "Patient comes with headache and high blood pressure."), expected_note_1, "First note created and equals the expected output")
        
        new_note = Note(2, "Patient complains of a strong headache on the back of neck")
        self.assertEqual(new_note, expected_note_2, "a new note is the same as expected note 2")
        
        
    def test_update_note(self):
        
        expected_note_1 = Note(1, "Patient comes with headache and high blood pressure.")
        expected_note_2 = Note(1, "Patient complains of a strong headache on the back of neck.")
        expected_note_3 = Note(2, "Patient complains of a strong headache on the back of neck.")
        
        self.assertIsNotNone(expected_note_1, "expected note 1 is not None")
        self.assertNotEqual(expected_note_1, expected_note_2, "two notes are not the same")
        
        expected_note_2.update_note("Patient comes with headache and high blood pressure.")
        
        self.assertNotEqual(expected_note_2, expected_note_3, "After updating the note is now not the same")
        self.assertEqual(expected_note_2, expected_note_1, "After updating the notes are now equal")




if __name__ == '__main__':
	unittest.main()