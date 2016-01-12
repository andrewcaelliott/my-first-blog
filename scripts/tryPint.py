from pint import UnitRegistry
ureg = UnitRegistry()

def run():
	for item in ureg.__dict__:
		print(item)
#	print(ureg.__doc__)
	q = 5.0 * ureg.furlong / ureg.fortnight
	print(q.to(ureg.meter / ureg.second).magnitude)	
	print(q.to(ureg.meter / ureg.second).units)
	print(q.to(ureg.meter / ureg.second).dimensionality)
	q2 = 23 * ureg.year
	print(q2)
	print(q2.dimensionality)	
	print(q2.dimensionality==ureg.s.dimensionality)
	print(q2.to(ureg.s))