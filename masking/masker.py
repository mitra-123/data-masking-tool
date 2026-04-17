from masking.strategies import (
    MaskingStrategy, RedactStrategy,
    PartialMaskStrategy, EmailMaskStrategy, CreditCardMaskStrategy,
    FakeNameStrategy, FakeEmailStrategy, FakePhoneStrategy
)
from masking.logger import MaskingReport
from masking.exceptions import UnsupportedStrategyError

STRATEGY_MAP = {
    "redact": RedactStrategy,
    "partial": PartialMaskStrategy,
    "email": EmailMaskStrategy,
    "credit_card": CreditCardMaskStrategy,
    "fake_name": FakeNameStrategy,
    "fake_email": FakeEmailStrategy,
    "fake_phone": FakePhoneStrategy,
}

class Masker:
    def __init__(self, config: dict):
        self.rules: dict[str, MaskingStrategy] = {}
        self.report = MaskingReport()
        for field, options in config["fields"].items():
            strategy_name = options["strategy"]
            if strategy_name not in STRATEGY_MAP:
                raise UnsupportedStrategyError(
                    f"Unknown strategy '{strategy_name}' for field '{field}'. "
                    f"Available: {list(STRATEGY_MAP.keys())}"
                )
            kwargs = {k: v for k, v in options.items() if k != "strategy"}
            self.rules[field] = STRATEGY_MAP[strategy_name](**kwargs)

    def mask_record(self, record: dict) -> dict:
        masked = record.copy()
        self.report.increment_records()
        for field, strategy in self.rules.items():
            if field in masked and masked[field]:
                masked[field] = strategy.mask(str(masked[field]))
                self.report.record_mask(field)
        return masked