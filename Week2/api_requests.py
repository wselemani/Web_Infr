import requests

API_KEY = ""

with open('.env') as f:
    for line in f:
        if line.startwith("NASA_KEY"):
            API_KEY = line.split(':')[1].strip().strip("")
            break

URL = f"https://science.nasa.gov/wp.json/wp/v2/apod-basic/?api_key={API_KEY}"
response_obj = requests.get(URL)
status = response_obj.status_code

if status != 200:
    print(f"Something went wrong with status: {status}")
else: 
     data = response_obj.json

print(data)


