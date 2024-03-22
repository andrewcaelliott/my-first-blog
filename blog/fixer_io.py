import sys
import json
#sys.path.append("../scripts")
from .PyHttpCall import callHttpGET

def getUSDConversionFactor(currency, year = None):
    if  year==None:
        version = "latest"
    else:
        version = year+"-12-31"
    response = callHttpGET("http://data.fixer.io/api/",version,{"access_key":"c65acaa2ab282e6eb961788d69eacc69","symbols":currency+',USD',"base":"EUR","callback":"?"}).text
    open_b = response.find("{")
    close_b = response.rfind("}")
    jsonResponse = json.loads(response[open_b:close_b+1])
    return jsonResponse["rates"][currency]/jsonResponse["rates"]['USD']

def convertToUSD(amount, currency, year = None):    
    if (currency=="USD"):
        return amount
    else:
        factor = getUSDConversionFactor(currency, year=year)
        return round(amount / factor,2)

def getCurrencyConversionFactor(currency1, currency2, year = None):
    if year==None:
        version = "latest"
    else:
        version = year+"-12-31"
    response = callHttpGET("http://data.fixer.io/api/",version,{"access_key":"c65acaa2ab282e6eb961788d69eacc69","symbols":currency1+','+currency2,"base":'EUR',"callback":"?"}).text
    open_b = response.find("{")
    close_b = response.rfind("}")
    jsonResponse = json.loads(response[open_b:close_b+1])
#    jsonResponse = json.loads(response[2:-1])
    return jsonResponse["rates"][currency1]/jsonResponse["rates"][currency2]

def convertToCurrency(amount, currency1, currency2, year = None):    
    if currency1.find("USD")>=0:
        currency1 = "USD"
    if (currency1==currency2):
        return amount
    else:
        factor = getCurrencyConversionFactor(currency1, currency2, year=year)
        return round(amount / factor,2)

