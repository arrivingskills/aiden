def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def calc(f, a, b):
    return f(a, b)

print(calc(subtract, 1, 2))


print = add

assert print(1, 2) == 3