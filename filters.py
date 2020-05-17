import validators

def is_valid_uri(uri):
    if validators.url(uri):
        return True
    return False

def float_to_int(v):
    if v:
        return int(float(v))
    return ""
