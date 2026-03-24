class Node:
    """Single node in the singly linked list."""
    def __init__(self, procedure):
        self.procedure = procedure
        self.next = None


class InterventionHistory:
    """
    Singly Linked Lists: Maintains the 'Intervention History' of a
    patient during their visit. Each node is a medical procedure
    pointing sequentially to the next step.
    """
    def __init__(self):
        self.head = None
        self.tail = None

    def add_procedure(self, procedure):
        new_node = Node(procedure)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        return True, f"Procedimiento '{procedure}' agregado al historial."

    def get_history_list(self):
        elements = []
        current = self.head
        while current:
            elements.append(current.procedure)
            current = current.next
        return elements

    def clear_history(self):
        self.head = None
        self.tail = None
