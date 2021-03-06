import os
import json
from blog.models import NumberFact
#from blog.models import NumberQuery
#from blog.forms import QueryForm
#from pint import UnitRegistry
from math import log10
from random import sample,randint,choice
from blog.views import quiz_from_seed
from blog.utils import (closeEnoughNumberFact, closeMagnitudeNumberFact, 
	numberFactsLikeThis, biggestNumberFact,parseBigNumber, num, 
	bracketNumber, randomFact, randomFactAny, sigfigs, renderInt, 
	spuriousFact, neatFacts, resolve_country_code, resolve_cia_country, 
	get_country_codes, summarise_country, summarise_country_list, get_country_stats,
	make_country_stats, get_stat, make_number)
from blog.chance_utils import format_round_sigfigs
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

def run7():
	measure=("area")
	seed = randint(0,1000000)
	rf = randomFact(NumberFact, measure, rseed=seed)
	print(rf.render)

	bestComparisons, tolerance, score  = numberFactsLikeThis(NumberFact, rf, rseed=seed) 

	print(tolerance, score)
	for fact in bestComparisons:
		print(fact.render_folk)
		print(fact.magnitude)
		print(fact.scale)
		print(fact.permlink)

	biggest = biggestNumberFact(bestComparisons)
	print(">>>", biggest.render)

def run8():
	measure=("count")
	seed = randint(0,1000000)
	rf = randomFact(NumberFact, measure, rseed=seed)
	magnitude = rf.magnitude
	scale = rf.scale
#	print(rf.render)
#	test = NumberFact.objects.filter().order_by("value")[0:10]#
#	for item in test:
#		print(item.render, item.magnitude, item.value)

#	print(bracketNumber(NumberFact, "481", 3, "extent"))
#	for i in range(-3,24,3):
#		print(i, bracketNumber(NumberFact, "1.25", i, measure))
#		print(i+1,bracketNumber(NumberFact, "12.5", i, measure))
#		print(i+2,bracketNumber(NumberFact, "125", i, measure))

#	for i in range(-3,24,3):
#		print(i, bracketNumber(NumberFact, "1.0", i, measure))
#		print(i+1,bracketNumber(NumberFact, "10.0", i, measure))
#		print(i+2,bracketNumber(NumberFact, "100.0", i, measure))

#	for i in range(-3,18,3):
	for i in range(3,6,3):
		print(i, bracketNumber(NumberFact, "1.0", i, measure))
		print(i,bracketNumber(NumberFact, "2.0", i, measure))
		print(i,bracketNumber(NumberFact, "4.0", i, measure))
		print(i,bracketNumber(NumberFact, "8.0", i, measure))
		print(i,bracketNumber(NumberFact, "16.0", i, measure))
		print(i,bracketNumber(NumberFact, "32.0", i, measure))
		print(i,bracketNumber(NumberFact, "64.0", i, measure))
		print(i,bracketNumber(NumberFact, "125.0", i, measure))
		print(i,bracketNumber(NumberFact, "250.0", i, measure))
		print(i,bracketNumber(NumberFact, "500.0", i, measure))

	print(1, bracketNumber(NumberFact, "100", 18, measure))

def run9():
	measure=("mass")
	seed = randint(0,1000000)
	rf = randomFact(NumberFact, measure, rseed=seed)
	print(rf)
	print(rf.measure)

def run10():
	klass = NumberFact
	print(NumberFact)
	print(klass)
	print(klass.objects)


def run11():
	klass = NumberFact
#	measure=("extent")#
#	seed = randint(0,1000000)
#	rf = randomFact(NumberFact, measure, rseed=seed)
#	print(rf.permlink)
#	dyk = spuriousFact(klass, 2, measure="amount!")
	dyk = spuriousFact(klass, 2)
	print(dyk)
	print(dyk["fact1"], dyk["comparison"], dyk["fact2"])

def run11a():
	print(sigfigs(102,2))
	print(sigfigs(253,2))
	print(sigfigs(332,2))
	print(sigfigs(102,3))
	print(sigfigs(253,3))
	print(sigfigs(332,3))


def run12():
	klass = NumberFact
	measure=("extent")
	seed = randint(0,1000000)
	rf = randomFact(NumberFact, measure, rseed=seed)
	print(rf.render)
	print(rf.measure)
	facts = neatFacts(klass, rf)
	for fact in facts:
#		print(fact["comparison"], fact["fact2"].render2)
#		print(fact["fact2"].measure)
		print(fact["fact1"].render0, fact["comparison"], fact["fact2"].render2)
		print(fact["fact2"].render2, fact["inversecomparison"], fact["fact1"].render0)

def run13():
	klass = NumberFact
	measure=("extent")
	seed = randint(0,1000000)
	rf = randomFact(NumberFact, measure, rseed=seed)
	print(rf.render_folk)

def run14():
	target = "olympic"
	nf = NumberFact.objects.filter(title__icontains=target)
	for f in nf:
		print(f)

