import sys
import json
#sys.path.append("../scripts")
from .PyHttpCall import callHttpGET

def getUSDConversionFactor(currency):
    response = callHttpGET("http://api.fixer.io/","latest",{"symbols":currency,"base":"USD","callback":"?"}).text
    jsonResponse = json.loads(response[1:-1])
    return jsonResponse["rates"][currency]

def convertToUSD(amount, currency):    
    if (currency=="USD"):
        return amount
    else:
        factor = getUSDConversionFactor(currency)
        return round(amount / factor,2)

def getCurrencyConversionFactor(currency1, currency2):
    response = callHttpGET("http://api.fixer.io/","latest",{"symbols":currency1,"base":currency2,"callback":"?"}).text
    jsonResponse = json.loads(response[1:-1])
    return jsonResponse["rates"][currency1]

def convertToCurrency(amount, currency1, currency2):    
    if (currency1==currency2):
        return amount
    else:
        factor = getCurrencyConversionFactor(currency1, currency2)
        return round(amount / factor,2)

def test():
    factor = getUSDConversionFactor("GBP")
    converted = convertToUSD(70, "GBP")
    print(converted)
