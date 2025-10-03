from abc import ABC, abstractmethod
from app.models.Payment import Payment
from app.observers.payment_observer import PaymentObserver


class EmailService(ABC):
    @abstractmethod
    async def send_email(self, to: str, subject: str, body: str) -> None:
        pass


class MockEmailService(EmailService):
    async def send_email(self, to: str, subject: str, body: str) -> None:
        print("------ SIMULACIÓN EMAIL ------")
        print(f"Para: {to}")
        print(f"Asunto: {subject}")
        print("Cuerpo:")
        print(body)
        print("-----------------------------")


class EmailNotifier(PaymentObserver):
    def __init__(self, email_service: EmailService):
        self.email_service = email_service

    async def update(self, payment: Payment) -> None:
        subject = "Confirmación de pago exitoso"
        body = (
            f"Hola usuario {payment.user_id},\n\n"
            f"Tu pago con ID {payment.id} por {payment.amount} fue procesado con éxito.\n"
            f"Estado: {payment.status}\n\n"
            f"¡Gracias por tu compra!"
        )
        to_email = f"user_{payment.user_id}@example.com"
        await self.email_service.send_email(to_email, subject, body)


class LoggerObserver(PaymentObserver):
    async def update(self, payment: Payment) -> None:
        print(f"[LOGGER] Pago {payment.id} -> Estado: {payment.status}, Usuario: {payment.user_id}")