def run15():
	target = "World"
	date = "2015"
	nf = NumberFact.objects.filter(date__year=date, location__icontains=target)
	for f in nf:
		print(f.render_folk)

def run16():
	code = "GB"
	print(resolve_country_code(code))
	code = "EH"
	print(resolve_country_code(code))
	name = "Algeria"
	print(resolve_cia_country(name))
	name = "Congo Democratic Republic of the"
	print(resolve_cia_country(name))

def val_from(fact):
	return float(fact.magnitude)*10**fact.scale

def sum_country(code):
	location = code
	print(resolve_country_code(location))
	facts = NumberFact.objects.filter(location__icontains = location).order_by('title')  
	#for fact in facts:
	#	print(fact.render_folk)
	spend = NumberFact.objects.filter(location__icontains = location, title__icontains = "Govt spending").order_by('-date')[0]  
	tax = NumberFact.objects.filter(location__icontains = location, title__icontains = "Total taxation").order_by('-date')[0]  
	GDP = NumberFact.objects.filter(location__icontains = location, title__icontains = "GDP in").order_by('-date')[0]  
	pop = NumberFact.objects.filter(location__icontains = location, title__icontains = "Population of").order_by('-date')[0]  
	land = NumberFact.objects.filter(location__icontains = location, title__icontains = "Land Area of").order_by('-date')[0]  
	try:
		debt = NumberFact.objects.filter(location__icontains = location, title__icontains = "National Debt").order_by('-date')[0]  
	except:
		debt = None
	try:
		hhcons = NumberFact.objects.filter(location__icontains = location, title__icontains = "Household Consumption").order_by('-date')[0]  
	except:
		hhcons = None
	try:
		gvcons = NumberFact.objects.filter(location__icontains = location, title__icontains = "Government Consumption").order_by('-date')[0]  
	except:
		gvcons = None
	try:
		invcap = NumberFact.objects.filter(location__icontains = location, title__icontains = "Investment in Capital").order_by('-date')[0]  
	except:
		invcap = None
	try:
		invinv = NumberFact.objects.filter(location__icontains = location, title__icontains = "Investment in Inventories").order_by('-date')[0]  
	except:
		invinv = None
	try:
		exports = NumberFact.objects.filter(location__icontains = location, title__icontains = "Exports").order_by('-date')[0]  
	except:
		exports = None
	try:
		imports = NumberFact.objects.filter(location__icontains = location, title__icontains = "Imports").order_by('-date')[0]  
	except:
		imports = None

	agri = NumberFact.objects.filter(location__icontains = location, title__icontains = "Agriculture").order_by('-date')[0]  
	industry = NumberFact.objects.filter(location__icontains = location, title__icontains = "Industrial").order_by('-date')[0]  
	services = NumberFact.objects.filter(location__icontains = location, title__icontains = "Services").order_by('-date')[0]  
	print ("Services>",services.render_folk)
	#print(spend.render_folk, tax.render_folk, GDP.render_folk, pop.render_folk)
	print(GDP.render_folk)
	print(pop.render_folk)
	print("GDP/capita", round(val_from(GDP)/val_from(pop),0))
	resp = round(val_from(GDP)/val_from(pop),2)
	print()
	print(land.render_folk)
	print("pop/land", round(val_from(pop)/val_from(land),0))
	print()
	print(tax.render_folk)
	print("tax/capita", round(val_from(tax)/val_from(pop),0))
	print("tax/GDP", round(100*val_from(tax)/val_from(GDP),0))
	print()
	print(spend.render_folk)
	print("spend/capita", round(val_from(spend)/val_from(pop),0))
	print("spend/GDP", round(100*val_from(spend)/val_from(GDP),0))
	print()
	deficit = val_from(spend) - val_from(tax)
	print("deficit", round(deficit,0)/1000000, "million")
	print("deficit/capita", round(deficit/val_from(pop),0))
	print("deficit/GDP", round(100*deficit/val_from(GDP),0))
	print("deficit/spend", round(100*deficit/val_from(spend),0))
	print()
	if debt:
		print(debt.render_folk)
		print("debt/capita", round(val_from(debt)/val_from(pop),0))
		print("debt/GDP", round(100*val_from(debt)/val_from(GDP),0))
		print()
	if hhcons:
		print(hhcons.render_folk)
		print("hhcons/capita", round(val_from(hhcons)/val_from(pop),0))
		print("hhcons/GDP", round(100*val_from(hhcons)/val_from(GDP),0))
		print()
	if gvcons:
		print(gvcons.render_folk)
		print("gvcons/capita", round(val_from(gvcons)/val_from(pop),0))
		print("gvcons/GDP", round(100*val_from(gvcons)/val_from(GDP),0))
		print()
	if invcap:
		print(invcap.render_folk)
		print("invcap/capita", round(val_from(invcap)/val_from(pop),0))
		print("invcap/GDP", round(100*val_from(invcap)/val_from(GDP),0))
		print()
	if invinv:
		print(invinv.render_folk)
		print("invinv/capita", round(val_from(invinv)/val_from(pop),0))
		print("invinv/GDP", round(100*val_from(invinv)/val_from(GDP),0))
		print()
	if exports:
		print(exports.render_folk)
		print("exports/capita", round(val_from(exports)/val_from(pop),0))
		print("exports/GDP", round(100*val_from(exports)/val_from(GDP),0))
		print()
	if imports:
		print(imports.render_folk)
		print("imports/capita", round(val_from(imports)/val_from(pop),0))
		print("imports/GDP", round(100*val_from(imports)/val_from(GDP),0))
		print()
	print(agri.render_folk)
	print("agri/capita", round(val_from(agri)/val_from(pop),0))
	print("agri/GDP", round(100*val_from(agri)/val_from(GDP),0))
	print()
	print(industry.render_folk)
	print("industry/capita", round(val_from(industry)/val_from(pop),0))
	print("industry/GDP", round(100*val_from(industry)/val_from(GDP),0))
	print()
	print(services.render_folk)
	print("services/capita", round(val_from(services)/val_from(pop),0))
	print("services/GDP", round(100*val_from(services)/val_from(GDP),0))
	print()
	print()
	return resp



