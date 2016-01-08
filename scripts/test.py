from blog.models import NumberFact

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

def run():
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
