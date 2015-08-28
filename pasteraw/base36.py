def encode(number):
    """Converts an integer to a base36 string."""
    alphabet = '0123456789abcdefghijklmnopqrstuvwxyz'

    if isinstance(number, (float)) and int(number) == number:
        number = int(number)

    if not isinstance(number, (int, long)):
        raise TypeError('number must be an integer')

    if number >= 0 and number <= 9:
        return alphabet[number]

    base36 = ''
    sign = ''

    if number < 0:
        sign = '-'
        number = -number

    while number != 0:
        number, i = divmod(number, len(alphabet))
        base36 = alphabet[i] + base36

    return sign + base36


def decode(s, base=36):
    """Converts a base36 string to an integer."""
    return int(s, base)


def re_encode(s, starting_base=16):
    """Re-encodes a string in another base to base 36."""
    return encode(decode(s, base=starting_base))


def validate(s):
    """Returns true if a string is base36-encoded."""
    try:
        decode(s)
        return True
    except Exception:
        return False
