import json
import boto3
import random
import requests

from chalice import Chalice

app = Chalice(app_name='DialogFlow-Test')
app.debug = True

@app.route('/')
def index():
  return 'Hello World!'

@app.route('/webhook',methods=['POST'])
def index():
    # A Simple hard coded reply.
    #reply = '{"fulfillmentMessages": [ {"text": {"text": ["The temperature is 21C"] } } ]}'

    #Get the geo-city value from the API and return a random temperature
    body = app.current_request.json_body
    city= body['queryResult']['parameters']['geo-city']
    temperature = str(random.randint(-20,35))
    # reply = '{"fulfillmentMessages": [ {"text": {"text": ["The  temperature in '+ city + ' is ' + temperature + '"] } } ]}'

    #Get the Geo-city and return the real forcast
    #Step 1 find the WOEID of the city.
    api_url='https://www.metaweather.com/api/location/search/?query=' + city
    headers = {'Content-Type': 'application/json'}
    response = requests.get(api_url, headers=headers)
    r= response.json()
    woeid = str(r[0]["woeid"])
    #Step 2 Use the WOEID to find the weather for the city
    api_url='https://www.metaweather.com/api/location/' + woeid
    headers = {'Content-Type': 'application/json'}
    response = requests.get(api_url, headers=headers)
    #Step 3 extract weather data
    r= response.json()
    city = str(r["title"])
    parent = str(r["parent"]["title"])
    weather = str(r["consolidated_weather"][0]["weather_state_name"])
    temp = int(r["consolidated_weather"][0]["the_temp"])
    humidity = str(r["consolidated_weather"][0]["humidity"])
    #Step 3 build the reply.
    reply = '{"fulfillmentMessages": [ {"text": {"text": ["Currently in '+ city + ', '+ parent + ' it is ' + str(temp) + ' degrees and ' + weather + '"] } } ]}'
    return reply

   