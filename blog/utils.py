import os
from random import sample,seed,randint,choice
from pint import UnitRegistry,UndefinedUnitError
from mysite.settings import BASE_DIR
from .convert import AMOUNT_UNITS
ureg = UnitRegistry()
Q_=ureg.Quantity

from blog.config import MULTIPLE_INVERSE
from math import log10
import re

links = None
country_codes = None
cia_country_names = None
country_stats = None

def sigfigs(x,n):
    negative = False
    if x ==0:
        return 0
    if x<0:
        return -sigfigs(-x,n)
    l10 = 1+round(log10(x),0)
    x = round(x, int(n-l10))
    if (x==round(x)):
        return int(x)
    else:
        return x

def output(x):
    if x/1000000000000 ==int(x/1000000000000):
        return  "{:,.0f} trillion".format(x/1000000000000)    
    if x/1000000000 ==int(x/1000000000):
        return  "{:,.0f} billion".format(x/1000000000)    
    elif x/1000000 ==int(x/1000000):
        return  "{:,.0f} million".format(x/1000000)    
    elif x/1000 ==int(x/1000):
        return  "{:,.0f} thousand".format(x/1000)    
    elif x==int(x):
        return  "{:,.0f}".format(x)    
    else:
        return "{:,f}".format(x).rstrip('0')    

def currency_output(x):
    x = sigfigs(x,6)
    if x/1000000000000 ==int(x/1000000000000):
        return  "{:,.0f} trillion".format(x/1000000000000)    
    elif x>1000000000000:
        return  "{:,.3f} trillion".format(x/1000000000000)    
    elif x/1000000000 ==int(x/1000000000):
        return  "{:,.0f} billion".format(x/1000000000)    
    elif x>1000000000:
        return  "{:,.3f} billion".format(x/1000000000)    
    elif x/1000000 ==int(x/1000000):
        return  "{:,.0f} million".format(x/1000000)    
    elif x>1000000:
        return  "{:,.3f} million".format(x/1000000)    
    elif x/1000 ==int(x/1000):
        return  "{:,.0f} thousand".format(x/1000)    
    elif x==int(x):
        return  "{:,.0f}".format(x)    
    else:
        return "{:,.2f}".format(x)
        """
    x = sigfigs(x,6)
    if x/1000000000000 ==int(x/1000000000000):
        return  "{:,.0f} trillion".format(x/1000000000000)    
    elif x/1000000000 ==int(x/1000000000):
        return  "{:,.0f} billion".format(x/1000000000)    
    elif x/1000000 ==int(x/1000000):
        return  "{:,.0f} million".format(x/1000000)    
    elif x/1000 ==int(x/1000):
        return  "{:,.0f} thousand".format(x/1000)    
    elif x==int(x):
        return  "{:,.0f}".format(x)    
    else:
        return "{:,.2f}".format(x)
"""

def num(s):
    return float(s)

def getMultiple(scale):
    if scale == -3:
        return "thousandth"
    if scale == 0:
        return "unit"
    elif scale == 3:
        return "thousand"
    elif scale == 6:
        return "million"
    elif scale == 9:
        return "billion"
    elif scale == 12:
        return "trillion"
    elif scale == 15:
        return "quadrillion"
    elif scale == 18:
        return "quintillion"
    elif scale == 21:
        return "sextillion"
    elif scale == 24:
        return "septillion"
    elif scale == 27:
        return "octillion"
    else:
        return "10^"+str(scale)

def getScaleFactor(multiple):
    if multiple.find("^")>0:
        scale = int(num(multiple.split('^')[1]))
    elif multiple == "Y":
        scale = 24
    elif multiple == "Z":
        scale = 21
    elif multiple == "E":
        scale = 18
    elif multiple == "P":
        scale = 15
    elif multiple == "T":
        scale = 12
    elif multiple == "G":    
        scale = 9
    elif multiple == "M":    
        scale = 6
    elif multiple == "k":    
        scale = 3
    elif multiple == "U":
        scale = 0
    elif multiple == "m":
        scale = -3
    else:
        scale = 0
    return scale, 10**scale

std_units = {
    "":"i",
    "$":"USD",
    "dollar":"USD",
    "dollars":"USD",
    "usd":"USD",
    "£":"GBP",
    "pounds":"GBP",
    "sterling":"GBP",
    "gbp":"GBP",
    "€":"EUR",
    "euro":"EUR",
    "euros":"EUR",
    "eur":"EUR",
    "¥":"JPY",
    "yen":"JPY",
    "jpy":"JPY",
    "aud":"AUD",
    "cad":"CAD",
    "chf":"CHF",
    "hkd":"HKD",
    "miles":"mile",
    "yards":"yard",
    "yd":"yard",
    "feet":"foot",
    "ft":"foot",
    "inches":"inch",
    "in":"inch",
    "years":"year",
    "yrs":"year",
    "yr":"year",
    "y":"year",
    "months":"month",
    "mth":"month",
    "weeks":"week",
    "wk":"week",
    "days":"day",
    "dy":"dy",
    "d":"d",
    "hours":"hour",
    "hrs":"hour",
    "hr":"hour",
    "h":"hour",
    "minutes":"minute",
    "mins":"minute",
    "min":"minute",
    "mn":"minute",
    "seconds":"second",
    "secs":"second",
    "sec":"second",
    "s":"second",
    "J":"Joule",
}

std_multiples = {
    "thousandth":"m",
    "thousand":"k",
    "thou":"k",
    "grand":"k",
    "m":"M",
    "mil":"M",
    "mill":"M",
    "million":"M",
    "b":"G",
    "bn":"G",
    "billion":"G",
    "t":"T",
    "trillion":"T",
}

def succ(multiple):
    mults={"m":"U", "U":"k", "k":"M", "M":"G", "G":"T", "T":"P", "P":"E",
        "E":"Z", "Z":"Y", "Y":"10^27", "10^27":"10^30", "10^30":"10^33", "10^33":"10^36", "10^36":"10^39", "10^39":"10^42"}
    if multiple in mults:
        return mults[multiple]
    else:        
        return None

def prec(multiple):
    mults={"U":"m", "k":"U", "M":"k", "G":"M", "T":"G", "P":"T", "E":"P",
        "Z":"E", "Y":"Z", "10^27":"Y", "10^30":"10^27", "10^33":"10^30", "10^36":"10^33", "10^39":"10^36", "10^42":"10^39"}
    if multiple in mults:
        return mults[multiple]
    else:        
        return None


def normalise(parsed):
    magnitude, multiple, unit = parsed
    if (multiple=="U" and unit.lower() in std_multiples and unit.lower()!="m"):
        multiple=unit
        unit="i"
    if unit.lower() in std_units.keys():
        unit = std_units[unit.lower()]
    measure = getMeasure(unit)   
    if multiple.lower() in std_multiples.keys():
        multiple = std_multiples[multiple.lower()]

    negative = False
    value = num(magnitude)
    if value!=0:
        if value < 0:
            negative = True
            value = -value
        while value>1000:
            value=value/1000
            value = sigfigs(value,6)
            multiple = succ(multiple)
        while value<1 and multiple!="U":
            value=value*1000
            value = sigfigs(value,6)
            multiple = prec(multiple)

        if negative:
            value = -value
        magnitude = str(value)
    return magnitude, multiple, unit, measure 

