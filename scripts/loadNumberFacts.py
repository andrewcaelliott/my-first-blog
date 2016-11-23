from blog.models import NumberFact
from blog.models import NumberQuery
from django.utils.text import slugify
from datetime import datetime
from time import strptime
from pytz import utc

def num(s):
    try:
        return int(s)
    except ValueError:
        return float(s)

def addFact(title="Test Fact", text="Just a trial", datefld=None, location="", magnitude="100", scale=0, multiple="unit", unit = "n/a", measure = "count"):
    deleteFacts(title=title)
    nf = NumberFact()
    nf.title=title
    nf.text=text
    if datefld:
        nf.date = utc.localize(datefld)
    else: 
        nf.date = None
    nf.location = location
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
        fields = line.split(",")
        if len(fields)== 8:
            ordinal, subject, magnitude, multiple, scale, unit, measure, comment = line.split(",")
            datefld = None
            location = ""
        elif len(fields) == 10:
            ordinal, subject, datestr, location, magnitude, multiple, scale, unit, measure, comment = line.split(",")
            if datestr == "":
                datefld = None
            else:
                d = strptime(datestr, "%Y")
 #               print(d)
 #               print(d[0:6])
                dt = datetime(*d[0:6])
#                dt.replace(tzinfo=utc)
                utc.localize(dt)
 #               print(dt)
#                print(dt.isoformat())
                datefld = dt
        else:
            raise ValueError("wrong number of fields in: "+line)
        #print(ordinal, subject, magnitude, multiple, scale, unit, measure, comment)
 #       print(fields)
 #       print(datefld)
        fact = addFact(title=metric+subject.replace(";",",").replace("\"",""), text=comment, datefld=datefld, location = location, magnitude=magnitude, scale=scale, multiple=multiple, unit = unit, measure=measure)
 #       print(fact)
 #       print(fact.date)
 #       print(fact.render)

def run():
    print("ok")
    deleteAllFacts()
    loadNumberFacts("./blog/data/LandArea.csv","Land Area of ","km^2", encoding="latin1")
    loadNumberFacts("./blog/data/GDP.csv","GDP in ","USD p/a", encoding="latin1")
    loadNumberFacts("./blog/data/GovRev.csv","Total taxation in ","USD p/a", encoding="latin1")
    loadNumberFacts("./blog/data/GovExp.csv","Govt spending in ","USD p/a", encoding="latin1")
    loadNumberFacts("./blog/data/Population.csv","Population of ","people", encoding="latin1")
    loadNumberFacts("./blog/data/Debt.csv","National Debt of ","USD", encoding="latin1")
    loadNumberFacts("./blog/data/Households.csv","Household Consumption in ","USD p/a", encoding="latin1")
    loadNumberFacts("./blog/data/GovtConsumption.csv","Government Consumption in ","USD p/a", encoding="latin1")
    loadNumberFacts("./blog/data/InvCapital.csv","Investment in Capital in ","USD p/a", encoding="latin1")
    loadNumberFacts("./blog/data/InvInventories.csv","Investment in Inventories in ","USD p/a", encoding="latin1")
    loadNumberFacts("./blog/data/Exports.csv","Exports from ","USD p/a", encoding="latin1")
    loadNumberFacts("./blog/data/Imports.csv","Imports to ","USD p/a", encoding="latin1")
    loadNumberFacts("./blog/data/Agriculture.csv","Agriculture production in ","USD p/a", encoding="latin1")
    loadNumberFacts("./blog/data/Industry.csv","Industrial production in ","USD p/a", encoding="latin1")
    loadNumberFacts("./blog/data/Services.csv","Services production in ","USD p/a", encoding="latin1")
    #loadNumberFacts("./blog/data/GovtExps.csv","Govt spending in ","USD p/a", encoding="latin1")
    loadNumberFacts("./blog/data/Reference_Speeds.csv","","km/h")
    #loadNumberFacts("./blog/data/Area_of_countries.csv","Area of ","m^2")
    loadNumberFacts("./blog/data/Reference_Energy.csv","","J")
    loadNumberFacts("./blog/data/Company_Revenues.csv","","USD")
    #loadNumberFacts("./blog/data/Population_of_countries.csv","Population of ","people", encoding="latin1")
    #loadNumberFacts("./blog/data/GDP_of_countries.csv","GDP of ","USD p/a", encoding="latin1")
    loadNumberFacts("./blog/data/Population_of_cities.csv","Population of ","people", encoding="latin1")
    loadNumberFacts("./blog/data/Animal_Populations.csv","","individuals")
    loadNumberFacts("./blog/data/Reference_Durations.csv","","USD p/a")
    loadNumberFacts("./blog/data/Reference_Amounts.csv","","")
    loadNumberFacts("./blog/data/Reference_Lengths.csv","","")
    loadNumberFacts("./blog/data/Reference_Masses.csv","Mass of ","kg")
    loadNumberFacts("./blog/data/Reference_Counts.csv","Number of ","")
    loadNumberFacts("./blog/data/costs_2015.csv","Cost of ","m")
    loadNumberFacts("./blog/data/heights_2015.csv","","m")
    loadNumberFacts("./blog/data/Reference_Volumes.csv","Volume of ","m^3")

