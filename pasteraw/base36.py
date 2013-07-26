import uuid


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


def decode(number):
    """Converts a base36 string to an integer."""
    return int(number, 36)


def unique():
    """Generates a unique base36 string."""
    return encode(uuid.uuid4().int)
