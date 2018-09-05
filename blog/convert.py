from math import log10
from .fixer_io import convertToUSD
from .fixer_io import convertToCurrency
from pint import UnitRegistry,UndefinedUnitError
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

def convertToUnit(magnitude, unit, target_unit):
    if unit in AMOUNT_UNITS: 
        n = convertToCurrency(magnitude, unit, target_unit)
        u = target_unit
    else:
        try:
            quantity = Q_(" ".join([str(magnitude), unit]))
            q2 = quantity.to(ureg(target_unit)) 
            n = q2.magnitude
            u = q2.units
        except UndefinedUnitError as e:
            n = magnitude
            u = 'unknown'
    return n, u



def convertToDefaultBase(magnitude, unit, year=None):
    if unit in AMOUNT_UNITS: 
        if isinstance(magnitude, str):
            magnitude = float(magnitude)
        n = convertToUSD(magnitude, unit, year=year)
        u = 'USD'
    else:
        try:
            quantity = Q_(" ".join([str(magnitude), unit]))
            print("Converting:",magnitude, unit,"==>",quantity)
            if quantity.dimensionality==ureg.s.dimensionality:
                n = quantity.to(ureg.year).magnitude
                u = quantity.to(ureg.year).units
            elif quantity.dimensionality==ureg.g.dimensionality:
                n = quantity.to(ureg.kg).magnitude
                u = quantity.to(ureg.kg).units
            elif quantity.dimensionality==ureg.J.dimensionality:
                n = quantity.to(ureg.J).magnitude
                u = quantity.to(ureg.J).units
            elif quantity.dimensionality==ureg.L.dimensionality:
                n = quantity.to(ureg.L).magnitude
                u = quantity.to(ureg.L).units
            else:
                n = quantity.to_base_units().magnitude
                u = quantity.to_base_units().units
            print(n,u)
        except UndefinedUnitError as e:
            n = magnitude
            u = 'unknown'
    return n, u

def convertToDefault(magnitude, unit, year=None):
    return convertToDefaultBase(magnitude, unit, year=year)[0]
