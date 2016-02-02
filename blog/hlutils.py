from .models import NumberFact
from random import randint,seed


def randomFact(measure, rseed=None):
    if rseed!=None:
        seed(rseed)
    count = NumberFact.objects.filter(measure=measure).count()
    rf = NumberFact.objects.filter(measure=measure)[randint(0,count-1)]
    return rf