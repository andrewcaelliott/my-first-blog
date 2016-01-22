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



def convertToDefaultBase(magnitude, unit):
    if unit in AMOUNT_UNITS: 
        n = convertToUSD(magnitude, unit)
        u = 'USD'
    else:
        try:
            quantity = Q_(" ".join([str(magnitude), unit]))
            if quantity.dimensionality==ureg.s.dimensionality:
                n = quantity.to(ureg.year).magnitude
                u = quantity.to(ureg.year).units
            elif quantity.dimensionality==ureg.g.dimensionality:
                n = quantity.to(ureg.kg).magnitude
                u = quantity.to(ureg.kg).units
            else:
                n = quantity.to_base_units().magnitude
                u = quantity.to_base_units().units
        except UndefinedUnitError as e:
            n = magnitude
            u = 'unknown'
    return n, u

def convertToDefault(magnitude, unit):
    return convertToDefaultBase(magnitude, unit)[0]