def normalise_nf(nf):
    nf.magnitude, nf.multiple, nf.unit, nf.measure = normalise((nf.magnitude, MULTIPLE_INVERSE[nf.scale], nf.unit))
    return nf

def getMeasure(unit):
    try:
        dim = ureg.parse_expression(unit).dimensionality 
        if dim == ureg.parse_expression('m').dimensionality :
            return "e"
        elif dim == ureg.parse_expression('s').dimensionality :
            return "d"
        elif dim == ureg.parse_expression('kg').dimensionality :
            return "m"
        else:
            return "?"
    except UndefinedUnitError:
        p = re.compile("^[A-Z]{3}$")
        m=p.match(unit)
        if m!=None:
            return "a"
        else:
            return "c"

def errorParsed():
    magnitude = "0"
    multiple = "U"
    unit = "i"
    measure ="c"
    return magnitude, multiple, unit, measure 

def literalParsed(literal):
    magnitude = "1"
    multiple = "?"
    unit = literal
    measure ="c"
    return magnitude, multiple, unit, measure 


def parseNumber(big_number, regex):
    p = re.compile(regex)
    m=p.match(big_number)
    if (m==None):
        return m
    else:      
        try:
            literal = m.group('literal')
            if literal:
                return literalParsed(literal)   
        except:
            pass
        magnitude = m.group('magnitude')
        unit = m.group('unit')
        multiple = 'U'
        try:
            multiple = m.group('multiple')
        except:
            pass
        return normalise((magnitude, multiple, unit))


def parseBigNumber(big_number):
    big_number=big_number.replace(",","")
    parsed = parseNumber(big_number,"^(?P<magnitude>[\-0-9\.e]+)\s*(?P<unit>[a-zA-Z/£$€¥]*(\^-?[0-9]*)?)$")
    if (parsed != None):
        return parsed
    parsed = parseNumber(big_number,"^(?P<unit>[a-zA-Z\/£$€¥](\^-?[0-9]*)?)\s*(?P<magnitude>[\-0-9\.e]+)$")
    if (parsed != None):
        return parsed
    parsed = parseNumber(big_number,"^(?P<magnitude>[\-0-9\.e]+)\s*(?P<multiple>[a-zA-Z]*)\s*(?P<unit>[a-zA-Z/£$€¥]*(\^-?[0-9]*)?)$")
    if (parsed != None):
        return parsed
    parsed = parseNumber(big_number,"^(?P<literal>[\w\s'-]+)$")
    if (parsed != None):
        return parsed
    parsed = parseNumber(big_number,"^(?P<unit>[a-zA-Z/£$€¥]*(\^-?[0-9]*)?)\s*(?P<magnitude>[\-0-9\.e]+)\s*(?P<multiple>[a-zA-Z]*)$")
    if (parsed != None):
        return parsed
    parsed = parseNumber(big_number,"^(?P<magnitude>[\-0-9\.e]+)$")
    if (parsed != None):
        return parsed
    return errorParsed()


def tests():
    parsed = parseBigNumber("100 thou GBP")
    print(parsed)
    parsed = parseBigNumber("100kg")
    print(parsed)
    #parsed = parseBigNumber("100m/s")
    #print(parsed)
    #parsed = parseBigNumber("10m/s^2")
    #print(parsed)
    #parsed = parseBigNumber("USD25.56")
    #print(parsed)
    #parsed = parseBigNumber("USD 25.56")
    #print(parsed)
    parsed = parseBigNumber("$25.56")
    print(parsed)
    parsed = parseBigNumber("£25.56")
    print(parsed)
    parsed = parseBigNumber("25.56$")
    print(parsed)
    parsed = parseBigNumber("25.56 £")
    print(parsed)
    #parsed = parseBigNumber("2.5 bn people")
    #print(parsed)
    #parsed = parseBigNumber("2.5bn people")
    #print(parsed)
    #parsed = parseBigNumber("$25.56m")
    #print(parsed)
    #parsed = parseBigNumber("GBP 25.56m")
    #print(parsed)
    #parsed = parseBigNumber("AUD 25.56 bn")
    #print(parsed)
    #parsed = parseBigNumber("25.56")
    #print(parsed)
    #parsed = parseBigNumber("2556000000")
    #print(parsed)
    parsed = parseBigNumber("255,600,000.3")
    print(parsed)
    parsed = parseBigNumber("8000.3")
    print(parsed)
    parsed = parseBigNumber("255,600,123,000.3")
    print(parsed)
    parsed = parseBigNumber("30e36")
    print(parsed)
    parsed = parseBigNumber("Graham's Number")
    print(parsed)
    parsed = parseBigNumber("100m")
    print(parsed)

#tests()

def measure_filter_upper(klass, magnitude_adj, scale_adj, measure):
    if (scale_adj<0):
        magnitude_adj = magnitude_adj * 10** scale_adj
        scale_adj = 0
    truncate_measure = measure[:measure.find(".")]
    matches = []
    match1 = klass.objects.filter(value__gte=magnitude_adj, scale=scale_adj, measure__startswith=measure)
    for fact in match1:
        matches.append(fact)
    match2 = klass.objects.filter(value__gte=magnitude_adj, scale=scale_adj, measure=truncate_measure)
    for fact in match2:
        matches.append(fact)
    return sorted(matches, key = lambda k: k.value)


def measure_filter_lower(klass, magnitude_adj, scale_adj, measure):
    if (scale_adj<0):
        magnitude_adj = magnitude_adj * 10** scale_adj
        scale_adj = 0
    truncate_measure = measure[:measure.find(".")]
    matches = []
    match1 = klass.objects.filter(value__lte=magnitude_adj, scale=scale_adj, measure__startswith=measure)
    for fact in match1:
        matches.append(fact)
    match2 = klass.objects.filter(value__lte=magnitude_adj, scale=scale_adj, measure=truncate_measure)
    for fact in match2:
        matches.append(fact)
    return sorted(matches, key = lambda k: k.value)



def bracketNumber(klass, magnitude, scale, measure):
    #tolerance=10000
    response = []
