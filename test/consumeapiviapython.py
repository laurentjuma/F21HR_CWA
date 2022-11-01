# Consume api via python

import requests
import json

# Get the token
# url = "http://localhost:8000/api/token/"
# payload = {'username': 'admin', 'password': 'admin'}
# headers = {'Content-Type': 'application/json'}
# response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
# token = response.json()['access']

# Get the data
url = "https://www.thecocktaildb.com/api/json/v1/1/popular.php"
# headers = {'Authorization': 'Bearer ' + token}
response = requests.request("GET", url)
print(response.json())

#Google calendar api
#https://developers.google.com/calendar/quickstart/python