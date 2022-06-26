from .PyHttpCall import callHttpPOST
import json
from blog.utils import (bracketNumber, getMultiple)
from blog.models import NumberFact


def rnd_mult_seq(measure, unit, base_mag, base_scale, factor, n):
	mag= base_mag
	scl = base_scale
	nfs= []
	for i in range (0,n):
		magnitude = str(mag)
		scale = scl
		nf = NumberFact(magnitude = str(mag), multiple = getMultiple(scale), scale=scale, unit = unit, measure = measure)
		nfs.append(nf)
		mag = mag * factor
		if mag > 1000:
			mag = base_mag
			scl = scl + 3
	return nfs

def rnd_money_seq(measure, unit, base_mag, base_scale, factor, n):
	mag= base_mag
	scl = base_scale
	money_seq = {1:2, 2:5, 5:10, 10:20, 20:50, 50:100, 100:200, 200:500, 500:1000}
	nfs= []
	for i in range (0,n):
		magnitude = str(mag)
		scale = scl
		nf = NumberFact(magnitude = str(mag), multiple = getMultiple(scale), scale=scale, unit = unit, measure = measure)
		nfs.append(nf)
		mag = money_seq[mag]
		if mag >= 1000:
			mag = 1
			scl = scl + 3
	return nfs


def run():
	print("ok")
	measure = "extent.hor"
	unit = "m"
	seq = rnd_money_seq(measure, unit, 1, 3, 2, 12)
#	seq = rnd_mult_seq(measure, unit, 4, 0, 10, 15)

	brackets = []
	for nf in seq:
		high, low = bracketNumber(NumberFact, nf.magnitude, nf.scale, nf.measure)
		brackets.append({"num":nf.render_folk[2:-1], "low":low, "high": high})

#	for bracket in brackets:
#		print (bracket)

	#return

	uri = "http://acae.echopublish.com/"
	service = "merge/"
	payload = {"measure":measure, "brackets": brackets, "desc":"masses starting with 10mm", "factor":"2, 5, 10 and repeating"}
	data = {
		"flow": "docx.flo",
		#"data_root": "docroot",
		"template": "ITABN_powers",
		"payload_type":"json",
		"identifier":"extents_1m_xmoney",
		"payload":json.dumps(payload),

	}
	pld = json.dumps(payload, indent=True)
	for bracket in json.loads(pld)["brackets"]:
		print(bracket["num"])
		print(bracket["low"], bracket["high"])
	#response = callHttpPOST(uri, service, data, contentType="text/json", username="PrimeUser:EchoPrime", trace=0)
	#print(json.loads(response.text))	