import requests
import skinclass
import pprint
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
        response = requests.get(csfloatAPIlink,headers=header,params={"sort_by":"most_recent","category":1,"type":"buy_now","max_price":165000})
        jsonData = response.json()

        for i in range(len(jsonData['data'])):
            currentItem = jsonData['data'][i]
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
                if (currentItem['price']-currentItem['reference']['base_price'])/stickerPrice < 0.1:
                    items.append({"Listing id":currentItem['id'],"Item name":currentItem['item']['market_hash_name'],"Profit margin":round(100*(1-currentItem['price']/currentItem['reference']['base_price']),3)})
        if len(items)==0:
              return 
        else:
            return sorted(items,key=lambda d:d['Profit margin'],reverse=False)

cheapItems = getCrazyCheap()
pprint.pprint(cheapItems)

cheapStickeredItems = getLowStickerPercentage()
pprint.pprint(cheapStickeredItems)