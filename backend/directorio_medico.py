class MedicalDirectory:
    """
    Native Lists: Maintains the directory of on-duty medical staff,
    allowing dynamic addition, removal and search of doctors
    during shift changes.
    """
    def __init__(self):
        self.doctors = []

    def add_doctor(self, name, specialty):
        for doc in self.doctors:
            if doc["name"] == name and doc["specialty"] == specialty:
                return False, f"El doctor/a {name} ({specialty}) ya esta en el directorio."

        new_doctor = {"name": name, "specialty": specialty}
        self.doctors.append(new_doctor)
        return True, f"Dr/a. {name} ({specialty}) agregado al turno."

    def remove_doctor(self, name):
        for doc in self.doctors:
            if doc["name"] == name:
                self.doctors.remove(doc)
                return True, f"Dr/a. {name} removido del turno."
        return False, f"Dr/a. {name} no se encontro en el directorio."

    def search_doctor(self, term):
        term = term.lower()
        results = [
            doc
            for doc in self.doctors
            if term in doc["name"].lower() or term in doc["specialty"].lower()
        ]
        return results

    def get_state(self):
        return self.doctors
