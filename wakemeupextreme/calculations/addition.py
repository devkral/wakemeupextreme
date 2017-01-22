import random

from . import calculations

def addition():
    p1 = random.randint(0, 100)
    p2 = random.randint(0, 100)
    return "What is {}+{}?".format(p1, p2), "{}".format(p1+p2)

calculations.questions.append(addition)