#   nf_gt = klass.objects.filter(value__gt=num(magnitude)*1, value__lt=num(magnitude)*1*(1+tolerance), scale=scale-0, measure=measure).order_by("value")
    nf_gt = measure_filter_upper(klass, num(magnitude)*1, scale-0, measure)
    if len(nf_gt)==0:
        nf_gt = measure_filter_upper(klass, num(magnitude)/1000, scale+3, measure)
    if len(nf_gt)==0:
        nf_gt = measure_filter_upper(klass, num(magnitude)/1000000, scale+6, measure)
    if len(nf_gt)==0:
        nf_gt = measure_filter_upper(klass, num(magnitude)/1000000000, scale+9, measure)

    nf_lt = measure_filter_lower(klass, num(magnitude)*1, scale-0, measure)
    if len(nf_lt)==0:
        nf_lt = measure_filter_lower(klass, num(magnitude)*1000, scale-3, measure)
    if len(nf_lt)==0:
        nf_lt = measure_filter_lower(klass, num(magnitude)*1000000, scale-6, measure)
    if len(nf_lt)==0:
        nf_lt = measure_filter_lower(klass, num(magnitude)*1000000000, scale-9, measure)

    if len(nf_gt)==0:
        response.append("No useful upper bracket on file")
    else:           
        response.append(" ".join([nf_gt[0].render_folk_long]))
    if len(nf_lt)==0:
        response.append("No useful lower bracket on file")
    else:           
        response.append(" ".join([nf_lt[-1].render_folk_long]))
    return response


def closeEnoughNumberFact(klass, magnitude, scale, tolerance, measure):
#   nf = klass.objects.filter(magnitude__gt=800, scale=scale)
    facts = []
    nf = klass.objects.filter(value__gte=num(magnitude)*1000/(1+tolerance), value__lt=num(magnitude)*1000*(1+tolerance), scale=scale-3, measure=measure)
    for fact in nf:
        facts.append(fact)
    nf = klass.objects.filter(value__gte=num(magnitude)/(1+tolerance), value__lt=num(magnitude)*(1+tolerance), scale=scale, measure=measure)
    for fact in nf:
        facts.append(fact)
    nf = klass.objects.filter(value__gte=num(magnitude)/1000/(1+tolerance), value__lt=num(magnitude)/1000*(1+tolerance), scale=scale+3, measure=measure)
    for fact in nf:
        facts.append(fact)
    return facts

def range_matches(klass, scale_lower, scale_upper, value_lower, value_upper, measure):
    if measure.find(".")<0: 
        return klass.objects.filter(scale__gte=scale_lower, scale__lte=scale_upper, value__gte=value_lower, value__lt=value_upper, measure__startswith=measure).exclude(measure__contains="~")
    else:
        truncate_measure = measure[:measure.find(".")]
        matches = []
        match1 = klass.objects.filter(scale__gte=scale_lower, scale__lte=scale_upper, value__gte=value_lower, value__lt=value_upper, measure=measure)
        for fact in match1:
            matches.append(fact)
        match2 = klass.objects.filter(scale__gte=scale_lower, scale__lte=scale_upper, value__gte=value_lower, value__lt=value_upper, measure=truncate_measure)
        for fact in match2:
            matches.append(fact)
        return matches


def closeMagnitudeNumberFact(klass, magnitude, measure, tolerance, multiple, scale, scale_tolerance = 30):
#   nf = klass.objects.filter(magnitude__gt=800, scale=scale)
    mag = num(magnitude)*multiple
    if mag > 1000:
        mag = mag/1000
    elif mag > 100:
        mag = mag/100
    elif mag > 10:
        mag = mag/10
    elif mag < 1:
        mag = mag*10
    facts = []
#    nf = klass.objects.filter(scale__gte=scale-scale_tolerance, scale__lte=scale+scale_tolerance, value__gte=mag/(1+tolerance), value__lt=mag*(1+tolerance), measure=measure)
    nf = range_matches(klass, scale-scale_tolerance, scale+scale_tolerance, mag/(1+tolerance), mag*(1+tolerance), measure)
    for fact in nf:
        facts.append(fact)
#    nf = klass.objects.filter(scale__gte=scale-1-scale_tolerance, scale__lte=scale-1+scale_tolerance, value__gte=mag*10/(1+tolerance), value__lt=mag*10*(1+tolerance), measure=measure)
    nf = range_matches(klass, scale-1-scale_tolerance, scale-1+scale_tolerance, mag*10/(1+tolerance), mag*10*(1+tolerance), measure)
    for fact in nf:
        facts.append(fact)
#    nf = klass.objects.filter(scale__gte=scale-2-scale_tolerance, scale__lte=scale-2+scale_tolerance, value__gte=mag*100/(1+tolerance), value__lt=mag*100*(1+tolerance), measure=measure)
    nf = range_matches(klass, scale-2-scale_tolerance, scale-2+scale_tolerance, mag*100/(1+tolerance), mag*100*(1+tolerance), measure)
    for fact in nf:
        facts.append(fact)
    return facts



def numberFactsLikeThis(klass, nf, rseed=None):
#    tolerances=[0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10, 25, 50, 100]
    if rseed != None:
        seed(rseed)
    tolerances=[1.0, 2.5, 5.0, 10, 25, 50, 100]
    for tolerance in tolerances:
        ce=closeEnoughNumberFact(klass, nf.magnitude, nf.scale, tolerance, nf.measure)
        try:
            ce.remove(nf)
        except:
            pass
        candidates = []
        for nf_a in ce:
            duplicate = False
            for nf_b in candidates:
                if nf_b.value == nf_a.value:
                    duplicate = True
                    break
            if  not(duplicate):
                candidates.append(nf_a)    

        if len(candidates)>=4:
            bestTolerance = tolerance
            bestComparisons = sample(candidates[1:-1],2)
            bestComparisons.append(candidates[0])
            bestComparisons.append(candidates[-1])
            bestComparisons = sample(bestComparisons,4)
            break
        bestTolerance = tolerance
        bestComparisons = sample(candidates,len(candidates))
    score = round(1*log10(bestTolerance/1000)**2)*(len(bestComparisons)-1)
    return bestComparisons, bestTolerance, score

def biggestNumberFact(nfs):
    biggestValue= 0
    biggestFact = None
    for fact in nfs:
        value = num(fact.magnitude) * 10**num(fact.scale)
        if value > biggestValue:
            biggestFact = fact
            biggestValue = value
    return biggestFact

def smallestNumberFact(nfs):
    smallestValue= 1e100
    smallestFact = None
    for fact in nfs:
        value = num(fact.magnitude) * 10**num(fact.scale)
        if value < smallestValue:
            smallestFact = fact
            smallestValue = value
    return smallestFact

def randomFact(klass, measure, rseed=None):
    if rseed!=None:
        seed(rseed)
    else:
        seed()
    if measure[-1]=="!":
        candidates = klass.objects.filter(measure=measure[:-1])    
    else:
        candidates = klass.objects.filter(measure__startswith=measure)    
    count = candidates.count()
    rf = candidates[randint(0,count-1)]
    return rf

def randomFactAny(klass, rseed=None):
    if rseed!=None:
        seed(rseed)
    count = klass.objects.filter().count()
    rf = klass.objects.filter()[randint(0,count-1)]
    return rf

def renderMult(value):
    if int(value)== value:
        return str(int(value))
    else:
        return str(value)

def renderInt(i):
    if i >= 1000000000000000:
        return " ".join([renderMult(i/1000000000000000),"quadrillion"])
    elif i >= 1000000000000:
        return " ".join([renderMult(i/1000000000000),"trillion"])
    elif i >= 1000000000:
        return " ".join([renderMult(i/1000000000),"billion"])
    elif i >= 1000000:
        return " ".join([renderMult(i/1000000),"million"])
    elif i >= 1000:
        return " ".join([renderMult(i/1000),"thousand"])
    else:
        return(str(i))




