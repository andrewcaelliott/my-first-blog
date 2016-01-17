from blog.models import NumberFact
from blog.models import NumberQuery

def num(s):
    try:
        return int(s)
    except ValueError:
        return float(s)

def addFact(title="Test Fact", text="Just a trial", number="100", scale=0, multiple="unit", unit = "n/a", measure = "count"):
	deleteFacts(title=title)
	nf = NumberFact()
	nf.title=title
	nf.text=text
	nf.number=number
	nf.value=num(nf.number)
	nf.scale=scale
	nf.unit = unit
	nf.measure = measure
	nf.multiple=multiple
	nf.save()
	return nf

def deleteFacts(title=None):
	facts = NumberFact.objects.all().filter(title=title)
	for fact in facts:
		fact.delete()

def loadNumberFacts(fileName, metric, unit):
	inFile= open(fileName)
	lines = inFile.readlines()
	for line in lines[0:]:
		print(line)
		ordinal, subject, number, multiple, scale, unit, measure, comment = line.split(",")
		print(ordinal, subject, number, multiple, scale, unit, measure, comment)
		#print(multiple)
		fact = addFact(title=metric+subject.replace(";",",").replace("\"",""), text=comment, number=number, scale=scale, multiple=multiple, unit = unit, measure=measure)
		print(fact.render)

def run():
#	loadNumberFacts("../blog/data/Population_of_countries.csv","Population of ","people")
#	loadNumberFacts("../blog/data/GDP_of_countries.csv","GDP of ","USD p/a")
#	loadNumberFacts("./blog/data/costs_2015.csv","Cost of ","m")
	loadNumberFacts("./blog/data/heights_2015.csv","Height of ","m")

