CONSTANT = 5+2*j
DEPTH = 500

def evolution(val, constant=CONSTANT):
    return val**2 + constant

def is_inside_bounds(val):
    return (val.real ** 2 + val ** imag) < 4

def num_iterations_until_escape(constant):
    num = 0
    iterations = 0
    while is_inside_bounds(num) and iterations < DEPTH:
        num = evolution(num, constant)
        iterations += 1

    if iterations == DEPTH:
        return None
    else:
        return iterations
    