def spuriousFact(klass, scale_tolerance, measure=None):
    facts = []
    if measure == None:
        measure=choice(["extent","extent","count", "amount!", "duration","mass","mass"])
    tolerance = 0.01
    while len(facts)==0:
#        seed = randint(0,1000000)
        rf = randomFact(klass, measure, rseed=None)
        facts = closeMagnitudeNumberFact(klass, rf.magnitude, rf.measure, tolerance, 1, rf.scale, scale_tolerance=scale_tolerance)
        try:
            facts.remove(rf)
        except:
            pass
        facts2 = closeMagnitudeNumberFact(klass, rf.magnitude, rf.measure,tolerance, 2, rf.scale, scale_tolerance=scale_tolerance)
        facts+=facts2
#        facts2b = closeMagnitudeNumberFact(klass, rf.magnitude, rf.measure,tolerance, 0.5)
#        facts+=facts2b
        facts4 = closeMagnitudeNumberFact(klass, rf.magnitude, rf.measure,tolerance, 4, rf.scale, scale_tolerance=scale_tolerance)
        facts+=facts4
        facts3 = closeMagnitudeNumberFact(klass, rf.magnitude, rf.measure,tolerance, 3, rf.scale, scale_tolerance=scale_tolerance)
        facts+=facts3
        facts4b = closeMagnitudeNumberFact(klass, rf.magnitude, rf.measure,tolerance, 0.25, rf.scale, scale_tolerance=scale_tolerance)
        facts+=facts4b
        facts5 = closeMagnitudeNumberFact(klass, rf.magnitude, rf.measure,tolerance, 5, rf.scale, scale_tolerance=scale_tolerance)
        facts+=facts5
 #       facts5b = closeMagnitudeNumberFact(klass, rf.magnitude, rf.measure,tolerance, 0.2)
 #       facts+=facts5b
    fact2 = choice(facts)
    ratio = (rf.value/fact2.value)*10**(rf.scale - fact2.scale)
    if ratio > 1:
        fact1 = rf
    else:
        fact1 = fact2
        fact2 = rf

    ratio = (fact1.value/fact2.value)*10**(fact1.scale - fact2.scale)
    intRatio = sigfigs(ratio, 2)
    if intRatio==1:
        comparison = "is about as big as"
    else:
        comparison = " ".join(["is", renderInt(intRatio), "x"])
    return {"fact1":fact1.render_folk, "fact1_link": fact1.link, "comparison":comparison, "fact2":fact2.render_folk, "fact2_link": fact2.link}



def neatRatio(klass, selectedFact, ratio, tolerance=0.02):
    rf = klass()
    rf.magnitude = str(num(selectedFact.magnitude)/ratio)
    rf.title = str(ratio)+" times "+selectedFact.title
    rf.measure = selectedFact.measure
    rf.scale = selectedFact.scale
    rf.multiple = selectedFact.multiple
    rf.unit = selectedFact.unit
    rf.normalise()
    facts = closeEnoughNumberFact(klass, rf.magnitude, rf.scale, tolerance, rf.measure)
    return facts

def facts_matching_ratio(klass, measure, ratio, target, tolerance = 0.02):
    seed = randint(0,1000000)
    target_facts = []
    used = []
    count = 0
    while len(target_facts) < target and count < 100:
        count+=1
        rf = randomFact(klass, measure)
        while rf in used:
            rf = randomFact(klass, measure)
        used.append(rf)
        facts = neatRatio(klass, rf, ratio, tolerance=tolerance)
        if rf in facts:
            facts.remove(rf)
        if facts:
            target_facts.append((rf, facts[0]))
    return target_facts



def neatFacts(klass, selectedFact, tolerance = 0.02):
    rf = selectedFact
    maxRatio = {"extent":10000, "extent.hor":10000, "extent.ver":10000, "mass":20000, "duration":10000, "duration.age":10000, "duration.span":10000, "count":500, "count.pop":500, "amount":500, "volume":10000, "area":10000, "energy":1000}[rf.measure]

    facts = closeMagnitudeNumberFact(klass, rf.magnitude, rf.measure, tolerance, 1, rf.scale)
    try:
        facts.remove(rf)
    except:
        pass
    facts2 = closeMagnitudeNumberFact(klass, rf.magnitude, rf.measure,tolerance, 2, rf.scale)
    facts+=facts2
#    facts2b = closeMagnitudeNumberFact(klass, rf.magnitude, rf.measure,tolerance, 0.5)
#    facts+=facts2b
    facts4 = closeMagnitudeNumberFact(klass, rf.magnitude, rf.measure,tolerance, 4, rf.scale)
    facts+=facts4
    facts4b = closeMagnitudeNumberFact(klass, rf.magnitude, rf.measure,tolerance, 0.25, rf.scale)
    facts+=facts4b
    facts5 = closeMagnitudeNumberFact(klass, rf.magnitude, rf.measure,tolerance, 5, rf.scale)
    facts+=facts5
#    facts5b = closeMagnitudeNumberFact(klass, rf.magnitude, rf.measure,tolerance, 0.2)
#    facts+=facts5b

    neat = []

    for fact in facts:
        raw_ratio = (rf.value/fact.value)*10**(rf.scale - fact.scale)

        if raw_ratio < 1:
            intRatio = sigfigs(1/raw_ratio, 2)
        else:
            intRatio = sigfigs(raw_ratio, 2)
        if intRatio==1:
            comparison = "is about as big as"
        elif raw_ratio < 1:
            comparison = "".join(["is 1/", renderMult(intRatio), " of"])
        else:
            comparison = "".join(["is ", renderMult(intRatio), " x"])
        comparison = comparison.replace("1/2.5", "2/5")
        if intRatio <= maxRatio:
            neat = neat+[{"fact1":rf, "comparison":comparison, "fact2":fact, "fact2render":fact.render2, "ratio":raw_ratio}]
    neat = sorted(neat, key = lambda k: k['ratio'])
    return neat

def get_article(article_name):
    #print(BASE_DIR)
    filen = os.path.join(BASE_DIR,"blog", "static", "md",article_name)
    with open (filen, "r") as artfile:
        content=artfile.read()        
    return content

def load_link_redirects(fileName, encoding="UTF-8"):
    inFile= open(fileName, encoding=encoding)
    lines = inFile.readlines()
    links = {}
    for line in lines[0:]:
        try:
            key, value = line.strip().split("|")
            links[key]= value
        except:
            print("could not parse line:"+line)
    inFile.close()
    return links

def save_link_redirects(links, fileName, encoding="UTF-8"):
    outFile= open(fileName, "w", encoding=encoding)
    for key in sorted(links.keys(), key = lambda k: k):
        line = key+"|"+links[key]+"\n"
        outFile.write(line)

def resolve_link(key):
    global links
    if links==None:
        links = load_link_redirects(os.path.join(BASE_DIR, "blog/data/links.txt"))
