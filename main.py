import matplotlib.pyplot as plt 
import os
import urllib.request
import json
import io
import base64
import redis
import time
import sys



fields = [
    "fully_diluted_valuation",
    "price_change_24h",
    "market_cap_change_24h",
    "market_cap_change_percentage_24h",
    "circulating_supply",
    "total_supply",
    "max_supply",
    "ath",
    "ath_change_percentage",
    "ath_date",
    "atl",
    "atl_change_percentage",
    "atl_date",
    "roi",
    "last_updated",
]


r = redis.Redis(
    host=sys.argv[3],
    port=int(sys.argv[2]), 
    password=sys.argv[1])


url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd'
contents = urllib.request.urlopen(url).read()
data = json.loads(contents)


for i in fields:
    for j in range(100):
        data[j].pop(i)
        
for j in range(100):
    s = io.BytesIO()


    url = 'https://api.coingecko.com/api/v3/coins/'+data[j]['id']+'/market_chart?vs_currency=usd&ids=bitcoin&days=7'
    contents = urllib.request.urlopen(url).read()
    dat = json.loads(contents)

    X1 = [] 
    Y1 = [] 

    for i in dat['prices']:
        X1.append(i[0])
        Y1.append(i[1])
    # Setting the figure size
    fig = plt.figure(figsize=(10,5))
    # plotting the first plot
    plt.plot(X1, Y1, linewidth=12.0) 
  
    plt.axis('off')

  
    # Show a legend on the plot 
    plt.legend() 
    #Saving the plot as an image
    fig.savefig(s, bbox_inches='tight', dpi=50)

    b64_string = 'data:image/jpeg;base64,' + base64.b64encode(s.getvalue()).decode("utf-8").replace("\n", "")

    p = {"plot":b64_string}
    data[j].update(p)
    
    #print(json.dumps(data[j]))
    time.sleep(5)
    

r.set('markets', json.dumps(data))

#print(json.dumps(data))
