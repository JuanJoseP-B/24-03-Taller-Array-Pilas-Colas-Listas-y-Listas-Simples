from collections import deque


class WaitingQueue:
    """
    Queues: Manages the general waiting room. Patients with priority
    level 4 or 5 enter a standard queue and are served in strict
    arrival order (FIFO).
    """
    def __init__(self):
        self.queue = deque()

    def enqueue(self, patient):
        self.queue.append(patient)
        return f"{patient} agregado a la sala de espera."

    def dequeue(self):
        if self.is_empty():
            return None, "La sala de espera esta vacia."
        patient = self.queue.popleft()
        return patient, f"{patient} ha sido llamado a consulta."

    def is_empty(self):
        return len(self.queue) == 0

    def get_state(self):
        return list(self.queue)
