from abc import ABC, abstractmethod
from app.models.Payment import Payment


class PaymentObserver(ABC):
    @abstractmethod
    async def update(self, payment: Payment) -> None:
        """Será llamado cuando un pago se procese exitosamente"""
        pass
