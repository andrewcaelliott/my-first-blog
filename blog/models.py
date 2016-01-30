from django.db import models
from django.utils import timezone
from pint import UnitRegistry,UndefinedUnitError
from .fixer_io import convertToCurrency
from .convert import convertToDefault
from .convert import AMOUNT_UNITS
from .config import all_unit_choices
from .config import MEASURE_CHOICES,MULTIPLE_CHOICES
from .utils import num,sigfigs,getScaleFactor,output,currency_output
ureg = UnitRegistry()
Q_=ureg.Quantity
UNIT_CHOICES = all_unit_choices

def closeEnoughNumberFact(magnitude, scale, tolerance, measure):
#   nf = NumberFact.objects.filter(magnitude__gt=800, scale=scale)
    facts = []
    nf = NumberFact.objects.filter(value__gte=num(magnitude)*1000/(1+tolerance), value__lt=num(magnitude)*1000*(1+tolerance), scale=scale-3, measure=measure)
    for fact in nf:
        facts.append(fact)
    nf = NumberFact.objects.filter(value__gte=num(magnitude)/(1+tolerance), value__lt=num(magnitude)*(1+tolerance), scale=scale, measure=measure)
    for fact in nf:
        facts.append(fact)
    nf = NumberFact.objects.filter(value__gte=num(magnitude)/1000/(1+tolerance), value__lt=num(magnitude)/1000*(1+tolerance), scale=scale+3, measure=measure)
    for fact in nf:
        facts.append(fact)
    return facts


class NumberQuery(models.Model):

    text       = models.TextField()
    title      = models.CharField(max_length=50)
    number      = models.CharField(max_length=100)
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

    def getCloseMatches(self):
        #todo first convert to default unit

        factor = self.setScaleFactor()
        try:
            num_ans = num(self.magnitude) * factor
        except:
            num_ans = 0            
        n = convertToDefault(num_ans, self.unit)

        if n>1000000000000:
            temp_scale = 12
            n = n / 1000000000000.0
        elif n>1000000000:
            temp_scale = 9
            n = n / 1000000000.0
        elif n>1000000:
            temp_scale = 6
            n = n / 1000000.0
        elif n>1000:
            temp_scale = 3
            n = n / 1000.0
        else:
            temp_scale = 0

        closeEnough = closeEnoughNumberFact(n, temp_scale, 0.2, self.get_measure_display())
        closeMatches = []
        for fact in closeEnough:
            match = {"text":fact.render, "link":fact.link}
            closeMatches.append(match)
#            closeMatches.append(":".join([fact.render,fact.link]))
#        closeMatches.append(" ".join([str(self.magnitude), str(scale), str(self.fields)]))
        if n==0:
            closeMatches.append({"text":"Invalid input", "link":"."})
        elif len(closeMatches)==0:
            closeMatches.append({"text":"No close matches found", "link":"."})
        return closeMatches

    def getComparisons(self, references):
        factor = self.setScaleFactor()
        try:
            num_ans = num(self.magnitude) * factor
        except:
            num_ans=0
        n = convertToDefault(num_ans, self.unit)
        comparisons = []
        if (n == 0):
            comparisons.append({"factor":0, "render":"Invalid input"})
        for reference in references:
            fact = NumberFact.objects.get(title=reference[0])
            factNumber = float(fact.value)*10**fact.scale
            comparisonNumber = n  / factNumber
            if (comparisonNumber <= 10000) and (comparisonNumber >= 0.0001):
                times = sigfigs(comparisonNumber,6);
                fraction = sigfigs(1/comparisonNumber,3);
                percent = sigfigs(times,6) * 100;
                if comparisonNumber >=0.5:
                    comparisonRender = reference[1].format(times=times, fraction=fraction, percent=percent)
                elif comparisonNumber >=0.1 or len(reference)<4:
                    comparisonRender = reference[2].format(times=times, fraction=fraction, percent = percent)
                else:
                    comparisonRender = reference[3].format(times=times, fraction=fraction, percent = percent)
                comparison ={"factor":comparisonNumber, "render": comparisonRender, "link":fact.link}
                comparisons.append(comparison)
        return comparisons

    def getConversions(self, conversions):
        conversion_answers = []
        num_ans = num(self.magnitude) * self.setScaleFactor()
        if self.unit in AMOUNT_UNITS: 
            for conversion in conversions:
                n = convertToCurrency(num_ans, self.unit, conversion)
                mag = round(n,2)
                conversion_answers.append(" ".join([currency_output(mag), conversion]))
        else:
            quantity = Q_(" ".join([str(num_ans), self.unit]))
            for conversion in conversions:
                conv_q = quantity.to(conversion)
                mag = sigfigs(conv_q.magnitude,6)
                conversion_answers.append(" ".join([output(mag), conversion]))
        return conversion_answers


    def _display(self):
        return " ".join([self.title,":",self.magnitude, self.get_multiple_display(), self.unit])

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
#    value = models.DecimalField(max_digits=30, decimal_places=10)
    value = models.FloatField()
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES)
    measure = models.CharField(max_length=1, choices=MEASURE_CHOICES)
    subject = models.TextField()

    def _display(self):
        return " ".join([self.title,":",self.magnitude, self.get_multiple_display(), self.unit])

    def _link(self):
        return "../fact/"+str(self.id)

    def __str__(self):
        return self.title        

    render = property(_display)
    link = property(_link)

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

