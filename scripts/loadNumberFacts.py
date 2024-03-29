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

def deleteUnitFacts(unit=None):
    facts = NumberFact.objects.all().filter(unit=unit)
    for fact in facts:
        fact.delete()

def deleteAllFacts():
    facts = NumberFact.objects.all()
    facts.delete()
#    for fact in facts:
#        fact.delete()

def loadNumberFacts(fileName, metric, unit, encoding="UTF-8"):
    inFile= open(fileName, encoding=encoding)
    lines = inFile.readlines()
    for line in lines[0:]:
        print(line)
        fields = line.split(",")
        if len(fields)== 8:
            ordinal, subject, magnitude, multiple, scale, lineunit, measure, comment = line.split(",")
            datefld = None
            location = ""
        else:
            if len(fields) == 10:
                ordinal, subject, datestr, location, magnitude, multiple, scale, lineunit, measure, comment = line.split(",")
            elif len(fields) == 9:
                subject, datestr, location, magnitude, multiple, scale, lineunit, measure, comment = line.split(",")
            else:
                raise ValueError("wrong number of fields in: "+line)
            if datestr == "":
                datefld = None
            else:
                d = strptime(datestr, "%Y")
                dt = datetime(*d[0:6])
                utc.localize(dt)
                datefld = dt
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
    print("deleted")
    loadNumberFacts("./blog/data/Reference_Amounts.csv","","USD", encoding="latin1")
    loadNumberFacts("./blog/data3/Population.csv","Population of ","people", encoding="latin1")
    loadNumberFacts("./blog/data3/GDP.csv","GDP in ","USD p/a", encoding="latin1")
    loadNumberFacts("./blog/data3/GovExp.csv","Govt spending in ","USD p/a", encoding="latin1")
    loadNumberFacts("./blog/data3/GovRev.csv","Total taxation in ","USD p/a", encoding="latin1")
    loadNumberFacts("./blog/data3/Debt.csv","Public Debt of ","USD", encoding="latin1")
    loadNumberFacts("./blog/data3/Households.csv","Household Consumption in ","USD p/a", encoding="latin1")
    loadNumberFacts("./blog/data3/GovtConsumption.csv","Government Consumption in ","USD p/a", encoding="latin1")
    loadNumberFacts("./blog/data3/InvCapital.csv","Investment in Capital in ","USD p/a", encoding="latin1")
    loadNumberFacts("./blog/data3/InvInventories.csv","Investment in Inventories in ","USD p/a", encoding="latin1")
    loadNumberFacts("./blog/data3/Exports.csv","Exports from ","USD p/a", encoding="latin1")
    loadNumberFacts("./blog/data3/Imports.csv","Imports to ","USD p/a", encoding="latin1")
    loadNumberFacts("./blog/data3/Agriculture.csv","Agricultural production in ","USD p/a", encoding="latin1")
    loadNumberFacts("./blog/data3/Industry.csv","Industrial production in ","USD p/a", encoding="latin1")
    loadNumberFacts("./blog/data3/Services.csv","Services production in ","USD p/a", encoding="latin1")
    loadNumberFacts("./blog/data3/LandArea.csv","Land Area of ","km^2", encoding="latin1")
    loadNumberFacts("./blog/data3/LandUseAgri.csv","Land used for agriculture in ","km^2", encoding="latin1")
    loadNumberFacts("./blog/data3/LandUseAgriArable.csv","Land used for arable in ","km^2", encoding="latin1")
    loadNumberFacts("./blog/data3/LandUseAgriPermCrops.csv","Land used for permanent crops in ","km^2", encoding="latin1")
    loadNumberFacts("./blog/data3/LandUseAgriPermPasture.csv","Land used for permanent pasture in ","km^2", encoding="latin1")
    loadNumberFacts("./blog/data3/LandUseForest.csv","Forest in ","km^2", encoding="latin1")
    loadNumberFacts("./blog/data3/LandUseOther.csv","Other land in ","km^2", encoding="latin1")
    #loadNumberFacts("./blog/data/Reference_Index.csv","","", encoding="latin1")
    #loadNumberFacts("./blog/data/Reference_Information.csv","","KB", encoding="latin1")
    loadNumberFacts("./blog/data/Reference_Counts.csv","Number of ","", encoding="latin1")
    loadNumberFacts("./blog/data/Reference_Counts_Deaths.csv","Number of ","", encoding="latin1")
    loadNumberFacts("./blog/data/Reference_Speeds.csv","","km/h", encoding="latin1")
    loadNumberFacts("./blog/data/Reference_Energy.csv","","J", encoding="latin1")
    loadNumberFacts("./blog/data/Company_Revenues.csv","","USD", encoding="latin1")
    loadNumberFacts("./blog/data/Population_of_countries - Missing.csv","Population of ","people", encoding="latin1")
    loadNumberFacts("./blog/data/Population_of_cities.csv","Population of ","people", encoding="latin1")
    loadNumberFacts("./blog/data/Animal_Populations.csv","","individuals", encoding="latin1")
    loadNumberFacts("./blog/data/Reference_Durations.csv","","y", encoding="latin1")
    loadNumberFacts("./blog/data/Reference_Amounts.csv","","USD", encoding="latin1")
    loadNumberFacts("./blog/data/Reference_Lengths.csv","","m", encoding="latin1")
    loadNumberFacts("./blog/data/Reference_Masses.csv","Mass of ","kg")
    loadNumberFacts("./blog/data/Reference_Capacity.csv","","L", encoding="latin1")
    # loadNumberFacts("./blog/data/costs_2015.csv","Cost of ","USD", encoding="latin1")
    loadNumberFacts("./blog/data/Reference_Volumes.csv","Volume of ","m^3", encoding="latin1")

