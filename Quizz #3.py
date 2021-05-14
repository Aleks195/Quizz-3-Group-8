import requests
import json
import sqlite3

conn = sqlite3.connect('one_call_weather.sqlite')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS _weather 
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            sunrise INTEGER,
            sunset INTEGER,
            moonset INTEGER 
            )''') #ფუნქცია ქმნის ცხრილს, სადაც sunrise, sunset და moonset არის სვეტები

city = "Tbilisi"
key = "a96d6412ce5a268dcbfba2e59b7f9cc5"
lat = 33.44
lon = -94.04
units = "metric"
part = "hourly, daily"
url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude={part}&appid={key}&units={units}"

r = requests.get(url)
print(r.status_code)
print(r.headers)
print(r.text)
res = r.json()
#print(json.dumps(res, indent=4))


with open('data.json', 'w') as file:
    json.dump(res, file, indent=4)

print(res['daily'])
print(res['current']['temp'])


for each in res['daily']:
    sunrise = each['sunrise']
    sunset = each['sunset']
    moonset = each['moonset']
    row = (sunrise, sunset, moonset)

    c.execute('INSERT INTO _weather (sunrise, sunset, moonset) VALUES (?, ?, ?)', row)

conn.commit()
conn.close()