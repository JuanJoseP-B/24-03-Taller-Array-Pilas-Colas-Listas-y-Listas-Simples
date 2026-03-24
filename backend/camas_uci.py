class ICUBeds:
    """
    Arrays: Represents the ICU (Intensive Care Unit) beds.
    Fixed size (e.g. 15 beds). Fast O(1) index-based access
    to check if a bed is free or occupied by a patient.
    """
    def __init__(self, capacity=15):
        self.capacity = capacity
        self.beds = [None] * capacity

    def assign_bed(self, index, patient):
        if 0 <= index < self.capacity:
            if self.beds[index] is None:
                self.beds[index] = patient
                return True, f"Cama {index} asignada a {patient}."
            return False, f"La cama {index} ya esta ocupada por {self.beds[index]}."
        return False, f"Indice {index} fuera de rango."

    def release_bed(self, index):
        if 0 <= index < self.capacity:
            if self.beds[index] is not None:
                patient = self.beds[index]
                self.beds[index] = None
                return True, f"Cama {index} liberada. Paciente {patient} dado de alta."
            return False, f"La cama {index} ya estaba libre."
        return False, f"Indice {index} fuera de rango."

    def get_state(self):
        return self.beds
