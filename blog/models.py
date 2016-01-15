from django.db import models
from django.utils import timezone
from pint import UnitRegistry,UndefinedUnitError
from .fixer_io import convertToCurrency
from .convert import convertToDefault
from .convert import AMOUNT_UNITS
from .config import all_unit_choices
from .config import MEASURE_CHOICES,MULTIPLE_CHOICES
from .utils import num,sigfigs,getScaleFactor
ureg = UnitRegistry()
Q_=ureg.Quantity
UNIT_CHOICES = all_unit_choices

class NumberQuery(models.Model):

    text       = models.TextField()
    title      = models.CharField(max_length=50)
    magnitude = models.CharField(max_length=20)
    scale = models.IntegerField()
    measure  = models.CharField(max_length=1, choices=MEASURE_CHOICES, default="c")
    location = models.CharField(max_length=100)
    value    = models.DecimalField(max_digits=30, decimal_places=10)
    multiple = models.CharField(max_length=1, choices=MULTIPLE_CHOICES, default="U")
    unit     = models.CharField(max_length=10, choices=UNIT_CHOICES)
    target_unit = models.CharField(max_length=10, choices=UNIT_CHOICES)
    subject = models.TextField()

    def setUnitChoices(self, choices):
        unit = models.CharField(max_length=10, choices=choices)

    def setScaleFactor(self):
        scale, factor = getScaleFactor(self.multiple)
        return factor

    def getComparisons(self, references):
        factor = self.setScaleFactor()
        num_ans = num(self.magnitude) * factor
        n = convertToDefault(num_ans, self.unit)
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
                    comparisonRender = reference[1].format(times=times, fraction=fraction, percent=percent)
                elif comparisonNumber >=0.1 or len(reference)<4:
                    comparisonRender = reference[2].format(times=times, fraction=fraction, percent = percent)
                else:
                    comparisonRender = reference[3].format(times=times, fraction=fraction, percent = percent)
                comparison ={"factor":comparisonNumber, "render": comparisonRender}
                comparisons.append(comparison)
        return comparisons

    def getConversions(self, conversions):
        conversion_answers = []
        num_ans = num(self.magnitude) * self.setScaleFactor()
        if self.unit in AMOUNT_UNITS: 
            for conversion in conversions:
                n = convertToCurrency(num_ans, self.unit, conversion)
                mag = round(n,2)
                conversion_answers.append(" ".join([str(mag), conversion]))
        else:
            quantity = Q_(" ".join([str(num_ans), self.unit]))
            for conversion in conversions:
                conv_q = quantity.to(conversion)
                mag = sigfigs(conv_q.magnitude,6)
                conversion_answers.append(" ".join([str(mag), conversion]))
        return conversion_answers


    def _display(self):
    	return " ".join([self.title,":",str(self.magnitude), self.multiple, self.unit, self.subject])

    def __str__(self):
        return self.title        

    render = property(_display)

class NumberFact(models.Model):

    text = models.TextField()
    title = models.CharField(max_length=50)
    magnitude = models.CharField(max_length=20)
    scale = models.IntegerField()
    multiple = models.CharField(max_length=1, choices=MULTIPLE_CHOICES)
    location = models.CharField(max_length=100)
    value = models.DecimalField(max_digits=30, decimal_places=10)
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES)
    measure = models.CharField(max_length=1, choices=MEASURE_CHOICES)
    subject = models.TextField()

    def _display(self):
        return " ".join([self.title,":",self.magnitude, self.multiple, self.unit, self.subject, self.measure])

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

