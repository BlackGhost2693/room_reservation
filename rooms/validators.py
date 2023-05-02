import re
from rest_framework.serializers import ValidationError


def phone_validator(value):
    """
    a validator for reservationist phone number  
    """
    regex = r'^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$'
    if not re.match(regex, value):
        raise ValidationError("Invalid phone number.")