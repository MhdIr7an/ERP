import decimal
def to_decimal(value):
    try:
        # print(f"Attempting to convert: {value}")
        return decimal.Decimal(value).quantize(decimal.Decimal('0.01'))
    # except decimal.InvalidOperation as e:
    except:
        # print(f"Error converting {value}: {e}")
        return 0

def to_integer(value):
    try:
        return int(value)
    except:
        return 0