import requests #The requests module allows you to send HTTP requests using Python.
import json
from time import sleep
from bs4 import BeautifulSoup
import re 
import pandas as pd
from flask import Flask, render_template, abort, url_for, json, jsonify
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def my_form_post():
    name = request.form['name']
    #add more fields here 
    #processed_text = text.upper()
    results = bioscraper_func(name)#process more than one text field 
    return render_template('./index.html', data=results)
    #return results



def bioscraper_func(name):

    name = str(name)
    text= "linkedin.com" + name 
    page = requests.get("https://www.google.dz/search?q="+text)
    soup = BeautifulSoup(page.content, features="html.parser")
    links = soup.findAll("a")
    linkedin_urls = []


    for link in  soup.find_all("a",href=re.compile("(?<=/url\?q=)(htt.*://.*)")):
        linkedin_urls.append(re.split(":(?=http)",link["href"].replace("/url?q=","")))

    Final_URL = linkedin_urls[0]
    Final_URL_X = Final_URL[0].split('&')[0]
    print(Final_URL_X)

    username = 'shashinsv'
    apiKey = 'zNJoRie9vmzPdFCBWTrPvzVOF'
    scraper = 'linkedinProfile'
    url = Final_URL_X #'https://ca.linkedin.com/in/vakilinia'

    apiEndPoint = "http://api.scraping-bot.io/scrape/data-scraper"
    apiEndPointResponse = "http://api.scraping-bot.io/scrape/data-scraper-response?"

    payload = json.dumps({"url": url, "scraper": scraper}) #converts a Python object into a json string
    headers = {
        'Content-Type': "application/json"
    }

    response = requests.request("POST", apiEndPoint, data=payload, auth=(username, apiKey), headers=headers)
    if response.status_code == 200:
        print(response.json())
        print(response.json()["responseId"])
        responseId = response.json()["responseId"]

        pending = True
        while pending:
            # sleep 5s between each loop, social-media scraping can take quite long to complete
            # so there is no point calling the api quickly as we will return an error if you do so
            sleep(10)
            finalResponse = requests.request("GET", apiEndPointResponse + "scraper=" + scraper + "&responseId=" + responseId
                                             , auth=(username, apiKey))
            result = finalResponse.json()
            if type(result) is list:
                pending = False
                print(finalResponse.text)
            elif type(result) is dict:
                print(result)
                if result["status"] == "pending":
                    print(result["message"])
                    continue
                elif result["error"] is not None:
                    pending = False
                    print(json.dumps(result, indent=4))

    else:
        print(response.text)
        
    try: 
      List_former_companies = [x['subtitle'] for x in result[0]['experience']][1:]
    except:
      print('No Former Employee') 
      
    Final_String = "" + result[0]['name'] + "    "
    #result[0].keys()

    if len(result[0]['about'])>4:
      Final_String = Final_String + '    ' + ' ' + result[0]['about'] + "."

    if len(result[0]['current_company'])>0:
      Final_String = Final_String + '    ' + result[0]['name'] + " is currently working for " + result[0]['current_company']['name'] + " as a " + result[0]['position'] + "."

    if len(List_former_companies)>0 : 
      Final_String = Final_String + '   ' + " Prior to " + result[0]['current_company']['name'] + ", "  + result[0]['name'] + " has worked for "  + str(List_former_companies[:3]).replace('[','').replace(']','').replace("'",'').replace(']','') + "."


    if len(result[0]['city'])>0:
        Final_String = Final_String + '  ' + result[0]['name'] + " is currently based in " + result[0]['city'] + "."

    if len(result[0]['education'])>0:  
        Final_String = Final_String + '  ' + result[0]['name'] + " has got " + result[0]['education'][0]['degree'] + " from " + result[0]['education'][0]['title'] + " in " + result[0]['education'][0]['field'] + "."

    return(Final_String)
    
if __name__ == '__main__':
        app.run(host='localhost', debug=True)
  
#'position', 
#'current_company'