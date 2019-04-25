
import json, requests
import numpy as np
import os, sys
import datetime, time

def init():    
  return None
    
    
def run(manager):
  try: 
    adls_connect_obj = manager.connect_adls()

    # api parameters
    city_ids = ['5747882', '5809844', '5799841', '5816449', '5812944', '5786882']
    city_batch = ",".join(city_ids)
    cities = ['Redmond, WA, USA','Seattle, WA, USA', 'Kirkland, WA, USA', 'Woodinville, WA, USA', 'Tacoma, WA, USA', 'Bellevue, WA, USA']
    
    response = requests.get("http://api.openweathermap.org/data/2.5/group?id=" + city_batch + "&appid=" + manager.weather_api_token)
    
    output_datetime = datetime.datetime.utcnow()
    data_output_path = "raw/weather_data/{}/{}/{}/{}/{}/weather_data.json".format(output_datetime.year, output_datetime.month, output_datetime.day, output_datetime.hour, output_datetime.minute)

    # write json file to adls
    manager.write_json_file(adls_connect_obj, data_output_path, response.content.decode('utf8'))

    return "200: Success"

  except Exception as e: 
    return str(e)
    
