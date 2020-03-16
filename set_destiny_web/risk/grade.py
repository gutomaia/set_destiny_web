

def grade(**kwargs):
    data = {}
    for k, v in kwargs.items():
        if isinstance(v, str):
            data[k] = v
        elif v <= 0:
            data[k] = 'economic'
        elif v <= 2:
            data[k] = 'regular'
        elif v >= 3:
            data[k] = 'responsible'
    return data
