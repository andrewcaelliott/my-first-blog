from django.db import models
from django.utils import timezone

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
        ('U', 'unit'),
        ('K', 'thousand'),
        ('M', 'million'),
        ('G', 'billion'),
        ('T', 'trillion'),
    )
    multiple = models.CharField(max_length=1, choices=MULTIPLE_CHOICES, default="U")
    unit = models.CharField(max_length=10)
    subject = models.TextField()

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
        n = num(self.number) * 10**self.scale
        comparisons = []
        for reference in references:
            fact = NumberFact.objects.get(title=reference[0])
            factNumber = fact.value*10**fact.scale
            comparisonNumber = n / factNumber
            times = comparisonNumber;
            fraction = 1/comparisonNumber;
            percent = times * 100;
            if comparisonNumber >=1:
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
        ('K', 'thousand'),
        ('M', 'million'),
        ('G', 'billion'),
        ('T', 'trillion'),
    )
    multiple = models.CharField(max_length=1, choices=MULTIPLE_CHOICES)
    location = models.CharField(max_length=100)
    value = models.DecimalField(max_digits=30, decimal_places=10)
    unit = models.CharField(max_length=10)
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

