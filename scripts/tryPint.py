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