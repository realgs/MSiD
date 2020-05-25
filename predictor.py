import requests
from datetime import datetime



r = requests.get('https://api-public.sandbox.pro.coinbase.com/products/BTC-USD/candles',
    params={'start':'2019-08-01','end':'2020-05-24','granularity':'86400'})

data = r.json()
for d in data:
    print(datetime.fromtimestamp(d[0]))
    #print(d)
    if (d[3] - d[4]) < 0:
        print("Urus o {}%".format((d[4]-d[3])/d[4]))
    else:
        print("zmalał o {}%".format((d[3]-d[4])/d[4]))