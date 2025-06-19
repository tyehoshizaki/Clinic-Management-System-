from json import JSONEncoder
from clinic.patient import Patient
from clinic.patient_record import PatientRecord

class PatientEncoder(JSONEncoder):
    
    def default(self, obj):
        
        if isinstance(obj, Patient):
            return {
                "__type__": "Patient",
                "PHN": obj.PHN,
                "name": obj.name,
                "birth_date": obj.birth_date,
                "phone": obj.phone,
                "email": obj.email,
                "address": obj.address,
                "autosave": obj.autosave

            }
        
        return super().default(obj)