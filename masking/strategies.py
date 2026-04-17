from abc import ABC, abstractmethod

class MaskingStrategy(ABC):
    @abstractmethod
    def mask(self, value: str) -> str:
        pass

class RedactStrategy(MaskingStrategy):
    def mask(self, value: str) -> str:
        return "***REDACTED***"

class PartialMaskStrategy(MaskingStrategy):
    def __init__(self, visible_chars: int = 4):
        self.visible_chars = visible_chars

    def mask(self, value: str) -> str:
        if len(value) <= self.visible_chars:
            return value
        return value[:self.visible_chars] + "*" * (len(value) - self.visible_chars)

class EmailMaskStrategy(MaskingStrategy):
    def mask(self, value: str) -> str:
        if "@" not in value:
            return "***@***.com"
        local, domain = value.split("@", 1)
        return local[0] + "***@" + domain

class CreditCardMaskStrategy(MaskingStrategy):
    def mask(self, value: str) -> str:
        digits = value.replace("-", "").replace(" ", "")
        return "****-****-****-" + digits[-4:]

from faker import Faker

fake = Faker()

class FakeNameStrategy(MaskingStrategy):
    def mask(self, value: str) -> str:
        return fake.name()

class FakeEmailStrategy(MaskingStrategy):
    def mask(self, value: str) -> str:
        return fake.email()

class FakePhoneStrategy(MaskingStrategy):
    def mask(self, value: str) -> str:
        return fake.phone_number()