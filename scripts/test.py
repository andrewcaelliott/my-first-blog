from blog.models import NumberFact
from blog.models import NumberQuery
from pint import UnitRegistry
ureg = UnitRegistry()
Q_=ureg.Quantity

def num(s):
    try:
        return int(s)
    except ValueError:
        return float(s)


def addTestFact():
	nf = NumberFact()
	nf.title="Test Fact"
	nf.text="Just a trial"
	nf.number="100"
	nf.value=num(nf.number)
	nf.scale=0
	nf.save()
	print(nf.render)

def addFact(title="Test Fact", text="Just a trial", number="100", scale=0, unit = "n/a"):
	deleteFacts(title=title)
	nf = NumberFact()
	nf.title=title
	nf.text=text
	nf.number=number
	nf.value=num(nf.number)
	nf.scale=scale
	nf.unit = unit
	nf.save()
	print(nf.render)


def getFacts(title=None):
	if title==None:
		facts = NumberFact.objects.all()
	else:		
		facts = NumberFact.objects.all().filter(title=title)
	return facts

def deleteFacts(title=None):
	facts = NumberFact.objects.all().filter(title=title)
	for fact in facts:
		print("deleting",fact.render)
		fact.delete()

def run1():
	#addFact()
	#deleteFacts(title="Test Fact")
	#print(getFacts())
	inFile= open("../blog/data/Population_of_countries.csv")
	lines = inFile.readlines()
	for line in lines:
		print(line)
		ordinal, country, number, multiple, scale, unit = line.split(",")
		print(ordinal, country, number, multiple, scale, unit)
		fact = addFact(title="Population of "+country.replace(";",",").replace("\"",""), text="fun fact", number=number, scale=scale, unit = " ".join([multiple, unit]))

def getConversions(nq, conversions):
	conversion_answers = []
	quantity = Q_(" ".join([str(nq.number), nq.unit]))
	for conversion in conversions:
		conversion_answers.append(str(quantity.to(conversion)))
	return conversion_answers

def run2():
	references = [
		('Population of World','for every person in the world'),
		('Population of China','for every person in China'),
		('Population of United States','for every person in the USA'),
		('Population of United Kingdom','for every person in the UK'),
	]
	nq = NumberQuery(number=2000, multiple="G", unit="things", measure="count")
	print(nq.getComparisons(references))

def run():
	conversions = [
		('meter'),
		('kilometer'),
		('mile'),
		('yard'),
	]
	nq = NumberQuery(number=2000, multiple="k", unit="m", measure="count")
#	print(getConversions(nq, conversions))
	print(nq.getConversions(conversions))
