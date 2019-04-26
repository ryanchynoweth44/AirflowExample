
import json, requests
import numpy as np
import os, sys
import datetime, time

def init():    
  return None
    
    
def run(api_token):
    # api parameters
    city_ids = ['5747882', '5809844', '5799841', '5816449', '5812944', '5786882']
    city_batch = ",".join(city_ids)
    cities = ['Redmond, WA, USA','Seattle, WA, USA', 'Kirkland, WA, USA', 'Woodinville, WA, USA', 'Tacoma, WA, USA', 'Bellevue, WA, USA']
    
    response = requests.get("http://api.openweathermap.org/data/2.5/group?id=" + city_batch + "&appid=" + api_token)
    
    return json.loads(response.content)

    
