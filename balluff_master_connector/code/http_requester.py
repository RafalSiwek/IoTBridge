import requests
import json

def get_req():

      # api-endpoint 
      URL = "http://192.168.0.2/dprop.jsn"
      # sending get request and saving the response as response object 
      while True:
            try:
                  r = requests.get(URL,timeout=2)
            except requests.exceptions.Timeout:
                  print(f'timeout, retrying ....')
                  continue
            except requests.exceptions.TooManyRedirects:
                  return "Wrong url"
            except requests.exceptions.RequestException as e:
                  print(e)
                  raise SystemExit(e)
            break

      # extracting data in json format 
      data = r.json() 
      # printing the output 
      print(f'{data}')
      #return data
      return data