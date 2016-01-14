import json
import sys
import base64
import requests

def post(targetURL, params, contentType="text/xml", username=None, trace=0):
    if trace:
        print(targetURL)
        print(params)
    if (username!=None):
        auth = username.split(":")
        r = requests.post(targetURL, data = params, auth=(auth[0], auth[1]))
    else:
        r = requests.post(targetURL, data = params)
    if trace:
        print(r)
    return r
'''
    print("params is ", type(params))
    if(type(params) is dict):
        paramStr = ""
        for aKey in params.keys():
            paramStr+=aKey+"="+URLEncoder.encode(params[aKey], "UTF-8")+"&"
        paramStr=paramStr[:-1]
        url = URL(targetURL+"?"+paramStr)
    else:
        paramStr = params
        url = URL(targetURL)
    if trace:        
        print(targetURL)
        print(paramStr)
        print(contentType)
        print(url)

    connection = url.openConnection()
    if username!=None:    
        userpass = username
        basicAuth = "Basic " + base64.b64encode(userpass);
        connection.setRequestProperty ("Authorization", basicAuth);
    connection.setRequestMethod("POST")
    if contentType != None:
        connection.setRequestProperty("Content-Type", contentType)
    connection.setRequestProperty("Content-Length", str(len(paramStr)))
    connection.setRequestProperty("Content-Language", "en-GB")
    connection.setUseCaches(0)
    connection.setDoInput(1)
    connection.setDoOutput(2)
    
    if(not(type(params) is dict)):
        wr= DataOutputStream(connection.getOutputStream())
        wr.writeBytes(paramStr)
        wr.flush()
        wr.close()

    inStream= connection.getInputStream()
    rd= BufferedReader(InputStreamReader(inStream))
    response = ""
    line = rd.readLine()
    while line != None:
        response +=line+"\r"
        line = rd.readLine()
    rd.close()
    return response
'''    
def get(targetURL, params, username=None, trace=0):
    if trace:
        print(targetURL)
        print(params)
    if (username!=None):
        auth = username.split(":")
        r = requests.get(targetURL, params = params, auth=(auth[0], auth[1]))
        if trace:
            print(r)
    else:
        r = requests.get(targetURL, params = params)
        if trace:
            print(r)
    return r

    
def delete(targetURL, params):
    url = URL(targetURL)
    connection = url.openConnection()
    connection.setRequestMethod("DELETE")    
    connection.setRequestProperty("Content-Language", "en-GB")
    connection.setUseCaches(0)
    connection.setDoOutput(2)
    inStream= connection.getInputStream()
    rd= BufferedReader(InputStreamReader(inStream))
    response = ""
    line = rd.readLine()
    while line != None:
        response +=line+"\r"
        line = rd.readLine()
    rd.close()
    return response
    

def callHttpPOST(uri, service, data, contentType="text/xml", username=None, trace=0):
    response = post(uri+service, data, contentType=contentType, username=username, trace=trace)
    return response

def callHttpDELETE(uri, service, data):
    response = delete(uri+service, data)
    return response
    
def callHttpGET(uri, service, data, username=None, trace=0):
    response = get(uri+service, data, username=username, trace=trace)
    return response
    
def run():
    #http://api.fixer.io/latest?symbols=USD,GBP
    print("test")
    #print(callHttpGET("http://api.fixer.io/","latest",{"symbols":"EUR,GBP","base":"USD","callback":"?"}).content)
