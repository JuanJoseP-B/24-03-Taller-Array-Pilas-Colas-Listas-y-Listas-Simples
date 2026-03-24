class UndoStack:
    """
    Stacks: Implements an 'Undo' system for medical staff.
    If a nurse logs an incorrect vital sign or discharges a patient
    by mistake, the action goes onto the stack and can be reverted
    immediately (LIFO).
    """
    def __init__(self):
        self.action_history = []

    def push_action(self, action):
        self.action_history.append(action)

    def pop_action(self):
        if self.is_empty():
            return None, "No hay acciones para deshacer."
        reverted = self.action_history.pop()
        return reverted, f"Accion deshecha: {reverted.get('description', 'Desconocida')}"

    def is_empty(self):
        return len(self.action_history) == 0

    def get_state(self):
        return self.action_history[::-1]
