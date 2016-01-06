from django.db import models
from django.utils import timezone

class NumberFact(models.Model):

    text = models.TextField()
    title = models.CharField(max_length=50)
    number = models.CharField(max_length=20)
    scale = models.IntegerField()
    location = models.CharField(max_length=100)
    value = models.DecimalField(max_digits=30, decimal_places=10)
    unit = models.CharField(max_length=10)
    subject = models.TextField()

    def _display(self):
    	return " ".join([self.title,":",self.number, self.unit, self.subject])

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

