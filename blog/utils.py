from random import sample,seed,randint,choice
from pint import UnitRegistry,UndefinedUnitError
ureg = UnitRegistry()
Q_=ureg.Quantity

from math import log10
import re

def sigfigs(x,n):
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
    if x/1000000000 ==int(x/1000000000):
        return  "{:,.0f} billion".format(x/1000000000)    
    elif x/1000000 ==int(x/1000000):
        return  "{:,.0f} million".format(x/1000000)    
    elif x/1000 ==int(x/1000):
        return  "{:,.0f} thousand".format(x/1000)    
    elif x==int(x):
        return  "{:,.0f}".format(x)    
    else:
        return "{:,.2f}".format(x)


def num(s):
    return float(s)

def getMultiple(scale):
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
}

std_multiples = {
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
    mults={"U":"k", "k":"M", "M":"G", "G":"T", "T":"P", "P":"E",
        "E":"Z", "Z":"Y", "Y":"10^27", "10^27":"10^30", "10^30":"10^33", "10^33":"10^36", "10^36":"10^39", "10^39":"10^42"}
    if multiple in mults:
        return mults[multiple]
    else:        
        return None

def prec(multiple):
    mults={"U":"k", "k":"M", "M":"G", "G":"T", "T":"P", "P":"E",
        "E":"Z", "Z":"Y", "Y":"10^27", "10^27":"10^30", "10^30":"10^33", "10^33":"10^36", "10^36":"10^39", "10^39":"10^42"}
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

    value = num(magnitude)
    while value>1000:
        value=value/1000
        value = sigfigs(value,6)
        multiple = succ(multiple)

    magnitude = str(value)
    return magnitude, multiple, unit, measure 

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

def bracketNumber(klass, magnitude, scale, measure):
    #tolerance=10000
    response = []
#   nf_gt = NumberFact.objects.filter(value__gt=num(magnitude)*1, value__lt=num(magnitude)*1*(1+tolerance), scale=scale-0, measure=measure).order_by("value")
    nf_gt = klass.objects.filter(value__gt=num(magnitude)*1, scale=scale-0, measure=measure).order_by("value")
    if len(nf_gt)==0:
        nf_gt = klass.objects.filter(value__gt=num(magnitude)/1000, scale=scale+3, measure=measure).order_by("value")
    if len(nf_gt)==0:
        nf_gt = klass.objects.filter(value__gt=num(magnitude)/1000000, scale=scale+6, measure=measure).order_by("value")
    if len(nf_gt)==0:
        nf_gt = klass.objects.filter(value__gt=num(magnitude)/1000000000, scale=scale+9, measure=measure).order_by("value")

    nf_lt = klass.objects.filter(value__lt=num(magnitude)*1, scale=scale-0, measure=measure).order_by("-value")
    if len(nf_lt)==0:
        nf_lt = klass.objects.filter(value__lt=num(magnitude)*1000, scale=scale-3, measure=measure).order_by("-value")
    if len(nf_lt)==0:
        nf_lt = klass.objects.filter(value__lt=num(magnitude)*1000000, scale=scale-6, measure=measure).order_by("-value")
    if len(nf_lt)==0:
        nf_lt = klass.objects.filter(value__lt=num(magnitude)*1000000000, scale=scale-9, measure=measure).order_by("-value")
    if len(nf_gt)==0:
        response.append("No useful upper bracket on file")
    else:           
        response.append(" ".join([nf_gt[0].render_folk_long]))
    if len(nf_lt)==0:
        response.append("No useful lower bracket on file")
    else:           
        response.append(" ".join([nf_lt[0].render_folk_long]))
    return response


def closeEnoughNumberFact(klass, magnitude, scale, tolerance, measure):
#   nf = NumberFact.objects.filter(magnitude__gt=800, scale=scale)
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

def closeMagnitudeNumberFact(klass, magnitude, measure, tolerance, multiple):
#   nf = NumberFact.objects.filter(magnitude__gt=800, scale=scale)
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
    nf = klass.objects.filter(value__gte=mag/(1+tolerance), value__lt=mag*(1+tolerance), measure=measure)
    for fact in nf:
        facts.append(fact)
    nf = klass.objects.filter(value__gte=mag*10/(1+tolerance), value__lt=mag*10*(1+tolerance), measure=measure)
    for fact in nf:
        facts.append(fact)
    nf = klass.objects.filter(value__gte=mag*100/(1+tolerance), value__lt=mag*100*(1+tolerance), measure=measure)
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
        ce.remove(nf)
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
    count = klass.objects.filter(measure=measure).count()
    rf = klass.objects.filter(measure=measure)[randint(0,count-1)]
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




def spuriousFact(klass):
    facts = []
    measure=choice(["extent","extent","amount","count","duration","mass","mass"])
    tolerance = 0.01
    while len(facts)==0:
        seed = randint(0,1000000)
        rf = randomFact(klass, measure, rseed=seed)
        facts = closeMagnitudeNumberFact(klass, rf.magnitude, rf.measure, tolerance, 1)
        try:
            facts.remove(rf)
        except:
            pass
        facts2 = closeMagnitudeNumberFact(klass, rf.magnitude, rf.measure,tolerance, 2)
        facts+=facts2
#        facts2b = closeMagnitudeNumberFact(klass, rf.magnitude, rf.measure,tolerance, 0.5)
#        facts+=facts2b
        facts4 = closeMagnitudeNumberFact(klass, rf.magnitude, rf.measure,tolerance, 4)
        facts+=facts4
        facts4b = closeMagnitudeNumberFact(klass, rf.magnitude, rf.measure,tolerance, 0.25)
        facts+=facts4b
        facts5 = closeMagnitudeNumberFact(klass, rf.magnitude, rf.measure,tolerance, 5)
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
    return {"fact1":fact1.render_folk, "comparison":comparison, "fact2":fact2.render_folk}



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
        print(count)
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



def neatFacts(klass, selectedFact):
    rf = selectedFact
    tolerance = 0.01
    maxRatio = {"extent":10000, "mass":20000, "duration":10000, "count":500, "amount":500}[rf.measure]

    facts = closeMagnitudeNumberFact(klass, rf.magnitude, rf.measure, tolerance, 1)
    try:
        facts.remove(rf)
    except:
        pass
    facts2 = closeMagnitudeNumberFact(klass, rf.magnitude, rf.measure,tolerance, 2)
    facts+=facts2
#    facts2b = closeMagnitudeNumberFact(klass, rf.magnitude, rf.measure,tolerance, 0.5)
#    facts+=facts2b
    facts4 = closeMagnitudeNumberFact(klass, rf.magnitude, rf.measure,tolerance, 4)
    facts+=facts4
    facts4b = closeMagnitudeNumberFact(klass, rf.magnitude, rf.measure,tolerance, 0.25)
    facts+=facts4b
    facts5 = closeMagnitudeNumberFact(klass, rf.magnitude, rf.measure,tolerance, 5)
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