#    print("links")
#    print(links)
    try:
        return links[key]
    except:
        links = load_link_redirects(os.path.join(BASE_DIR, "blog/data/links.txt"))
        try:
            return links[key]
        except:
            return "http://IsThatABigNumber.com/sponsor"

def save_links():
    global links
    if links!=None:
        filename = os.path.join(BASE_DIR, "blog/data/links.txt")
        save_link_redirects(links, filename)
        return filename
    else: 
        return "n/a"

def poke_link(link, key):
    global links
    if links==None:
        links = load_link_redirects(os.path.join(BASE_DIR, "blog/data/links.txt"))
    links[key]=link


def load_country_codes(fileName, encoding="UTF-8"):
    inFile= open(fileName, encoding=encoding)
    lines = inFile.readlines()
    country_codes = {}
    cia_country_names = {}
    for line in lines[0:]:
        try:
            key, cia, country = line.strip().split(",")
            if cia[0]=='"':
                cia = cia[1:-2]
            if country[0]=='"':
                country = country[1:-2]
            country_codes[key]=country
            cia_country_names[cia]=key
        except:
            print("could not parse line:"+line)
    inFile.close()
    return country_codes, cia_country_names

def resolve_country_code(key):
    global country_codes, cia_country_names
    if country_codes==None:
        country_codes, cia_country_names = load_country_codes(os.path.join(BASE_DIR, "blog/data/CountryCodes.csv"))
    try:
        return country_codes[key]
    except:
        return "unknown country code "+key

def get_country_codes():
    return load_country_codes(os.path.join(BASE_DIR, "blog/data/CountryCodes.csv"))

def country_code_list():
    cc_dict = get_country_codes()[0]
    cc_list = []
    for key in cc_dict.keys():
#        cc_list.append((key, key+":"+cc_dict[key]))
        cc_list.append((key, cc_dict[key]))
    return sorted(cc_list, key = lambda k: k[1])


def resolve_cia_country(name):
    global country_codes, cia_country_names
    if cia_country_names==None:
        country_codes, cia_country_names = load_country_codes(os.path.join(BASE_DIR, "blog/data/CountryCodes.csv"))
    try:
        code = cia_country_names[name]
        return country_codes[code], code
    except:
        return "unknown country name "+name

def val_from(fact):
    return float(fact.magnitude)*10**fact.scale

def make_number(klass, magnitude, title, measure, unit):
    nf = klass(magnitude=magnitude, multiple="unit", scale=0, unit=unit, measure = measure, title = title, value=num(magnitude))
    return nf

def make_amount(klass, magnitude, title, unit="USD"):
    nf = klass(magnitude=magnitude, multiple="unit", scale=0, unit=unit, measure = "amount", title = title, value=num(magnitude))
    return nf

def make_perc(klass, magnitude, title):
    nf = klass(magnitude=magnitude, multiple="unit", scale=0, unit="%", measure = "perc", title = title, value=num(magnitude))
    return nf

def make_count(klass, magnitude, title, unit):
    nf = klass(magnitude=magnitude, multiple="unit", scale=0, unit=unit, measure = "count", title = title, value=num(magnitude))
    return nf


