import pandas as pd
import requests
import csv

apikey = "51151d8bff82d479e65a9aacd3ffbe62"
url_for_symbols = f"https://api.forexrateapi.com/v1/symbols?api_key={apikey}"
resp = requests.get(url_for_symbols)
symbols_list = list(resp.json()["symbols"].keys())
print(symbols_list) ##all current currencies
#Burada tüm currencylere ait kodları alabiliyoruz ve aşağıdaki kodda currencies yerine koyup direkt tüm currencies için veriyi alabiliriz.
#Fakat araştırdığım ücretsiz apilerin hiçbirinde belli bir zaman aralığı için ücretsiz kullanabileceğim api bulamadım.
#Burada aldığım currency'lerin 5 tanesi için tek tek sorgu atarak dosya oluşturmayı tercih ettim.

start_date = "2021-01-01"
end_date = "2021-01-10"
base_currency = "USD"

output_dict = {"date": [], "name": [], "value": []}
headers = {"accept": "application/json"}
for symbol in symbols_list[:5]: # ilk 5 tanesini bu döngüde seçiyorum.
  url = f"https://api.forexrateapi.com/v1/timeframe?api_key={apikey}&start_date={start_date}&end_date={end_date}&base={base_currency}&currencies={symbol}"
  response = requests.get(url, headers=headers)
  #print(response.text)
  data = response.json()["rates"]
  for key, value in data.items():
    output_dict["date"].append(key)
    output_dict["name"].append(symbol)
    output_dict["value"].append(value[symbol])

df = pd.DataFrame.from_dict(output_dict)
df = df.sort_values(by=['date', 'name'])
df.head(10)

df.to_csv("currencies.csv", index=False)