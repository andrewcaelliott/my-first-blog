from blog.models import NumberFact
from blog.models import NumberQuery
from django.utils.text import slugify

def num(s):
    try:
        return int(s)
    except ValueError:
        return float(s)

def addFact(title="Test Fact", text="Just a trial", magnitude="100", scale=0, multiple="unit", unit = "n/a", measure = "count"):
    deleteFacts(title=title)
    nf = NumberFact()
    nf.title=title
    nf.text=text
    nf.magnitude=magnitude
    nf.value=num(nf.magnitude)
    nf.scale=scale
    nf.unit = unit
    nf.measure = measure
    nf.multiple=multiple
    nf.permlink = slugify(title)
    nf.save()
    return nf

def deleteFacts(title=None):
    facts = NumberFact.objects.all().filter(title=title)
    for fact in facts:
        fact.delete()

def deleteAllFacts():
    facts = NumberFact.objects.all()
    for fact in facts:
        fact.delete()

def loadNumberFacts(fileName, metric, unit, encoding="UTF-8"):
    inFile= open(fileName, encoding=encoding)
    lines = inFile.readlines()
    for line in lines[0:]:
        print(line)
        ordinal, subject, magnitude, multiple, scale, unit, measure, comment = line.split(",")
        print(ordinal, subject, magnitude, multiple, scale, unit, measure, comment)
        #print(multiple)
        fact = addFact(title=metric+subject.replace(";",",").replace("\"",""), text=comment, magnitude=magnitude, scale=scale, multiple=multiple, unit = unit, measure=measure)
        print(fact.render)

def run():
    deleteAllFacts()
    loadNumberFacts("./blog/data/Company_Revenues.csv","","USD")
    loadNumberFacts("./blog/data/Population_of_countries.csv","Population of ","people", encoding="latin1")
    loadNumberFacts("./blog/data/GDP_of_countries.csv","GDP of ","USD p/a", encoding="latin1")
    loadNumberFacts("./blog/data/GovtRevs.csv","Total taxation in ","USD p/a", encoding="latin1")
    loadNumberFacts("./blog/data/GovtExps.csv","Govt spending in ","USD p/a", encoding="latin1")
    loadNumberFacts("./blog/data/Population_of_cities.csv","Population of ","people", encoding="latin1")
    loadNumberFacts("./blog/data/Animal_Populations.csv","","individuals")
    loadNumberFacts("./blog/data/Reference_Durations.csv","","USD p/a")
    loadNumberFacts("./blog/data/Reference_Amounts.csv","","")
    loadNumberFacts("./blog/data/Reference_Lengths.csv","","")
    loadNumberFacts("./blog/data/Reference_Masses.csv","Mass of ","kg")
    loadNumberFacts("./blog/data/Reference_Counts.csv","Number of ","")
    loadNumberFacts("./blog/data/costs_2015.csv","Cost of ","m")
    loadNumberFacts("./blog/data/heights_2015.csv","","m")

