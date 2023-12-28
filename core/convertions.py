import decimal
def to_decimal(value):
    try:
        return decimal.Decimal(value).quantize(decimal.Decimal('0.01'))
    except:
        return 0

def to_integer(value):
    try:
        return int(value)
    except:
        return 0