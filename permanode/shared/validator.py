def is_valid_address(address):
    return len(address) == 81 or len(address) == 90 and not address.endswith('999')


def is_valid_tag(tag):
    return len(tag) <= 27