def summarise_country(klass, code, qamount, currency="USD"):
    response = {}
    location = code
    country = resolve_country_code(location)
    response["country"] = country
    #facts = klass.objects.filter(location__icontains = location).order_by('title')  
    #for fact in facts:
    #   print(fact.render_folk)
    spend = klass.objects.filter(location__icontains = location, title__icontains = "Govt spending").order_by('-date')[0]  
    spend = spend.getConversions([currency])[0]
    tax = klass.objects.filter(location__icontains = location, title__icontains = "Total taxation").order_by('-date')[0]  
    tax = tax.getConversions([currency])[0]
    GDP = klass.objects.filter(location__icontains = location, title__icontains = "GDP in").order_by('-date')[0]  
    GDP = GDP.getConversions([currency])[0]
    pop = klass.objects.filter(location__icontains = location, title__icontains = "Population of").order_by('-date')[0]  
    land = klass.objects.filter(location__icontains = location, title__icontains = "Land Area of").order_by('-date')[0]  
    try:
        debt = klass.objects.filter(location__icontains = location, title__icontains = "National Debt").order_by('-date')[0]  
        debt = debt.getConversions([currency])[0]
    except:
        debt = None
    try:
        hhcons = klass.objects.filter(location__icontains = location, title__icontains = "Household Consumption").order_by('-date')[0]  
        hhcons = hhcons.getConversions([currency])[0]
    except:
        hhcons = None
    try:
        gvcons = klass.objects.filter(location__icontains = location, title__icontains = "Government Consumption").order_by('-date')[0]  
        gvcons = gvcons.getConversions([currency])[0]
    except:
        gvcons = None
    try:
        invcap = klass.objects.filter(location__icontains = location, title__icontains = "Investment in Capital").order_by('-date')[0]  
        invcap = invcap.getConversions([currency])[0]
    except:
        invcap = None
    try:
        invinv = klass.objects.filter(location__icontains = location, title__icontains = "Investment in Inventories").order_by('-date')[0]  
        invinv = invinv.getConversions([currency])[0]
    except:
        invinv = None
    try:
        exports = klass.objects.filter(location__icontains = location, title__icontains = "Exports").order_by('-date')[0]  
        exports = exports.getConversions([currency])[0]
    except:
        exports = None
    try:
        imports = klass.objects.filter(location__icontains = location, title__icontains = "Imports").order_by('-date')[0]  
        imports = imports.getConversions([currency])[0]
    except:
        imports = None

    try:
        agri = klass.objects.filter(location__icontains = location, title__icontains = "Agricultural").order_by('-date')[0]  
        agri = agri.getConversions([currency])[0]
    except:
        agri = None
    try:
        industry = klass.objects.filter(location__icontains = location, title__icontains = "Industrial").order_by('-date')[0]  
        industry = industry.getConversions([currency])[0]
    except:
        industry = None
    try:
        services = klass.objects.filter(location__icontains = location, title__icontains = "Services").order_by('-date')[0]  
        services = services.getConversions([currency])[0]
    except:
        services = None
    try:
        agriland = klass.objects.filter(location__icontains = location, title__icontains = "Land used for agriculture").order_by('-date')[0]  
    except:
        agriland = None
    try:
        forest = klass.objects.filter(location__icontains = location, title__icontains = "Forest").order_by('-date')[0]  
    except:
        forest = None
    try:
        other = klass.objects.filter(location__icontains = location, title__icontains = "Other land").order_by('-date')[0]  
    except:
        other = None
    basics = {"GDP": GDP, "Population":pop, "Land":land,
            "GDP per capita": make_amount(klass, str(round(val_from(GDP)/val_from(pop),0)), "GDP per capita", unit=currency),
            "Population density": make_count(klass, str(round(1000000*val_from(pop)/val_from(land),0)), "Population density", "people")
    }
    response["basics"]= basics
    deficit = make_amount(klass, str(round(val_from(spend) - val_from(tax),0)), "Deficit", unit=currency)
    deficit.normalise()
    tax_spend = {
        "tax": tax,
#        "tax/capita": round(val_from(tax)/val_from(pop),0),
        "tax/capita": make_amount(klass, str(round(val_from(tax)/val_from(pop),0)), "tax/capita", unit=currency),
#        "tax/GDP": round(100*val_from(tax)/val_from(GDP),0),
        "tax/GDP": make_perc(klass, str(round(100*val_from(tax)/val_from(GDP),0)), "tax/GDP"),
        "spend": spend,
        "spend/capita": make_amount(klass, str(round(val_from(spend)/val_from(pop),0)), "spend/capita", unit=currency),
        "spend/GDP": make_perc(klass, str(round(100*val_from(spend)/val_from(GDP),0)), "spend/GDP"),
#        "deficit": normalise_nf(make_amount(klass, str(round(deficit,0)), "deficit")),
        "deficit": deficit,
        "deficit/capita": make_amount(klass, str(round(val_from(deficit)/val_from(pop),0)), "deficit/capita", unit=currency),
        "deficit/GDP": make_perc(klass, str(round(100*val_from(deficit)/val_from(GDP),0)), "deficit/GDP"),
        "deficit/spend": make_perc(klass, str(round(100*val_from(deficit)/val_from(spend),0)), "deficit/spend"),
    }
    response["tax_spend"]= tax_spend
    if debt:
        nat_debt = {
        "nat_debt": debt,
        "debt/capita": make_amount(klass, str(round(val_from(debt)/val_from(pop),0)), "debt/capita", unit=currency),
        "debt/GDP": make_perc(klass, str(round(100*val_from(debt)/val_from(GDP),0)), "debt/GDP"),
        }
        response["nat_debt"]=nat_debt
    uses = {}
    if hhcons:
        uses["hhcons"] = hhcons
        uses["hhcons/capita"] = make_amount(klass, str(round(val_from(hhcons)/val_from(pop),0)), "HC/capita", unit=currency)
        uses["hhcons/GDP"]= make_perc(klass, str(round(100*val_from(hhcons)/val_from(GDP),0)), "HC/GDP")
    if gvcons:
        uses["gvcons"] = gvcons
        uses["gvcons/capita"]= make_amount(klass, str(round(val_from(gvcons)/val_from(pop),0)), "GC/capita", unit=currency)
        uses["gvcons/GDP"]= make_perc(klass, str(round(100*val_from(gvcons)/val_from(GDP),0)), "GC/GDP")
    if invcap and invinv:
        inv =make_amount(klass, str(round(val_from(invcap)+val_from(invinv),0)), "Investment", unit=currency)
        uses["inv"] = inv
        inv.normalise()
        uses["inv/capita"] = make_amount(klass, str(round(val_from(inv)/val_from(pop),0)), "Inv/capita", unit=currency)
        uses["inv/GDP"] = make_perc(klass, str(round(100*val_from(inv)/val_from(GDP),0)), "Inv/GDP")
    if invcap:
        uses["invcap"] = invcap
        uses["invcap/capita"] = make_amount(klass, str(round(val_from(invcap)/val_from(pop),0)), "IC/capita", unit=currency)
        uses["invcap/GDP"] = make_perc(klass, str(round(100*val_from(invcap)/val_from(GDP),0)), "IC/GDP")
    if invinv:
        uses["invinv"] = invinv
        uses["invinv/capita"] = make_amount(klass, str(round(val_from(invinv)/val_from(pop),0)), "II/capita", unit=currency)
        uses["invinv/GDP"] = make_perc(klass, str(round(100*val_from(invinv)/val_from(GDP),0)), "II/GDP")
    if exports:
        uses["exports"] = exports
        uses["exports/capita"] = make_amount(klass, str(round(val_from(exports)/val_from(pop),0)), "exports/capita", unit=currency)
        uses["exports/GDP"] = make_perc(klass, str(round(100*val_from(exports)/val_from(GDP),0)), "exports/GDP")
    if imports:
        uses["imports"] = imports
        uses["imports/capita"] = make_amount(klass, str(round(val_from(imports)/val_from(pop),0)), "imports/capita", unit=currency)
        uses["imports/GDP"] = make_perc(klass, str(round(100*val_from(imports)/val_from(GDP),0)), "imports/GDP")
    response["uses"]= uses
    sources = {}
    if agri:
        sources["agriculture"] = agri
        sources["agri/capita"] = make_amount(klass, str(round(val_from(agri)/val_from(pop),0)), "agr.prod/capita", unit=currency)
        sources["agri/GDP"] = make_perc(klass, str(round(100*val_from(agri)/val_from(GDP),0)), "agr.prod/GDP")
    if industry:
        sources["industry"] = industry
        sources["industry/capita"] = make_amount(klass, str(round(val_from(industry)/val_from(pop),0)), "ind.prod/capita", unit=currency)
        sources["industry/GDP"] = make_perc(klass, str(round(100*val_from(industry)/val_from(GDP),0)), "ind.prod/GDP")
    if services:
        sources["services"] = services
        sources["services/capita"] = make_amount(klass, str(round(val_from(services)/val_from(pop),0)), "serv.prod/capita", unit=currency)
        sources["services/GDP"] = make_perc(klass, str(round(100*val_from(services)/val_from(GDP),0)), "serv.prod/GDP")
    response["sources"] = sources
    landuse = {}
    if agriland:
        landuse["agriland"] = agriland
        landuse["agriland/land"] = make_perc(klass, str(round(100*val_from(agriland)/val_from(land),0)), "agricultural land %")
    if forest:
        landuse["forest"] = forest
        landuse["forest/land"] = make_perc(klass, str(round(100*val_from(forest)/val_from(land),0)), "forest %")
    if other:
        landuse["other"] = other
        landuse["other/land"] = make_perc(klass, str(round(100*val_from(other)/val_from(land),0)), "other land %")
    response["landuse"] = landuse
    return response


def summarise_country_list(klass1, klass, code, qamount):
    currency = "USD"
    if qamount:
#    try:
        comparator = parseBigNumber(qamount)
        if comparator[3]=="a":
            currency = comparator[2]
    cdict  = summarise_country(klass, code, qamount, currency=currency)
    country = resolve_country_code(code)
    ask = None
    response = []
    if qamount:
