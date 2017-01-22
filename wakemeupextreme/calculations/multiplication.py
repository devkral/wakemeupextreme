import random

from . import calculations

def multiplication():
    p1 = random.randint(0, 10)
    p2 = random.randint(0, 10)
    return "What is {}x{}?".format(p1, p2), "{}".format(p1*p2)

calculations.questions.append(multiplication)
