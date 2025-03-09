import requests
import skinclass
import pprint
import threading
import time
#api key csfloat: Rd3UmYDMXvJlqwueoFJoaI11rpyuOHgv

#all listings: https://csfloat.com/api/v1/listings
#specific listing: https://csfloat.com/api/v1/listings/<ID>

csfloatAPIlink = "https://csfloat.com/api/v1/listings"

with open("api_key.txt","r") as f:
        api_key = f.readline()

header={
    "Authorization": api_key
    }

desertHydraParameters={
    "market_hash_name": "AWP | Desert Hydra (Field-Tested)",
    "category": 1,
    "sort_by": "most_recent",
    "type": "buy_now",
    "state": "listed",
    "max_float": 0.27,
    "max_price": 185000,
}

#desertHydra = skinclass.Skin(desertHydraParameters)
#desertHydra.getCheapest(1650)
#print(desertHydra.cheapestItems)

def getCrazyCheap():
        items = []
        response = requests.get(csfloatAPIlink,headers=header,params={"sort_by":"most_recent","category":0,"type":"buy_now","max_price":165000})
        jsonData = response.json()

        for i in range(len(jsonData['data'])):
            currentItem = jsonData['data'][i]
            if currentItem['reference']['base_price'] > currentItem['reference']['predicted_price']:
                if currentItem['price'] < currentItem['reference']['predicted_price']:
                    items.append({"Listing id":currentItem['id'],"Item name":currentItem['item']['market_hash_name'],"Profit margin":round(100*(1-currentItem['price']/currentItem['reference']['predicted_price']),3)})
            else:
                if currentItem['price'] < currentItem['reference']['base_price']:
                    items.append({"Listing id":currentItem['id'],"Item name":currentItem['item']['market_hash_name'],"Profit margin":round(100*(1-currentItem['price']/currentItem['reference']['base_price']),3)})

        return sorted(items,key=lambda d:d['Profit margin'],reverse=False)

def getLowStickerPercentage():
        items = []
        response = requests.get(csfloatAPIlink,headers=header,params={"sort_by":"most_recent","category":1,"type":"buy_now","max_price":165000})
        jsonData = response.json()

        for i in range(len(jsonData['data'])):
            currentItem = jsonData['data'][i]
            stickerPrice = sum([sticker.get("reference",{}).get("price",0)/100 for sticker in currentItem["item"].get("stickers",[])])
            if stickerPrice>0:
                if currentItem['reference']['base_price'] > currentItem['reference']['predicted_price']:
                    if (currentItem['price']-currentItem['reference']['predicted_price'])/stickerPrice < 0.1:
                         items.append({"Listing id":currentItem['id'],"Item name":currentItem['item']['market_hash_name'],"Profit margin":round(100*(1-currentItem['price']/currentItem['reference']['predicted_price']),3)})
                else:     
                    if (currentItem['price']-currentItem['reference']['base_price'])/stickerPrice < 0.1:
                        items.append({"Listing id":currentItem['id'],"Item name":currentItem['item']['market_hash_name'],"Profit margin":round(100*(1-currentItem['price']/currentItem['reference']['base_price']),3)})
        
        responseStattrack = requests.get(csfloatAPIlink,headers=header,params={"sort_by":"most_recent","category":2,"type":"buy_now","max_price":165000})
        jsonData2 = responseStattrack.json()
        for i in range(len(jsonData2['data'])):
            currentItem = jsonData2['data'][i]
            stickerPrice = sum([sticker.get("reference",{}).get("price",0)/100 for sticker in currentItem["item"].get("stickers",[])])
            if stickerPrice>0:
                if currentItem['reference']['base_price'] > currentItem['reference']['predicted_price']:
                    if (currentItem['price']-currentItem['reference']['predicted_price'])/stickerPrice < 0.1:
                         items.append({"Listing id":currentItem['id'],"Item name":currentItem['item']['market_hash_name'],"Profit margin":round(100*(1-currentItem['price']/currentItem['reference']['predicted_price']),3)})
                else:     
                    if (currentItem['price']-currentItem['reference']['base_price'])/stickerPrice < 0.1:
                        items.append({"Listing id":currentItem['id'],"Item name":currentItem['item']['market_hash_name'],"Profit margin":round(100*(1-currentItem['price']/currentItem['reference']['base_price']),3)})

        return sorted(items,key=lambda d:d['Profit margin'],reverse=False)

def timer(func1,func2):
     while True:
        func1()
        func2()
        time.sleep(90) #2 minutes

def sendToDiscord(item):
    webhook_url = "https://discord.com/api/webhooks/1348120570822266891/yXXE86xTw4yJkJafiYJe_wHPzlCFcp0dhuCyJNZ-l1ikG758gemfjHNyo89dEC1LoY0B"
    message = {
        "content": f"{item['Item name']}, Profit margin: {item['Profit margin']} \n [Listing](https://csfloat.com/item/{item['Listing id']}) "
    }
    requests.post(webhook_url, json=message)

def runShi():
     cheapItems = getCrazyCheap()
     for item in cheapItems:
        sendToDiscord(item)

def runShi2():
     cheapStickeredItems = getLowStickerPercentage()
     for item in cheapStickeredItems:
        sendToDiscord(item)

t = threading.Thread(target=timer,args=(runShi,runShi2))
t.start()


     

#pprint.pprint(cheapItems)
#pprint.pprint(cheapStickeredItems)
