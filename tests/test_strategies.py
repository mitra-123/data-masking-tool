from masking.strategies import EmailMaskStrategy, RedactStrategy, CreditCardMaskStrategy

def test_email_mask():
    s = EmailMaskStrategy()
    assert s.mask("john.doe@gmail.com") == "j***@gmail.com"

def test_redact():
    s = RedactStrategy()
    assert s.mask("anything") == "***REDACTED***"

def test_credit_card():
    s = CreditCardMaskStrategy()
    assert s.mask("1234-5678-9012-3456") == "****-****-****-3456"