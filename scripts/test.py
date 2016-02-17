from blog.models import NumberFact
#from blog.models import NumberQuery
#from blog.forms import QueryForm
#from pint import UnitRegistry
from math import log10
from random import sample,randint
from blog.utils import closeEnoughNumberFact, numberFactsLikeThis, biggestNumberFact,parseBigNumber, num, bracketNumber, randomFact

#
#ureg = UnitRegistry()
#Q_=ureg.Quantity
#
#def num(s):
    #try:
        #return int(s)
    #except ValueError:
        #return float(s)
#
#
#def addTestFact():
	#nf = NumberFact()
	#nf.title="Test Fact"
	#nf.text="Just a trial"
	#nf.number="100"
	#nf.value=num(nf.number)
	#nf.scale=0
	#nf.save()
	#print(nf.render)
#
#def addFact(title="Test Fact", text="Just a trial", number="100", scale=0, unit = "n/a"):
	#deleteFacts(title=title)
	#nf = NumberFact()
	#nf.title=title
	#nf.text=text
	#nf.number=number
	#nf.value=num(nf.number)
	#nf.scale=scale
	#nf.unit = unit
	#nf.save()
	#print(nf.render)
#
#
#def getFacts(title=None):
	#if title==None:
		#facts = NumberFact.objects.all()
	#else:		
		#facts = NumberFact.objects.all().filter(title=title)
	#return facts
#
#def deleteFacts(title=None):
	#facts = NumberFact.objects.all().filter(title=title)
	#for fact in facts:
		#print("deleting",fact.render)
		#fact.delete()
#
#def run1():
	##addFact()
	##deleteFacts(title="Test Fact")
	##print(getFacts())
	#inFile= open("../blog/data/Population_of_countries.csv")
	#lines = inFile.readlines()
	#for line in lines:
		#print(line)
		#ordinal, country, number, multiple, scale, unit = line.split(",")
		#print(ordinal, country, number, multiple, scale, unit)
		#fact = addFact(title="Population of "+country.replace(";",",").replace("\"",""), text="fun fact", number=number, scale=scale, unit = " ".join([multiple, unit]))
#
#def getConversions(nq, conversions):
	#conversion_answers = []
	#quantity = Q_(" ".join([str(nq.number), nq.unit]))
	#for conversion in conversions:
		#conversion_answers.append(str(quantity.to(conversion)))
	#return conversion_answers
#
#def run2():
	#references = [
		#('Population of World','for every person in the world'),
		#('Population of China','for every person in China'),
		#('Population of United States','for every person in the USA'),
		#('Population of United Kingdom','for every person in the UK'),
	#]
	#nq = NumberQuery(number=2000, multiple="G", unit="things", measure="count")
	#print(nq.getComparisons(references))
#
#def run3():
	#conversions = [
		#('meter'),
		#('kilometer'),
		#('mile'),
		#('yard'),
	#]
	#nq = NumberQuery(number=2000, multiple="k", unit="m", measure="count")
##	print(getConversions(nq, conversions))
	#print(nq.getConversions(conversions))
#
#def sigfigs(x,n):
	#l10 = 1+round(log10(x),0)
	#return round(x, int(n-l10))
#
#def run4():
	#q = 1/7
	#print(q)
	#print(sigfigs(q, 6))	
	#print(sigfigs(10*q, 6))	
	#print(sigfigs(1000*q, 6))
	#print(sigfigs(1000000*q, 6))		
	#print(sigfigs(10000000*q, 6))		
	#print(sigfigs(10000000*q, 7))		
	#print(sigfigs(10000000*q, 4))	
#
#def run5():
	#qf = QueryForm()
	#print(qf.fields['measure'].choices)
#
#def closeEnoughNumberFact(magnitude, scale, tolerance, measure):
##	nf = NumberFact.objects.filter(magnitude__gt=800, scale=scale)
	#facts = []
	#nf = NumberFact.objects.filter(value__gte=magnitude*1000/(1+tolerance), value__lt=magnitude*1000*(1+tolerance), scale=scale-3, measure=measure)
	#for fact in nf:
		#facts.append(fact)
	#nf = NumberFact.objects.filter(value__gte=magnitude/(1+tolerance), value__lt=magnitude*(1+tolerance), scale=scale, measure=measure)
	#for fact in nf:
		#facts.append(fact)
	#nf = NumberFact.objects.filter(value__gte=magnitude/1000/(1+tolerance), value__lt=magnitude/1000*(1+tolerance), scale=scale+3, measure=measure)
	#for fact in nf:
		#facts.append(fact)
	#return facts
#
def run6():
	nf = closeEnoughNumberFact(NumberFact, 900, 3, 0.5,"extent")
	for fact in nf:
		print(fact.value, fact.render)

#def run7():
#	bn = parseBigNumber("126g767")
#	print(bn)

def run():
	measure=("extent")
	seed = randint(0,1000000)
	rf = randomFact(NumberFact, measure, rseed=seed)
	print(rf.render)

	bestComparisons, tolerance, score  = numberFactsLikeThis(NumberFact, rf, rseed=seed) 

	print(tolerance, score)
	for fact in bestComparisons:
		print(fact.render)
		print(fact.magnitude)
		print(fact.scale)

	biggest = biggestNumberFact(bestComparisons)
	print(">>>", biggest.render)

def run9():
	measure=("mass")
	seed = randint(0,1000000)
	rf = randomFact(NumberFact, measure, rseed=seed)
	magnitude = rf.magnitude
	scale = rf.scale
#	print(rf.render)
#	test = NumberFact.objects.filter().order_by("value")[0:10]#
#	for item in test:
#		print(item.render, item.magnitude, item.value)

#	print(bracketNumber(magnitude, scale, measure))
	for i in range(0,24,3):
		print(bracketNumber(NumberFact, "1.25", i, "count"))
		print(bracketNumber(NumberFact, "12.5", i, "count"))
		print(bracketNumber(NumberFact, "125", i, "count"))

def run10():
	klass = NumberFact
	print(NumberFact)
	print(klass)
	print(klass.objects)
