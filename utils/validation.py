import re
from validate_email import validate_email

def verify_regex(regex, d):
    d = str(d)
    regex = re.compile(regex)
    if regex.match(d) is None:
        return False
    return True

def is_money(d):
    return verify_regex('^[0-9]+(\.[0-9]{1,2})?$', d)

def is_rating(d):
    # A rating should be an integer between 1 and 5
    return verify_regex('^[1-5]$', d)

def is_valid_email(d):
    return validate_email(d)

def is_valid_length(d, min, max):
    # The function checks whether d's length is in the range [min, max]
    d = str(d)
    if (len(d) >= min and len(d) <= max):
        return True
    return False

def is_valid_username(d):
    # The current system is desgined to accept username in the range between 6 and 24
    return verify_regex('^[a-zA-Z0-9_-]{6,24}$', d)

def is_valid_password(d):
    # The password should contain at least:
    #  - One lower case letter
    #  - One upper case latter
    #  - One number
    if is_valid_length(d, 8, 24):
        return verify_regex('^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])', d)
    return False