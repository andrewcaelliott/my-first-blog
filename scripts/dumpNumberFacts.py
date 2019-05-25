import sys
import json
import os
sys.path.append("../scripts")

from blog.models import NumberFact
from mysite.settings import BASE_DIR


def run():

	allfacts = NumberFact.objects.all()

	outfile = os.path.join(BASE_DIR, "explain", "dumpfacts2.csv")
	print(outfile)
	file = open(outfile, "w")
	for fact in allfacts:
		print(fact.magnitude, fact.scale, fact.unit, fact.measure, fact.title)
		file.write(",".join([str(fact.magnitude), str(fact.scale), str(fact.unit), str(fact.measure), fact.title])+"\n")
	file.close()