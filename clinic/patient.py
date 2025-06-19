from .patient_record import PatientRecord
class Patient:
    
    def __init__(self, PHN, name, birth_date, phone, email, address, autosave=False):
        """
        Constructor for a Patient
        
        """
        self.autosave = autosave
        
        self.PHN = PHN
        self.name = name
        self.birth_date = birth_date
        self.phone = phone
        self.email = email
        self.address = address

        self.patient_record = PatientRecord(PHN, self.autosave)
        
        
    def update_patient(self, PHN, name, birth_date, phone, email, address):
        """
        Updates a Patient

        """
        
        self.PHN = PHN
        self.name = name
        self.birth_date = birth_date
        self.phone = phone
        self.email = email
        self.address = address
        
    def create_note(self, text):
        
        return self.patient_record.create_note(text)
    
    def search_note(self, code):
        
        return self.patient_record.search_note(code)

    def retrieve_notes(self, text):
        
        return self.patient_record.retrieve_notes(text)

    def update_note(self, code, text):
        
        return self.patient_record.update_note(code, text)
        
    def delete_note(self, code):
        
        return self.patient_record.delete_note(code)

    def list_notes(self):
        
        return self.patient_record.list_notes()

    def __eq__(self, other):
        """
        Patients are equal if
        PHN is same
        Name is same
        Birth date is same
        Phone is same
        email is same
        and address is same

        Returns:
            True if patients are same 
            False if patient are not the same
        """
        
        return self.PHN == other.PHN and \
            self.name == other.name and \
            self.birth_date == other.birth_date and \
            self.phone == other.phone and \
            self.email == other.email and \
            self.address == other.address
            
    def __str__(self):
        return (f"Patient(PHN: {self.PHN}, Name: {self.name}, Birth Date: {self.birth_date}, "
                f"Phone: {self.phone}, Email: {self.email}, Address: {self.address})")
        
    def __repr__(self):
        return (f"Patient(PHN={self.PHN!r}, name={self.name!r}, birth_date={self.birth_date!r}, "
                f"phone={self.phone!r}, email={self.email!r}, address={self.address!r})")
