from .camas_uci import ICUBeds
from .cola_espera import WaitingQueue
from .pila_deshacer import UndoStack
from .directorio_medico import MedicalDirectory
from .historial_intervenciones import InterventionHistory


class HospitalManager:
    """
    Central state manager that exposes grouped operations
    from all data structures as a unified API for the frontend.
    """

    def __init__(self):
        self.beds = ICUBeds(capacity=15)
        self.waiting_room = WaitingQueue()
        self.undo_stack = UndoStack()
        self.directory = MedicalDirectory()
        self.patient_histories = {}

    # === ICU Beds (Array) ===

    def assign_bed(self, index, patient):
        success, msg = self.beds.assign_bed(index, patient)
        if success:
            self.undo_stack.push_action({
                "type": "assign_bed",
                "description": f"Asignada cama {index} a {patient}",
                "index": index,
                "patient": patient,
            })
        return success, msg

    def release_bed(self, index):
        current_patient = self.beds.beds[index]
        success, msg = self.beds.release_bed(index)
        if success:
            self.undo_stack.push_action({
                "type": "release_bed",
                "description": f"Liberada cama {index} (era de {current_patient})",
                "index": index,
                "patient": current_patient,
            })
        return success, msg

    def get_beds_state(self):
        return self.beds.get_state()

    # === Waiting Room (Queue) ===

    def enqueue_patient(self, patient):
        msg = self.waiting_room.enqueue(patient)
        self.undo_stack.push_action({
            "type": "enqueue_patient",
            "description": f"Paciente {patient} ingresado a sala de espera",
            "patient": patient,
        })
        return True, msg

    def dequeue_patient(self):
        patient, msg = self.waiting_room.dequeue()
        if patient:
            self.undo_stack.push_action({
                "type": "dequeue_patient",
                "description": f"Sacado {patient} de la sala de espera para atencion",
                "patient": patient,
            })
            return True, msg
        return False, msg

    def get_waiting_state(self):
        return self.waiting_room.get_state()

    # === Medical Directory (List) ===

    def add_doctor(self, name, specialty):
        success, msg = self.directory.add_doctor(name, specialty)
        if success:
            self.undo_stack.push_action({
                "type": "add_doctor",
                "description": f"Doctor {name} agregado al directorio",
                "name": name,
                "specialty": specialty,
            })
        return success, msg

    def remove_doctor(self, name):
        docs = self.directory.search_doctor(name)
        if not docs:
            return False, "Doctor no encontrado."
        specialty = docs[0]["specialty"]

        success, msg = self.directory.remove_doctor(name)
        if success:
            self.undo_stack.push_action({
                "type": "remove_doctor",
                "description": f"Doctor {name} eliminado del directorio",
                "name": name,
                "specialty": specialty,
            })
        return success, msg

    def get_directory(self):
        return self.directory.get_state()

    # === Patient History (Singly Linked List) ===

    def add_intervention(self, patient, procedure):
        if patient not in self.patient_histories:
            self.patient_histories[patient] = InterventionHistory()

        success, msg = self.patient_histories[patient].add_procedure(procedure)
        if success:
            self.undo_stack.push_action({
                "type": "add_intervention",
                "description": f"Proc. '{procedure}' agregado a {patient}",
                "patient": patient,
                "procedure": procedure,
            })
        return success, msg

    def get_patient_history(self, patient):
        if patient in self.patient_histories:
            return self.patient_histories[patient].get_history_list()
        return []

    # === Undo System (Stack) ===

    def undo_last_action(self):
        action, msg = self.undo_stack.pop_action()
        if not action:
            return False, msg

        action_type = action["type"]

        if action_type == "assign_bed":
            self.beds.release_bed(action["index"])
            return True, f"Revertido: Se libero la cama {action['index']} asignada por error."

        elif action_type == "release_bed":
            self.beds.assign_bed(action["index"], action["patient"])
            return True, f"Revertido: Se reasigno {action['patient']} a la cama {action['index']}."

        elif action_type == "enqueue_patient":
            if len(self.waiting_room.queue) > 0 and self.waiting_room.queue[-1] == action["patient"]:
                self.waiting_room.queue.pop()
                return True, f"Revertido: Se saco a {action['patient']} de la cola."
            return False, "No se pudo deshacer la encolacion."

        elif action_type == "dequeue_patient":
            self.waiting_room.queue.appendleft(action["patient"])
            return True, f"Revertido: {action['patient']} devuelto al inicio de la sala de espera."

        elif action_type == "add_doctor":
            self.directory.remove_doctor(action["name"])
            return True, f"Revertido: Doctor {action['name']} removido."

        elif action_type == "remove_doctor":
            self.directory.add_doctor(action["name"], action["specialty"])
            return True, f"Revertido: Doctor {action['name']} restaurado."

        elif action_type == "add_intervention":
            history = self.patient_histories.get(action["patient"])
            if history:
                current_list = history.get_history_list()
                if current_list and current_list[-1] == action["procedure"]:
                    current_list.pop()
                    history.clear_history()
                    for proc in current_list:
                        history.add_procedure(proc)
                    return True, f"Revertido: Procedimiento '{action['procedure']}' eliminado."
            return False, "No se pudo deshacer la intervencion."

        return True, "Revertido."

    def get_action_history(self):
        return self.undo_stack.get_state()
