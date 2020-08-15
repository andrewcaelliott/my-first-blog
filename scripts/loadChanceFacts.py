from blog.models import ChanceFact
from blog.models import ChanceQuery
from django.utils.text import slugify
from datetime import datetime
from time import strptime
from pytz import utc

def num(s):
    try:
        return int(s)
    except ValueError:
        return float(s)

def addChanceFact(title="Test Fact", text="Just a trial", probability = "1 in 100", item_text = "items", exposed_items="50", repetition_text = "repetitions", exposed_repetitions = 20, repeat_mode = "repeats", outcome_text="hits", page_type="smp", fact_type="facts"):
    deleteChanceFacts(title=title)
    cf = ChanceFact()
    cf.title=title
    cf.text=text
    cf.probability = probability
    cf.item_text       = item_text
    cf.exposed_items    = exposed_items
    cf.repetition_text       = repetition_text
    cf.exposed_repetitions    = exposed_repetitions
    cf.outcome_text       = outcome_text
    cf.repeat_mode = repeat_mode
    cf.page_type = page_type
    cf.fact_type = fact_type
    cf.permlink = slugify(title)
    cf.save()
    return cf

def deleteChanceFacts(title=None):
    facts = ChanceFact.objects.all().filter(title=title)
    for fact in facts:
        fact.delete()

def deleteAllChanceFacts():
    facts = ChanceFact.objects.all()
    facts.delete()

def loadChanceFacts(fileName, prefix, encoding="UTF-8"):
    inFile= open(fileName, encoding=encoding)
    lines = inFile.readlines()
    for line in lines[1:]:
        fields = line[:-1].split(",")
        ordinal, subject, probability, items, item_count, repetitions, repetition_count, hits, repeats, page_type, fact_type, source = fields
        probability = probability.replace(";", ",")
        hits = hits.replace(";", ",")
        print(ordinal, subject, probability, items, item_count, repetitions, repetition_count, hits, repeats, page_type, fact_type, source)
        fact = addChanceFact(
            title=subject, text=source, probability = probability, item_text = items, exposed_items=item_count, repetition_text = repetitions, exposed_repetitions = repetition_count, repeat_mode=repeats, outcome_text=hits,
            page_type =page_type,
            fact_type = fact_type            
            )
        print(fact.title, fact.permlink)

def run():
    print("ok")
    deleteAllChanceFacts()
    print("deleted")
    loadChanceFacts("./blog/data/watcot/Chances.csv","Chance of ", encoding="latin1")


