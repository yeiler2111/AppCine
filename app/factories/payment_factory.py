from abc import ABC, abstractmethod

class PaymentStrategy(ABC):
    @abstractmethod
    async def pay(self, amount: float) -> dict:
        pass


class CreditCardPayment(PaymentStrategy):
    async def pay(self, amount: float) -> dict:
        return {"status": "success", "method": "credit_card", "amount": amount}


class PaypalPayment(PaymentStrategy):
    async def pay(self, amount: float) -> dict:
        return {"status": "success", "method": "paypal", "amount": amount}


class MockPayment(PaymentStrategy):
    async def pay(self, amount: float) -> dict:
        return {"status": "success", "method": "mock", "amount": amount}


class PaymentFactory:
    @staticmethod
    def get_strategy(method: str) -> PaymentStrategy:
        strategies = {
            "credit_card": CreditCardPayment,
            "paypal": PaypalPayment,
            "mock": MockPayment,
        }
        if method not in strategies:
            raise ValueError(f"Método de pago no soportado: {method}")
        return strategies[method]()