def runbatch():
	good= 0
	bad = 0
	badlist = []
	codes = sorted(get_country_codes()[0].keys(), key = lambda k: k)
	resp = {}
	for code in codes:
#	for code in ["CG", "KR", "CD", "CX", "IM", "WF", "SJ", "NF", "JE", "CY", "EH", "FK", "PN", "SH", "FM", "KP", "CZ", "BS", "VA", "GM"]:
	 	print (code)
	 	try:
	 		r = sum_country(code)
	 		good+=1
	 		resp[resolve_country_code(code)]=r
	 	except:
	 		print("Problem with "+code+" "+resolve_country_code(code))
	 		bad+=1
	 		badlist+=[code+" "+resolve_country_code(code)]
	print("Good",good, "Bad", bad)
	print (badlist)
	return resp


def run16():
	r = runbatch()
	for key in r.keys():
		print (key,",",r[key])
	

def run17():
	print("ok")
	resp = summarise_country(NumberFact, "JP", "100000")
	#print(resp)
	print(resp["tax_spend"])
	ts = resp["tax_spend"]
	for item in ts:
		print(ts[item].render_folk)
	#print(json.dumps(resp, indent=4))

#	nf = NumberFact(magnitude="123.4", multiple="thousand", scale=3, unit="m", measure = "extent", title = "a long way")
#	print(nf)
#	print(nf.render_folk)
	for item in resp:
		print(item)

	resp2 = summarise_country_list(NumberFact, "FR", "100000")
	print(resp2)

def make_country_stats():
	codes = sorted(get_country_codes()[0].keys(), key = lambda k: k)
	stats = {}
	for code in [code for code in codes if code!="World"]:
		try:
		        sum = summarise_country(NumberFact, code, None, currency="USD")
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
	return quartiles, dataquantile

def get_all_stats_for(stats, countrycode):
	costats={}
	for key in stats.keys():
		costats[key]={}
		for subkey in stats[key].keys():
			statset = stats[key][subkey]
			costats[key][subkey]=get_stats_for(statset, countrycode)
	return costats


def run18():
#	stats = make_country_stats()	
#	print(get_all_stats_for(stats, "ZA")["basics"])
#	print(get_all_stats_for(stats, "DE")["basics"])
#	print(get_all_stats_for(stats, "AU")["basics"])
	print(get_country_stats(NumberFact, "AU")["sources"])


#def get_stat(stats, compkey):
#	key, subkey = compkey.split(".")
#	fullstat =  stats[key][subkey]
#	return list(map(lambda k:(k, fullstat["items"][k].render_folk), fullstat["sortindex"]))

def run19():
	stats = make_country_stats()
	statlist = get_stat(NumberFact, "basics.GDP")
	statlist.reverse()
	for item in statlist:
		print(resolve_country_code(item[0]), item[1])
	
def run20():
	klass = NumberFact
	measure=("duration")
	seed = randint(0,1000000)
	rf = make_number(klass, "1723", "test", measure, "years")
	print(rf)
	print(rf.render)
	print(rf.measure)
	facts = neatFacts(klass, rf, tolerance=0.02)
	for fact in facts:
#		print(fact["comparison"], fact["fact2"].render2)
		print(fact)
		print(fact["fact2"].measure)

def run21():
	klass = NumberFact
	measure=("extent")
	seed = randint(0,1000000)
	rf = make_number(klass, "2723", "test", measure, "m")
	print(rf.render_folk)
	facts = neatFacts(klass, rf, tolerance=0.02)
	for fact in facts:
#		print(fact["comparison"], fact["fact2"].render2)
		print(fact)
		print(fact["fact2"].measure)

def run22():
	klass = NumberFact
	params = {"measure":"amount"}
	seed = randint(0,1000000)
	quiz = quiz_from_seed(seed, params)
	print(quiz["comparison"])
	for option in quiz["options"]:
		print (option.render_folk)

def run():
	p = 10
	s = format_round_sigfigs(p, level=4)
	print(s)