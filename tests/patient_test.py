from unittest import TestCase
from unittest import main
from clinic.patient import *

class PatientTest(TestCase):
    
    def setUp(self):
        self.patient = Patient
        
    def test_equal_notes(self):
        
        expected_patient_1 = Patient(987654321, "Kevin Stills", "1980-03-03", "250-814-3333", "kevinstills@gmail.com", "1000 Moss St")
        expected_patient_1a = Patient(987654321, "Kevin Stills", "1980-03-03", "250-814-3333", "kevinstills@gmail.com", "1000 Moss St")
        expected_patient_2 = Patient(9792226666, "Jin Hu", "2002-02-28", "278 222 4545", "jinhu@outlook.com", "200 Admirals Rd, Esquimalt")
        expected_patient_3 = Patient(9798884444, "Ali Mesbah", "1980-03-03", "250 301 6060", "mesbah.ali@gmail.com", "500 Fairfield Rd, Victoria")
        
        self.assertEqual(expected_patient_1, expected_patient_1a, "two patient that are equal")
        self.assertNotEqual(expected_patient_2, expected_patient_3, "two notes that are not equal")
        self.assertEqual(expected_patient_3, expected_patient_3, "The same patient twice")
        
        
    def test_create_note(self):
        
        expected_patient_1 = Patient(987654321, "Kevin Stills", "1980-03-03", "250-814-3333", "kevinstills@gmail.com", "1000 Moss St")
        expected_patient_2 = Patient(9792226666, "Jin Hu", "2002-02-28", "278 222 4545", "jinhu@outlook.com", "200 Admirals Rd, Esquimalt")
        
        self.assertIsNotNone(Patient(987654321, "Kevin Stills", "1980-03-03", "250-814-3333", "kevinstills@gmail.com", "1000 Moss St"))
        
        self.assertEqual(Patient(987654321, "Kevin Stills", "1980-03-03", "250-814-3333", "kevinstills@gmail.com", "1000 Moss St"), expected_patient_1, "First patient created and equals the expected output")
        
        new_patient = Patient(9792226666, "Jin Hu", "2002-02-28", "278 222 4545", "jinhu@outlook.com", "200 Admirals Rd, Esquimalt")
        self.assertEqual(new_patient, expected_patient_2, "a new patient is the same as expected patient 2")
        
        
    def test_update_note(self):
        
        expected_patient_1 = Patient(987654321, "Kevin Stills", "1980-03-03", "250-814-3333", "kevinstills@gmail.com", "1000 Moss St")
        expected_patient_2 = Patient(9792226666, "Jin Hu", "2002-02-28", "278 222 4545", "jinhu@outlook.com", "200 Admirals Rd, Esquimalt")
        expected_patient_3 = Patient(9792226666, "Jin Hu", "2002-02-28", "278 222 4545", "jinhu@outlook.com", "200 Admirals Rd, Esquimalt")
        
        self.assertIsNotNone(expected_patient_1, "expected patient 1 is not None")
        self.assertNotEqual(expected_patient_1, expected_patient_2, "two notes are not the same")
        
        expected_patient_2.update_patient(987654321, "Kevin Stills", "1980-03-03", "250-814-3333", "kevinstills@gmail.com", "1000 Moss St")
        
        self.assertNotEqual(expected_patient_2, expected_patient_3, "After updating the patient is now not the same")
        self.assertEqual(expected_patient_2, expected_patient_1, "After updating the notes are now equal")


if __name__ == '__main__':
	unittest.main()