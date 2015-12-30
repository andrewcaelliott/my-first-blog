from django.db import models
from django.utils import timezone

class NumberFact(models.Model):

    text = models.TextField()
    number = models.CharField(max_length=20)
    unit = models.CharField(max_length=10)
    referent = models.TextField()
    title = models.CharField(max_length=50)

    def _display(self):
    	return " ".join([self.title,":",self.number, self.unit, self.referent])

    render = property(_display)


    def __str__(self):
        return self.title        

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

