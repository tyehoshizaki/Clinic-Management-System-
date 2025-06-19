import os
from .patient import Patient
from clinic.dao.patient_dao_json import PatientDAOJSON
from .note import Note
from .patient_record import PatientRecord
from clinic.exception.invalid_login_exception import InvalidLoginException
from clinic.exception.duplicate_login_exception import DuplicateLoginException
from clinic.exception.invalid_logout_exception import InvalidLogoutException
from clinic.exception.illegal_access_exception import IllegalAccessException
from clinic.exception.illegal_operation_exception import IllegalOperationException
from clinic.exception.no_current_patient_exception import NoCurrentPatientException
import hashlib

class Controller:

    def __init__(self, autosave=False):
        """
        the controllers constructer with the current user, current patient, a dictionary of users and a dictionary of patients
        """
        self.autosave = autosave
        self.current_user = None
        self.current_patient = None
        
        if autosave:
            self.users = self.load_users()
        else:
            self.users = {
                "user": "123456",
                "ali": "@G00dPassw0rd"
            }
        
        self.logedin = False
        self.have_current_patient = False

        self.patient_dao = PatientDAOJSON(self.autosave)
        
        
        
    def load_users(self):
        
        users = {}
        
        dir_path = os.path.dirname(__file__)
        file_path = os.path.join(dir_path, 'users.txt')
        
        with open(file_path, 'r') as file:
            for line in file:
                user, password_hash = line.strip().split(',')
                users[user] = password_hash
                
        return users
    
    def get_password_hash(self, password):

        encoded_password = password.encode('utf-8')
        hash_object = hashlib.sha256(encoded_password)
        hex_dig = hash_object.hexdigest()
        return hex_dig
                

    def login(self, username, password):
        """
        allows users to login if they have the correct password

        Returns:
            True if loged in
            False if they could not be loged in
        """
        
        if self.logedin:
            raise DuplicateLoginException("Already Logged in")
        
        if self.autosave:
            password_hash = self.get_password_hash(password)
        else:
            password_hash = password
        
        if not username in self.users or not self.users[username] == password_hash:
            raise InvalidLoginException("Invalid Username or Password")

        if username in self.users and self.users[username] == password_hash and not self.logedin:
            self.current_user = username
            self.logedin = True
            return True

    def logout(self):
        """
        allows user to logout

        Returns:
            True if could be loged out
            False if could not be loged out
        """

        if not self.logedin:
            raise InvalidLogoutException("Already Lodded out")

        else:
            self.unset_current_patient()
            self.current_user = None
            self.logedin = False
            self.have_current_patient = False
            return True

    def search_patient(self, PHN):
        """
        searches for a patient based on the PHN

        Returns:
            The patient if they could be located
            None if no patient coould be found
        """
        if not self.logedin:
            raise IllegalAccessException("Not Logged in")

        return self.patient_dao.search_patient(PHN)

    def create_patient(self, PHN, name, birth_date, phone, email, address):
        """
        Creates a patient and add them to the dictionary of patients

        Returns:
            the patient if could be created
            None if patient coulf not be created
        """

        if not self.logedin:
            raise IllegalAccessException("Not Logged in")

        if self.patient_dao.search_patient(PHN):
            raise IllegalOperationException("PHN Already Registered")

        return self.patient_dao.create_patient(Patient(PHN, name, birth_date, phone, email, address, self.autosave))

    def retrieve_patients(self, name):
        """
        retrieves a list of patients if the provided name is the same as some patients in the dictionary
        
        Returns:
            A list
        """

        if not self.logedin:
            raise IllegalAccessException("Not Logged in")

        return self.patient_dao.retrieve_patients(name)

    def update_patient(self, key, PHN, name, birth_date, phone, email, address):
        """
        Updates a patients PHN, name, birthday, phonem email, and address

        Returns:
            True if patient could be updated
            False if patient could not be updated
        """

        if not self.logedin:
            raise IllegalAccessException("Not Logged in")
        
        if not self.patient_dao.search_patient(key):
            raise IllegalOperationException("Invaild PHN")
        
        if self.have_current_patient:
            if self.current_patient.PHN == key:
                raise IllegalOperationException("Cannot Update Current Patient")
        
        return self.patient_dao.update_patient(key, Patient(PHN, name, birth_date, phone, email, address))

    def delete_patient(self, PHN):
        """
        deletes patient from dictionary with PHN
        
        Returns:
            True if they could be deleted
            False if they could not be deleted
        """

        if not self.logedin:
            raise IllegalAccessException("Not Logged in")
        
        if not self.patient_dao.search_patient(PHN):
            raise IllegalOperationException("Invaild PHN")

        if self.have_current_patient:
            if self.current_patient.PHN == PHN:
                raise IllegalOperationException("Cannot Delete Current Patient")
        
        return self.patient_dao.delete_patient(PHN)

    def list_patients(self):
        """
        Provides a full list of patients in the dictionary

        Returns:
            A list of patients
        """

        if not self.logedin:
            raise IllegalAccessException("Not Logged in")

        return self.patient_dao.list_patients()

    def set_current_patient(self, PHN):
        """
        Sets a current patient base on the PHN

        Returns:
            True if could set a current patient
            None if no patient could be set
        """

        if not self.logedin:
            raise IllegalAccessException("Not Logged in")
        
        if not self.search_patient(PHN):
            raise IllegalOperationException("Invaild PHN")
        
        self.current_patient = self.search_patient(PHN)
        self.have_current_patient = True
        return True
    
    def get_current_patient(self):
        """
        gets the current patient

        Returns:
            The current patient
            None if no current patient
        """
        
        if not self.logedin:
            raise IllegalAccessException("Not Logged in")
        
        return self.current_patient
    
    def unset_current_patient(self):
        """
        Sets current patient to None

        Returns:
            False if could set current patient to None
            True if could set current patient to None
        """
        
        if not self.logedin:
            raise IllegalAccessException("Not Logged in")
        
        self.current_patient = None
        self.have_current_patient = False
            
        return True

    def create_note(self, text):
        """
        Creates a note for current patient

        Returns:
            Note if note could be created
            None if note could not be created
        """
        
        if not self.logedin:
            raise IllegalAccessException("Not Logged in")
        
        if not self.have_current_patient:
            raise NoCurrentPatientException("Current Patient Not Set")
        
        return self.current_patient.create_note(text)
    
    def search_note(self, code):
        """
        Looks for note with note's code

        Returns:
            The note if could be found
            None if note could not be found
        """
        
        if not self.logedin:
            raise IllegalAccessException("Not Logged in")
        
        if not self.have_current_patient:
            raise NoCurrentPatientException("Current Patient Not Set")
        
        return self.current_patient.search_note(code)

    def retrieve_notes(self, text):
        """
        retrieves all notes that have text in the note's text
        
        Returns:
           A list of Notes
        """
        
        if not self.logedin:
            raise IllegalAccessException("Not Logged in")
        
        if not self.have_current_patient:
            raise NoCurrentPatientException("Current Patient Not Set")
        
        return  self.current_patient.retrieve_notes(text)

    def update_note(self, code, text):
        """
        updates note's text

        Returns:
            True if note could be updated
            False if note could not be updated
        """
        
        if not self.logedin:
            raise IllegalAccessException("Not Logged in")
        
        if not self.have_current_patient:
            raise NoCurrentPatientException("Current Patient Not Set")
        
        return self.current_patient.update_note(code, text)
        
    def delete_note(self, code):
        """
        deletes note from patient record
        
        Returns:
            True if note could be deleted
            False if note could not be deleted
        """

        if not self.logedin:
            raise IllegalAccessException("Not Logged in")
        
        if not self.have_current_patient:
            raise NoCurrentPatientException("Current Patient Not Set")
        
        return self.current_patient.delete_note(code)
    
    def list_notes(self):
        """
        Provides a list of note from current patient's record

        Returns:
            A list of notes
        """
        
        if not self.logedin:
            raise IllegalAccessException("Not Logged in")
        
        if not self.have_current_patient:
            raise NoCurrentPatientException("Current Patient Not Set")
        
        return self.current_patient.list_notes()