#    try:
#        comparator = parseBigNumber(qamount)
        unit = comparator[2]
        compnq = klass1(title = "You asked about", magnitude=comparator[0], multiple = comparator[1], unit = comparator[2], measure=comparator[3])
        factpacks = []
        if compnq.measure == "a":
            fact = cdict["basics"]["Population"]
            factpacks.append((fact, '{times:,.2f} '+currency+' for every person in '+fact.title.replace("Population of ",""),'{times:,.2f} '+currency+' for every person in '+fact.title.replace("Population of ",""),'1 '+currency+'  for every {fraction:,.0f} people in '+fact.title.replace("Population of ","")))
            fact = cdict["basics"]["GDP"]
            factpacks.append((fact, '{times:,.2f} times the '+fact.title,'{percent:,.2f} % of the '+fact.title,'{percent:,.2f} % of the '+fact.title))
            fact = cdict["tax_spend"]["spend"]
            factpacks.append((fact, '{times:,.2f} times '+fact.title,'{percent:,.2f} % of '+fact.title,'{percent:,.2f} % of '+fact.title))
        elif compnq.measure == "c":
            fact = cdict["basics"]["Population"]
            factpacks.append((fact, '{times:,.2f} for every person in the '+fact.title,'{percent:,.2f} percent of the '+fact.title,'1 '+unit+' for every {fraction:,.0f} people in the '+fact.title))
            fact = cdict["basics"]["Land"]
            factpacks.append((fact, '{times:,.2f} for every km^2 of the '+fact.title,'{percent:,.2f} percent of the '+fact.title,'1 '+unit+' for every {fraction:,.0f} km^2 in the '+fact.title))
            fact = cdict["basics"]["GDP"]
            factpacks.append((fact, '{times:,.2f} times the '+fact.title,'{percent:,.2f} percent of the '+fact.title,'1 '+unit+' for every {fraction:,.0f} '+currency+' in the '+fact.title))
        elif compnq.measure == "e":
            fact = cdict["basics"]["Population"]
            factpacks.append((fact, '{times:,.2f} m for every person in the '+fact.title,'{times:,.2f} for every person in the '+fact.title,'1  for every {fraction:,.0f} people in the '+fact.title))
        else:
            fact = cdict["basics"]["Population"]
            factpacks.append((fact, '{times:,.2f} '+unit+' for every person in the '+fact.title,'{percent:,.2f} for every 100 people of the '+fact.title,'1 '+unit+' for every {fraction:,.0f} people in the '+fact.title))
            fact = cdict["basics"]["Land"]
            factpacks.append((fact, '{times:,.2f} '+unit+' for every km^2 of the '+fact.title,'{percent:,.2f} percent of the '+fact.title,'1 '+unit+' for every {fraction:,.0f} km^2 in the '+fact.title))
            fact = cdict["basics"]["GDP"]
            factpacks.append((fact, '{times:,.2f}  '+unit+' for every $ of '+fact.title,'{percent:,.2f} percent of the '+fact.title,'1 '+unit+' for every {fraction:,.0f} '+currency+' in the '+fact.title))

        comparisons = compnq.getDynamicComparisons(factpacks, year="2016")

        #print(compnf.render_folk, compnf.scale)
        #comparator.title = "You asked about"
        if compnq.unit.lower() == "usd":
            ask = ["Is That A Big Number?", compnq, None, comparisons]
        else:
            if compnq.unit.upper() in AMOUNT_UNITS:
                conversions = compnq.getConversions( ["USD"], year="2016")
                ask = ["Is That A Big Number?", compnq, conversions[0], comparisons]
            else:
                ask = ["Is That A Big Number?", compnq, None, comparisons]
        #response+=[ask]
 #   except:
  #      pass
    context = get_country_stats(klass, code)
    basics = [country,
        {"base":{"stat":("basics","Population"),"datum":cdict["basics"]["Population"],"context":context["basics"]["Population"]}},
        {
            "base":{"stat":("basics","Land"),"datum":cdict["basics"]["Land"],"context":context["basics"]["Land"]},
            "derived":[{"stat":("basics","Population density"),"datum":cdict["basics"]["Population density"],"context":context["basics"]["Population density"]}]
        },
        {
            "base":{"stat":("basics","GDP"),"datum":cdict["basics"]["GDP"], "context":context["basics"]["GDP"]},
            "derived":[{"stat":("basics","GDP per capita"),"datum":cdict["basics"]["GDP per capita"], "context":context["basics"]["GDP per capita"]}]
        },
    ]
    tax_spend=["Taxation and Government Expenditure",
        { 
            "base": {"stat":("tax_spend","tax"),"datum":cdict["tax_spend"]["tax"], "context":context["tax_spend"]["tax"]},
            "derived": [{"stat":("tax_spend","tax/capita"),"datum":cdict["tax_spend"]["tax/capita"], "context":context["tax_spend"]["tax/capita"]},
                           {"stat":("tax_spend","tax/GDP"),"datum":cdict["tax_spend"]["tax/GDP"], "context":context["tax_spend"]["tax/GDP"]}]
        },
        { 
            "base": {"stat":("tax_spend","spend"),"datum":cdict["tax_spend"]["spend"], "context":context["tax_spend"]["spend"]},
            "derived": [{"stat":("tax_spend","spend/capita"),"datum":cdict["tax_spend"]["spend/capita"], "context":context["tax_spend"]["spend/capita"]},
                            {"stat":("tax_spend","spend/GDP"),"datum":cdict["tax_spend"]["spend/GDP"], "context":context["tax_spend"]["spend/GDP"]}],
        },
        { 
            "base": {"stat":("tax_spend","deficit"),"datum":cdict["tax_spend"]["deficit"], "context":context["tax_spend"]["deficit"]},
            "derived": [{"stat":("tax_spend","deficit/capita"),"datum":cdict["tax_spend"]["deficit/capita"], "context":context["tax_spend"]["deficit/capita"]},
                         {"stat":("tax_spend","deficit/GDP"),"datum":cdict["tax_spend"]["deficit/GDP"], "context":context["tax_spend"]["deficit/GDP"]}],
        },
    ]
    try:
        debt = ["National Debt",
            { 
                "base": {"stat":("nat_debt","nat_debt"),"datum":cdict["nat_debt"]["nat_debt"], "context":context["nat_debt"]["nat_debt"]},
                "derived":[{"stat":("nat_debt","debt/capita"),"datum":cdict["nat_debt"]["debt/capita"], "context":context["nat_debt"]["debt/capita"]},
                              {"stat":("nat_debt","debt/GDP"),"datum":cdict["nat_debt"]["debt/GDP"], "context":context["nat_debt"]["debt/GDP"]}]
            }
        ]
    except:
        debt = ["National Debt", "No information available"]
    uses = ["Where GDP goes"]
    try:
        uses += [{ 
                "base": {"stat":("uses","hhcons"),"datum":cdict["uses"]["hhcons"], "context":context["uses"]["hhcons"]},
                "derived": [{"stat":("uses","hhcons/capita"),"datum":cdict["uses"]["hhcons/capita"], "context":context["uses"]["hhcons/capita"]},
                               {"stat":("uses","hhcons/GDP"),"datum":cdict["uses"]["hhcons/GDP"], "context":context["uses"]["hhcons/GDP"]}]
        }]
        uses += [{ 
                "base": {"stat":("uses","gvcons"),"datum":cdict["uses"]["gvcons"], "context":context["uses"]["gvcons"]},
                "derived": [{"stat":("uses","gvcons/capita"),"datum":cdict["uses"]["gvcons/capita"], "context":context["uses"]["gvcons/capita"]},
                                {"stat":("uses","gvcons/GDP"),"datum":cdict["uses"]["gvcons/GDP"], "context":context["uses"]["gvcons/GDP"]}]
        }]
        uses += [{ 
                "base": {"stat":("uses","hhinv"),"datum":cdict["uses"]["inv"], "context":context["uses"]["inv"]},
                "derived":[{"stat":("uses","inv/capita"),"datum":cdict["uses"]["inv/capita"], "context":context["uses"]["inv/capita"]},
                              {"stat":("uses","inv/GDP"),"datum":cdict["uses"]["inv/GDP"], "context":context["uses"]["inv/GDP"]}]
        }]
        uses += [{ 
                "base": {"stat":("uses","exports"),"datum":cdict["uses"]["exports"], "context":context["uses"]["exports"]},
                "derived":[{"stat":("uses","exports/capita"),"datum":cdict["uses"]["exports/capita"], "context":context["uses"]["exports/capita"]},
                              {"stat":("uses","exports/GDP"),"datum":cdict["uses"]["exports/GDP"], "context":context["uses"]["exports/GDP"]}]
        }]
        uses += [{ 
                "base": {"stat":("uses","imports"),"datum":cdict["uses"]["imports"], "context":context["uses"]["imports"]},
                "derived":[{"stat":("uses","imports/capita"),"datum":cdict["uses"]["imports/capita"], "context":context["uses"]["imports/capita"]},
                              {"stat":("uses","imports/GDP"),"datum":cdict["uses"]["imports/GDP"], "context":context["uses"]["imports/GDP"]}]
        }]
    except:
        pass
    sources = ["Where GDP comes from"]
    try:
        sources += [{ 
                "base": {"stat":("sources","agriculture"),"datum":cdict["sources"]["agriculture"], "context":context["sources"]["agriculture"]},
                "derived": [{"stat":("sources","agri/capita"),"datum":cdict["sources"]["agri/capita"], "context":context["sources"]["agri/capita"]},
                                {"stat":("sources","agri/GDP"),"datum":cdict["sources"]["agri/GDP"], "context":context["sources"]["agri/GDP"]}]
        }]
        sources += [{ 
                "base": {"stat":("sources","industry"),"datum":cdict["sources"]["industry"], "context":context["sources"]["industry"]},
                "derived": [{"stat":("sources","industry/capita"),"datum":cdict["sources"]["industry/capita"], "context":context["sources"]["industry/capita"]},
                                {"stat":("sources","industry/GDP"),"datum":cdict["sources"]["industry/GDP"], "context":context["sources"]["industry/GDP"]}]
        }]
        sources += [{ 
                "base": {"stat":("sources","services"),"datum":cdict["sources"]["services"], "context":context["sources"]["services"]},
                "derived": [{"stat":("sources","services/capita"),"datum":cdict["sources"]["services/capita"], "context":context["sources"]["services/capita"]},
                               {"stat":("sources","services/GDP"),"datum":cdict["sources"]["services/GDP"], "context":context["sources"]["services/GDP"]}]
        }]
    except:
        pass
    landuse = ["How land is used"]
    try:
        landuse += [{ 
                "base": {"stat":("landuse","agriland"),"datum":cdict["landuse"]["agriland"], "context":context["landuse"]["agriland"]},
                "derived": [{"stat":("landuse","agriland/land"),"datum":cdict["landuse"]["agriland/land"], "context":context["landuse"]["agriland/land"]}]
        }]
        landuse += [{ 
                "base": {"stat":("landuse","forest"),"datum":cdict["landuse"]["forest"], "context":context["landuse"]["forest"]},
                "derived": [{"stat":("landuse","forest/land"),"datum":cdict["landuse"]["forest/land"], "context":context["landuse"]["forest/land"]}]
        }]
        landuse += [{ 
                "base": {"stat":("landuse","other"),"datum":cdict["landuse"]["other"], "context":context["landuse"]["other"]},
                "derived": [{"stat":("landuse","other/land"),"datum":cdict["landuse"]["other/land"], "context":context["landuse"]["other/land"]}]
        }]
    except:
        pass
    response+=[basics]
    response += [sources]
    response += [uses]
    response+=[tax_spend]
    response += [debt]
    response += [landuse]

    return ask, response


