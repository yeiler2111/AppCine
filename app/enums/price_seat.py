import enum

class PriceSeat(enum.Enum):
    GENERAL = (1, 10)
    VIP = (2, 25)
    PAREJA = (3, 35)

    def __init__(self, seat_id: int, price: float):
        self.seat_id = seat_id
        self.price = price

    @classmethod
    def from_id(cls, seat_id: int):
        for seat in cls:
            if seat.seat_id == seat_id:
                return seat
        raise ValueError(f"Seat id {seat_id} no válido")
