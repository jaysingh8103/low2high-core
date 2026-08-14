import phonenumbers

def normalize_phone(phone_str: str, default_region: str = "IN") -> str | None:
    """
    Normalizes a phone number to E.164 format.
    Returns None if the number is invalid or cannot be parsed.
    """
    if not phone_str:
        return None
    try:
        parsed = phonenumbers.parse(phone_str, default_region)
        if phonenumbers.is_valid_number(parsed):
            return phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
    except phonenumbers.NumberParseException:
        pass
    return None

def normalize_address(address_str: str) -> str | None:
    """
    Basic normalization for addresses (lowercase, stripped).
    """
    if not address_str:
        return None
    return " ".join(address_str.lower().split())