def get_country_stats(klass, key):
    global country_stats
    if country_stats==None:
        country_stats = make_country_stats(klass)
    try:
    #if 1:
        return get_all_stats_for(country_stats, key)
    except:
        return "unknown country code "+key


def make_country_stats(klass):
    codes = sorted(get_country_codes()[0].keys(), key = lambda k: k)
    stats = {}
    for code in [code for code in codes if code!="World"]:
        try:
                sum = summarise_country(klass, code, None, currency="USD")
                for key in sum.keys():
                    if key!="country":
                        try:
                            stats[key]
                        except KeyError:
                            stats[key]={}
                        for subkey in sum[key].keys():
                            try:
                                stats[key][subkey]
                            except KeyError:
                                stats[key][subkey]={}
                            try:
                                stats[key][subkey]["items"]
                            except KeyError:
                                stats[key][subkey]["items"]={}
                            stats[key][subkey]["items"][code]=sum[key][subkey]
        except:
            print("problem with", code)



    for key in stats.keys():
        for subkey in stats[key].keys():
            statset = stats[key][subkey]
            n = len(statset["items"])
            sortedstats = sorted(statset["items"], key = lambda k: statset["items"][k].value*10**statset["items"][k].scale)
            statset["sortindex"]=sortedstats
            inverse = {}
            percentile = {}
            n = len(sortedstats)
            for i in range(n):
                inverse[sortedstats[i]]=i
                percentile[sortedstats[i]]=round(100*i/n)
            statset["inverse"]=inverse
            statset["percentile"]=percentile
            n = len(statset["items"])
            q0 = round(n*0)
            q25 = round(n*0.25)
            q50 = round(n*0.5)
            q75 = round(n*0.75)
            q100 = n-1
            quantiles=[
                (sortedstats[q0],statset["items"][sortedstats[q0]]),
                (sortedstats[q25],statset["items"][sortedstats[q25]]),
                (sortedstats[q50],statset["items"][sortedstats[q50]]),
                (sortedstats[q75],statset["items"][sortedstats[q75]]),
                (sortedstats[q100],statset["items"][sortedstats[q100]])]
            statset["quantiles"]= quantiles

    return stats

def get_stats_for(statset, countrycode):
    quantiles = statset["quantiles"]
    quartiles = list(map(lambda q:[resolve_country_code(q[0]),q[1].render_folk], quantiles))
    dataquantile = statset["percentile"][countrycode] 
    highlights = list(map(lambda code:statset["percentile"][code],["US", "RU", "CN"]))
    return quartiles, dataquantile, highlights

def get_all_stats_for(stats, countrycode):
    costats={}
    for key in stats.keys():
        costats[key]={}
        for subkey in stats[key].keys():
            statset = stats[key][subkey]
            costats[key][subkey]=get_stats_for(statset, countrycode)
    return costats

def get_stat(klass, compkey):
    global country_stats
    if country_stats==None:
        country_stats = make_country_stats(klass)
    key, subkey = compkey.split(".")
    fullstat =  country_stats[key][subkey]
    return list(map(lambda k:(k, fullstat["items"][k]), fullstat["sortindex"]))
