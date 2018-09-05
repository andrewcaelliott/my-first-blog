import sys
import json
#sys.path.append("../scripts")
from .PyHttpCall import callHttpGET

def getUSDConversionFactor(currency, year = None):
    if  year==None:
        version = "latest"
    else:
        version = year+"-12-31"
    response = callHttpGET("http://data.fixer.io/api/",version,{"access_key":"c65acaa2ab282e6eb961788d69eacc69","symbols":currency,"base":"USD","callback":"?"}).text
    open_b = response.find("{")
    close_b = response.rfind("}")
    jsonResponse = json.loads(response[open_b:close_b+1])
    return jsonResponse["rates"][currency]

def convertToUSD(amount, currency, year = None):    
    if (currency=="USD"):
        return amount
    else:
        factor = getUSDConversionFactor(currency, year=year)
        return round(amount / factor,2)

def getCurrencyConversionFactor(currency1, currency2, year = None):
    if  year==None:
        version = "latest"
    else:
        version = year+"-12-31"
    response = callHttpGET("http://api.fixer.io/",version,{"symbols":currency1,"base":currency2,"callback":"?"}).text
    open_b = response.find("{")
    close_b = response.rfind("}")
    jsonResponse = json.loads(response[open_b:close_b+1])
#    jsonResponse = json.loads(response[2:-1])
    return jsonResponse["rates"][currency1]

def convertToCurrency(amount, currency1, currency2, year = None):    
    if (currency1==currency2):
        return amount
    else:
        factor = getCurrencyConversionFactor(currency1, currency2, year=year)
        return round(amount / factor,2)

