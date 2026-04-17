from masking.masker import Masker

config = {
    "fields": {
        "email": {"strategy": "email"},
        "name": {"strategy": "redact"},
        "credit_card": {"strategy": "credit_card"},
    }
}

def test_mask_record():
    masker = Masker(config)
    record = {
        "name": "John Doe",
        "email": "john@gmail.com",
        "credit_card": "1234-5678-9012-3456"
    }
    result = masker.mask_record(record)
    assert result["name"] == "***REDACTED***"
    assert result["email"] == "j***@gmail.com"
    assert result["credit_card"] == "****-****-****-3456"

def test_unmasked_fields_unchanged():
    masker = Masker(config)
    record = {"name": "John", "email": "j@g.com", "age": "25"}
    result = masker.mask_record(record)
    assert result["age"] == "25"