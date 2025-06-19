from unittest import TestCase
from unittest import main
from clinic.patient_record import *

class PatientRecordTest(TestCase):
    
    def setUp(self):
        self.patient_record = PatientRecord()
        
        
    def test_create_note(self):
        
        expected_note_1 = Note(1, "Patient comes with headache and high blood pressure.")
        
        the_note = self.patient_record.create_note("Patient comes with headache and high blood pressure.")
        
        self.assertIsNotNone(self.patient_record, "the patient record is now not None")
        
        self.assertEqual(the_note, expected_note_1, "The note is expected")
        
        
        
    def test_search_note(self):
        
        expected_note_1 = Note(1, "Patient comes with headache and high blood pressure.")
        expected_note_2 = Note(2, "Patient complains of a strong headache on the back of neck.")
        expected_note_3 = Note(3, "Patient says high BP is controlled, 120x80 in general.")
        
        self.patient_record.create_note("Patient comes with headache and high blood pressure.")
        
        actual_note = self.patient_record.search_note(1)
        
        self.assertIsNotNone(actual_note, "Found a note")
        self.assertEqual(actual_note, expected_note_1, "It is the expected note")
        
        self.patient_record.create_note("Patient complains of a strong headache on the back of neck.")
        
        actual_note = self.patient_record.search_note(2)
        
        self.assertEqual(actual_note, expected_note_2, "could find another note and is eaqul to expected")
        
    def test_retrieve_notes(self):
        
        expected_note_1 = Note(1, "Patient comes with headache and high blood pressure.")
        expected_note_2 = Note(2, "Patient complains of a strong headache on the back of neck.")
        expected_note_3 = Note(4, "Patient feels general improvement and no more headaches.")

        self.patient_record.create_note("Patient comes with headache and high blood pressure.")
        self.patient_record.create_note("Patient complains of a strong headache on the back of neck.")
        self.patient_record.create_note("Patient is taking medicines to control blood pressure.")
        self.patient_record.create_note("Patient feels general improvement and no more headaches.")
        self.patient_record.create_note("Patient says high BP is controlled, 120x80 in general.")

        list = self.patient_record.retrieve_notes("neck")
        self.assertEqual(len(list), 1, "retrieved list of notes has size 1")
        actual_note1 = list[0]
        self.assertEqual(actual_note1, expected_note_2, "retrieved note in the list is note 2")

        list = self.patient_record.retrieve_notes("headache")
        self.assertEqual(len(list), 3, "retrieved list of headache notes from Joe Hancock has size 3")
        self.assertEqual(list[0], expected_note_1, "first retrieved note in the list is note 1")
        self.assertEqual(list[1], expected_note_2, "second retrieved note in the list is note 2")
        self.assertEqual(list[2], expected_note_3, "third retrieved note in the list is note 4")

        list = self.patient_record.retrieve_notes("lungs")
        self.assertEqual(len(list), 0, "list has no size")
        
    def test_update_notes(self):
        

        expected_note_1 = Note(3, "Patient is taking medicines to control blood pressure.")
        expected_note_2 = Note(5, "Patient says high BP is controlled, 120x80 in general.")

        self.patient_record.create_note("Patient comes with headache and high blood pressure.")
        self.patient_record.create_note("Patient complains of a strong headache on the back of neck.")
        self.patient_record.create_note("Patient is taking medicines to control blood pressure.")
        self.patient_record.create_note("Patient feels general improvement and no more headaches.")
        self.patient_record.create_note("Patient says high BP is controlled, 120x80 in general.")

        self.assertTrue(self.patient_record.update_note(3, "Patient is taking Losartan 50mg to control blood pressure."), "update patient record's note")
        
        actual_note = self.patient_record.search_note(3)
        self.assertNotEqual(actual_note, expected_note_1, "note has updated data, cannot be equal to the original data")
        
        expected_note_1a = Note(3, "Patient is taking Losartan 50mg to control blood pressure.")
        self.assertEqual(actual_note, expected_note_1a, "patient was updated, their data has to be updated and correct")
        
        self.assertTrue(self.patient_record.update_note(5, "Patient says high BP is controlled, 120x80 every morning."), "update patient record's note")
        
        actual_note = self.patient_record.search_note(5)
        self.assertNotEqual(actual_note, expected_note_2, "note has updated data, cannot be equal to the original data")
        
        expected_note_2a = Note(5, "Patient says high BP is controlled, 120x80 every morning.")
        self.assertEqual(actual_note, expected_note_2a, "patient was updated, their data has to be updated and correct")
        
    def test_delete_note(self):

        expected_note_1 = Note(1, "Patient comes with headache and high blood pressure.")
        expected_note_2 = Note(2, "Patient complains of a strong headache on the back of neck.")
        expected_note_3 = Note(3, "Patient is taking medicines to control blood pressure.")
        expected_note_4 = Note(4, "Patient feels general improvement and no more headaches.")
        expected_note_5 = Note(5, "Patient says high BP is controlled, 120x80 in general.")

        self.assertFalse(self.patient_record.delete_note(3), "cannot delete note when there are no notes for that patient record in the system")

        self.patient_record.create_note("Patient comes with headache and high blood pressure.")
        self.patient_record.create_note("Patient complains of a strong headache on the back of neck.")
        self.patient_record.create_note("Patient is taking medicines to control blood pressure.")
        self.patient_record.create_note("Patient feels general improvement and no more headaches.")
        self.patient_record.create_note("Patient says high BP is controlled, 120x80 in general.")
        
        self.assertEqual(self.patient_record.search_note(3), expected_note_3, "note is there")
        self.assertTrue(self.patient_record.delete_note(3), "delete patient record's note")
        self.assertIsNone(self.patient_record.search_note(3), "note is gone")

        self.assertEqual(self.patient_record.search_note(2), expected_note_2, "note is there")
        self.assertTrue(self.patient_record.delete_note(2), "delete patient record's note")
        self.assertIsNone(self.patient_record.search_note(2), "note is gone")
        
        self.assertEqual(self.patient_record.search_note(5), expected_note_5, "note is there")
        self.assertTrue(self.patient_record.delete_note(5), "delete patient record's note")
        self.assertIsNone(self.patient_record.search_note(5), "note is gone")
        
    def test_list_notes(self):

        expected_note_1 = Note(1, "Patient comes with headache and high blood pressure.")
        expected_note_2 = Note(2, "Patient complains of a strong headache on the back of neck.")
        expected_note_3 = Note(3, "Patient is taking medicines to control blood pressure.")
        expected_note_4 = Note(4, "Patient feels general improvement and no more headaches.")
        expected_note_5 = Note(5, "Patient says high BP is controlled, 120x80 in general.")

        list = self.patient_record.list_notes()
        self.assertEqual(len(list), 0, "list of notes for patient has size 0")

        self.patient_record.create_note("Patient comes with headache and high blood pressure.")
        list = self.patient_record.list_notes()
        self.assertEqual(len(list), 1, "list of notes for patient has size 1")
        self.assertEqual(list[0], expected_note_1, "Patient comes with headache and high blood pressure.")

        self.patient_record.create_note("Patient complains of a strong headache on the back of neck.")
        self.patient_record.create_note("Patient is taking medicines to control blood pressure.")
        self.patient_record.create_note("Patient feels general improvement and no more headaches.")
        self.patient_record.create_note("Patient says high BP is controlled, 120x80 in general.")

        list = self.patient_record.list_notes()
        self.assertEqual(len(list), 5, "list of notes has size 5")
        self.assertEqual(list[0], expected_note_5, "note 5 is the first in the list of patients")
        self.assertEqual(list[1], expected_note_4, "note 4 is the second in the list of patients")
        self.assertEqual(list[2], expected_note_3, "note 3 is the third in the list of patients")
        self.assertEqual(list[3], expected_note_2, "note 2 is the fourth in the list of patients")
        self.assertEqual(list[4], expected_note_1, "note 1 is the fifth in the list of patients")

        self.patient_record.delete_note(3)
        self.patient_record.delete_note(1)
        self.patient_record.delete_note(5)

        list = self.patient_record.list_notes()
        self.assertEqual(len(list), 2, "list of notes has size 2")
        self.assertEqual(list[0], expected_note_4, "note 4 is the first in the list of notes")
        self.assertEqual(list[1], expected_note_2, "note 2 is the second in the list of notes")
        
    
if __name__ == '__main__':
	unittest.main()