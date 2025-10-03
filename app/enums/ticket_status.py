import enum

class TicketStatus(enum.Enum):
    LIBRE = "libre"
    RESERVADO = "reservado"
    OCUPADO = "ocupado"
    CANCELADO = "cancelado"
