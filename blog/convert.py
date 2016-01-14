from pint import UnitRegistry,UndefinedUnitError
from math import log10
from .fixer_io import convertToUSD
ureg = UnitRegistry()
Q_=ureg.Quantity

            

AMOUNT_UNITS= (
	    'USD',
            'AUD',
            'CAD',
            'CHF',
            'EUR',
            'GBP',
            'HKD',
            'JPY',
            )

def convertToDefault(magnitude, unit):
    if unit in AMOUNT_UNITS: 
        n = convertToUSD(magnitude, unit)
    else:
        try:
            quantity = Q_(" ".join([str(magnitude), unit]))
            if quantity.dimensionality==ureg.s.dimensionality:
                n = quantity.to(ureg.year).magnitude
            else:
                n = quantity.to_base_units().magnitude
        except UndefinedUnitError as e:
            n = magnitude
    return n
