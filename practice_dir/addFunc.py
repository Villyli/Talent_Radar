def add(a, b):
    if isinstance(a, str):
        return a + '+' + b
    return a + b