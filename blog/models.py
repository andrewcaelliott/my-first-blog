from django.db import models
from django.utils import timezone
from pint import UnitRegistry,UndefinedUnitError
from math import log10
ureg = UnitRegistry()
Q_=ureg.Quantity

UNIT_CHOICES= (
        ('i', 'item'),
        ('km', 'kilometer'),
        ('m', 'meter'),
        ('cm', 'centimeter'),
        ('mm', 'millimeter'),
        ('mi', 'mile'),
        ('yd', 'yard'),
        ('ft', 'foot'),
        ('in', 'inch'),
        ('USD', 'USD'),
        ('year', 'year'),
        ('month', 'month'),
        ('week', 'week'),
        ('day', 'day'),
        ('hour', 'hour'),
        ('minute', 'minute'),
        ('second', 'second'),
    )


def sigfigs(x,n):
    l10 = 1+round(log10(x),0)
    x = round(x, int(n-l10))
    if (x==round(x)):
        return int(x)
    else:
        return x

def num(s):
    try:
        return int(s)
    except ValueError:
        return float(s)


class NumberQuery(models.Model):

    text = models.TextField()
    title = models.CharField(max_length=50)
    number = models.CharField(max_length=20)
    scale = models.IntegerField()
    MEASURE_CHOICES = (
        ('c', 'count'),
        ('a', 'amount'),
        ('e', 'extent'),
        ('d', 'duration'),
        ('n', 'number'),
    )
    measure = models.CharField(max_length=1, choices=MEASURE_CHOICES, default="c")
    location = models.CharField(max_length=100)
    value = models.DecimalField(max_digits=30, decimal_places=10)
    MULTIPLE_CHOICES = (
        ('U', '-'),
        ('K', 'thousand'),
        ('M', 'million'),
        ('G', 'billion'),
        ('T', 'trillion'),
    )
    multiple = models.CharField(max_length=1, choices=MULTIPLE_CHOICES, default="U")
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES)
    target_unit = models.CharField(max_length=10, choices=UNIT_CHOICES)
    subject = models.TextField()

    def setUnitChoices(self, choices):
        unit = models.CharField(max_length=10, choices=choices)

    def getScaleFactor(self):
        if self.multiple == "T":
            self.scale = 12
        elif self.multiple == "G":    
            self.scale = 9
        elif self.multiple == "M":    
            self.scale = 6
        elif self.multiple == "K":    
            self.scale = 3
        elif self.multiple == "U":
            self.scale = 0
        else:
            self.scale = 0
        return 10**self.scale


    def getComparisons(self, references):
        if self.multiple == "T":
            self.scale = 12
        elif self.multiple == "G":    
            self.scale = 9
        elif self.multiple == "M":    
            self.scale = 6
        elif self.multiple == "K":    
            self.scale = 3
        elif self.multiple == "U":
            self.scale = 0
        else:
            self.scale = 0
        num_ans = num(self.number) * 10**self.scale
        try:
            quantity = Q_(" ".join([str(num_ans), self.unit]))
            if quantity.dimensionality==ureg.s.dimensionality:
                n = quantity.to(ureg.year).magnitude
            else:
                n = quantity.to_base_units().magnitude
        except UndefinedUnitError as e:
            n = num_ans
        comparisons = []
        for reference in references:
            fact = NumberFact.objects.get(title=reference[0])
            factNumber = float(fact.value)*10**fact.scale
            comparisonNumber = n  / factNumber
            if (comparisonNumber <= 100000) and (comparisonNumber >= 0.00001):
                times = sigfigs(comparisonNumber,6);
                fraction = sigfigs(1/comparisonNumber,3);
                percent = sigfigs(times,6) * 100;
                if comparisonNumber >=0.5:
                    #comparisonRender=" ".join([str(round(comparisonNumber,2)),reference[1]])
                    #comparisonRender = reference[1] % {"times":times, "fraction":fraction, "percent":percent}
                    comparisonRender = reference[1].format(times=times, fraction=fraction, percent=percent)
                elif comparisonNumber >=0.1 or len(reference)<4:
    #                comparisonRender=" ".join([str(round(1/comparisonNumber,2)),reference[2]])
                    comparisonRender = reference[2].format(times=times, fraction=fraction, percent = percent)
                else:
                    comparisonRender = reference[3].format(times=times, fraction=fraction, percent = percent)
                comparison ={"number":comparisonNumber, "render": comparisonRender}
                comparisons.append(comparison)
            #print(" ".join([refrender, reference[1]]))
        return comparisons

    def getConversions(self, conversions):
        conversion_answers = []
        num_ans = num(self.number) * self.getScaleFactor()
        quantity = Q_(" ".join([str(num_ans), self.unit]))
        for conversion in conversions:
            conv_q = quantity.to(conversion)
            mag = sigfigs(conv_q.magnitude,6)
            conversion_answers.append(" ".join([str(mag), str(conv_q.units)]))
        return conversion_answers


    def _display(self):
    	return " ".join([self.title,":",str(self.number), self.multiple, self.unit, self.subject])

    def __str__(self):
        return self.title        

    render = property(_display)

class NumberFact(models.Model):

    text = models.TextField()
    title = models.CharField(max_length=50)
    number = models.CharField(max_length=20)
    scale = models.IntegerField()
    MULTIPLE_CHOICES = (
        ('U', '-'),
        ('K', 'thousand'),
        ('M', 'million'),
        ('G', 'billion'),
        ('T', 'trillion'),
    )
    multiple = models.CharField(max_length=1, choices=MULTIPLE_CHOICES)
    location = models.CharField(max_length=100)
    value = models.DecimalField(max_digits=30, decimal_places=10)
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES)
    MEASURE_CHOICES = (
        ('c', 'count'),
        ('a', 'amount'),
        ('e', 'extent'),
        ('d', 'duration'),
        ('n', 'number'),
    )
    measure = models.CharField(max_length=1, choices=MEASURE_CHOICES)
    subject = models.TextField()

    def _display(self):
        return " ".join([self.title,":",self.number, self.multiple, self.unit, self.subject, self.measure])

    def __str__(self):
        return self.title        

    render = property(_display)


class Comparison(models.Model):

    text = models.TextField()
    title = models.CharField(max_length=50)
    numberFact1 = models.ForeignKey('NumberFact', default=0, related_name="primary")
    numberFact2 = models.ForeignKey('NumberFact', default=0)
    difference = models.DecimalField(max_digits=30, decimal_places=10)
    ratio = models.DecimalField(max_digits=30, decimal_places=20)

    def __str__(self):
        return self.title        

    def _display(self):
        return " ".join([self.title,":",self.numberFact1, self.numberFact2])

    render = property(_display)

class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    #text = models.TextField()
    numberFact = models.ForeignKey('NumberFact', default=0)
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

