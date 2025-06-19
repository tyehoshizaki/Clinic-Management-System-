import json
import os
from .patient_dao import PatientDAO
from clinic.exception.illegal_operation_exception import IllegalOperationException
from .patient_decoder import PatientDecoder
from .patient_encoder import PatientEncoder

class PatientDAOJSON(PatientDAO):
    
    def __init__(self, autosave=False):
        
        self.autosave = autosave
        
        if self.autosave:
            self.patients = self.load_patients()
            self.patients = {int(key): patient for key, patient in self.patients.items()}
            
        else:
            self.patients = {}
        
    def load_patients(self):
        
        patients_file = 'clinic/records/patients.json'
        
        patients = {}
        try:
            with open(patients_file, 'r+') as file:
                patients = json.load(file, cls=PatientDecoder)
        except FileNotFoundError:
            with open(patients_file, 'w+') as file:
                json.dump({}, file)
            
        return patients
            
    def save_patients(self):
        
        patients_file = 'clinic/records/patients.json'
        
        with open(patients_file, 'w+') as file:
            json.dump(self.patients, file, cls=PatientEncoder, indent=4)

    def search_patient(self, key):
        
        return self.patients.get(key)
    
    def create_patient(self, patient):
        
        if not self.search_patient(patient.PHN):

            self.patients[patient.PHN] = patient
            if self.autosave:
                self.save_patients()
                
            return patient

        else:
            return None
    
    def retrieve_patients(self, name):
        
        retrieved_patients = []

        for patient in self.patients.values():
            if name in patient.name:
                retrieved_patients.append(patient)

        return retrieved_patients
    
    def update_patient(self, key, patient):

        if key == patient.PHN:
            self.patients[key].update_patient(patient.PHN, patient.name, patient.birth_date, patient.phone, patient.email, patient.address)
            if self.autosave:
                self.save_patients()
                
            return True

        else:
            if self.search_patient(patient.PHN):
                raise IllegalOperationException("Cannot Have Same PHN as Existing Patient")
            
            new_patient = self.patients.pop(key)
            new_patient.update_patient(patient.PHN, patient.name, patient.birth_date, patient.phone, patient.email, patient.address)
            self.patients[patient.PHN] = new_patient
            if self.autosave:
                self.save_patients()
                
            return True
    
    def delete_patient(self, key):
        for note in self.patients[key].list_notes():
            self.patients[key].delete_note(note.code)
        
        del self.patients[key]
        if self.autosave:
            self.save_patients()
            
        return True
    
    def list_patients(self):
        
        list_of_patients = []
        for patients in self.patients.values():
            list_of_patients.append(patients)

        return list_of_patients

