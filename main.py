import requests
import skinclass
import pprint
import threading
import time
import csv
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

#Legg t logikk i "getCrazyCheap" som sjekker at et outputtet item faktisk er den billigste av den typen på markedet.

def getCrazyCheap():
        items = []
        response = requests.get(csfloatAPIlink,headers=header,params={"sort_by":"most_recent","min_ref_qty":20,"category":0,"type":"buy_now","max_price":165000})
        jsonData = response.json()

        for i in range(len(jsonData['data'])):
            currentItem = jsonData['data'][i]
            stickerPrice = sum([sticker.get("reference",{}).get("price",0)/100 for sticker in currentItem["item"].get("stickers",[])])

            if currentItem['reference']['base_price'] > currentItem['reference']['predicted_price']:
                if currentItem['price'] < currentItem['reference']['predicted_price']:
                    if stickerPrice>0:
                        stickerPercentage = (currentItem['price']-currentItem['reference']['predicted_price'])/stickerPrice
                    else:
                        stickerPercentage = 0
                    items.append({"Listing id":currentItem['id'],"Item name":currentItem['item']['market_hash_name'],"Profit margin":round(100*(1-currentItem['price']/currentItem['reference']['predicted_price']),3),"Lowest calculated price":currentItem['reference']['predicted_price'],"Sale price":currentItem['price'],"Sticker percentage":stickerPercentage,"Sticker price":stickerPrice,"Icon url":currentItem['item']['icon_url'],"def_index":currentItem['item']['def_index'],"paint_index":currentItem['item'].get('paint_index',0),"float_value":currentItem['item'].get('float_value',0),"is_stattrak":currentItem['item'].get('is_stattrak',0),"is_souvenir":currentItem['item'].get('is_souvenir',0),"sticker_index":currentItem['item'].get("sticker_index",0),"is_commodity":currentItem['item'].get('is_commodity',0),"keychain_index":currentItem['item'].get('keychain_index',0),"rarity":currentItem['item'].get('rarity',0),"target":"sjekk"})
            else:
                if currentItem['price'] < currentItem['reference']['base_price']:
                    if stickerPrice>0:
                        stickerPercentage = (currentItem['price']-currentItem['reference']['base_price'])/stickerPrice
                    else:
                        stickerPercentage = 0
                    items.append({"Listing id":currentItem['id'],"Item name":currentItem['item']['market_hash_name'],"Profit margin":round(100*(1-currentItem['price']/currentItem['reference']['base_price']),3),"Lowest calculated price":currentItem['reference']['base_price'],"Sale price":currentItem['price'],"Sticker percentage":stickerPercentage,"Sticker price":stickerPrice,"Icon url":currentItem['item']['icon_url'],"def_index":currentItem['item']['def_index'],"paint_index":currentItem['item'].get('paint_index',0),"float_value":currentItem['item'].get('float_value',0),"is_stattrak":currentItem['item'].get('is_stattrak',0),"is_souvenir":currentItem['item'].get('is_souvenir',0),"sticker_index":currentItem['item'].get("sticker_index",0),"is_commodity":currentItem['item'].get('is_commodity',0),"keychain_index":currentItem['item'].get('keychain_index',0),"rarity":currentItem['item'].get('rarity',0),"target":"sjekk"})

        responseBestDeal = requests.get(csfloatAPIlink,headers=header,params={"sort_by":"expires_soon","category":0,"type":"buy_now","max_price":165000,"min_ref_qty":20})
        jsonData2 = responseBestDeal.json()
        for i in range(len(jsonData2['data'])):
            currentItem = jsonData2['data'][i]
            stickerPrice = sum([sticker.get("reference",{}).get("price",0)/100 for sticker in currentItem["item"].get("stickers",[])])
            if currentItem['reference']['base_price'] > currentItem['reference']['predicted_price']:
                if currentItem['price'] < currentItem['reference']['predicted_price']:
                    if stickerPrice>0:
                        stickerPercentage = (currentItem['price']-currentItem['reference']['predicted_price'])/stickerPrice
                    else:
                        stickerPercentage = 0
                    items.append({"Listing id":currentItem['id'],"Item name":currentItem['item']['market_hash_name'],"Profit margin":round(100*(1-currentItem['price']/currentItem['reference']['predicted_price']),3),"Lowest calculated price":currentItem['reference']['predicted_price'],"Sale price":currentItem['price'],"Sticker percentage":stickerPercentage,"Sticker price":stickerPrice,"Icon url":currentItem['item']['icon_url'],"def_index":currentItem['item']['def_index'],"paint_index":currentItem['item'].get('paint_index',0),"float_value":currentItem['item'].get('float_value',0),"is_stattrak":currentItem['item'].get('is_stattrak',0),"is_souvenir":currentItem['item'].get('is_souvenir',0),"sticker_index":currentItem['item'].get("sticker_index",0),"is_commodity":currentItem['item'].get('is_commodity',0),"keychain_index":currentItem['item'].get('keychain_index',0),"rarity":currentItem['item'].get('rarity',0),"target":"sjekk"})
            else:
                if currentItem['price'] < currentItem['reference']['base_price']:
                    if stickerPrice>0:
                        stickerPercentage = (currentItem['price']-currentItem['reference']['base_price'])/stickerPrice
                    else:
                        stickerPercentage = 0
                    items.append({"Listing id":currentItem['id'],"Item name":currentItem['item']['market_hash_name'],"Profit margin":round(100*(1-currentItem['price']/currentItem['reference']['base_price']),3),"Lowest calculated price":currentItem['reference']['base_price'],"Sale price":currentItem['price'],"Sticker percentage":stickerPercentage,"Sticker price":stickerPrice,"Icon url":currentItem['item']['icon_url'],"def_index":currentItem['item']['def_index'],"paint_index":currentItem['item'].get('paint_index',0),"float_value":currentItem['item'].get('float_value',0),"is_stattrak":currentItem['item'].get('is_stattrak',0),"is_souvenir":currentItem['item'].get('is_souvenir',0),"sticker_index":currentItem['item'].get("sticker_index",0),"is_commodity":currentItem['item'].get('is_commodity',0),"keychain_index":currentItem['item'].get('keychain_index',0),"rarity":currentItem['item'].get('rarity',0),"target":"sjekk"})


        return sorted(items,key=lambda d:d['Profit margin'],reverse=False)

def getLowStickerPercentage():
        items = []
        response = requests.get(csfloatAPIlink,headers=header,params={"sort_by":"most_recent","category":1,"type":"buy_now","min_ref_qty":20,"max_price":165000})
        jsonData = response.json()

        for i in range(len(jsonData['data'])):
            currentItem = jsonData['data'][i]
            stickerPrice = sum([sticker.get("reference",{}).get("price",0)/100 for sticker in currentItem["item"].get("stickers",[])])
            if stickerPrice>0:
                if currentItem['reference']['base_price'] > currentItem['reference']['predicted_price']:
                    stickerPercentage = (currentItem['price']-currentItem['reference']['predicted_price'])/stickerPrice
                    if stickerPercentage < 0.1:
                         items.append({"Listing id":currentItem['id'],"Item name":currentItem['item']['market_hash_name'],"Profit margin":round(100*(1-currentItem['price']/currentItem['reference']['predicted_price']),3),"Lowest calculated price":currentItem['reference']['predicted_price'],"Sale price":currentItem['price'],"Sticker percentage":stickerPercentage,"Sticker price":stickerPrice,"Icon url":currentItem['item']['icon_url'],"def_index":currentItem['item']['def_index'],"paint_index":currentItem['item'].get('paint_index',0),"float_value":currentItem['item'].get('float_value',0),"is_stattrak":currentItem['item'].get('is_stattrak',0),"is_souvenir":currentItem['item'].get('is_souvenir',0),"sticker_index":currentItem['item'].get("sticker_index",0),"is_commodity":currentItem['item'].get('is_commodity',0),"keychain_index":currentItem['item'].get('keychain_index',0),"rarity":currentItem['item'].get('rarity',0),"target":"sjekk"})
                else:
                    stickerPercentage = (currentItem['price']-currentItem['reference']['base_price'])/stickerPrice        
                    if stickerPercentage < 0.1:
                        items.append({"Listing id":currentItem['id'],"Item name":currentItem['item']['market_hash_name'],"Profit margin":round(100*(1-currentItem['price']/currentItem['reference']['base_price']),3),"Lowest calculated price":currentItem['reference']['base_price'],"Sale price":currentItem['price'],"Sticker percentage":stickerPercentage,"Sticker price":stickerPrice,"Icon url":currentItem['item']['icon_url'],"def_index":currentItem['item']['def_index'],"paint_index":currentItem['item'].get('paint_index',0),"float_value":currentItem['item'].get('float_value',0),"is_stattrak":currentItem['item'].get('is_stattrak',0),"is_souvenir":currentItem['item'].get('is_souvenir',0),"sticker_index":currentItem['item'].get("sticker_index",0),"is_commodity":currentItem['item'].get('is_commodity',0),"keychain_index":currentItem['item'].get('keychain_index',0),"rarity":currentItem['item'].get('rarity',0),"target":"sjekk"})
        
        responseStattrack = requests.get(csfloatAPIlink,headers=header,params={"sort_by":"most_recent","category":2,"type":"buy_now","min_ref_qty":20,"max_price":165000})
        jsonData2 = responseStattrack.json()
        for i in range(len(jsonData2['data'])):
            currentItem = jsonData2['data'][i]
            stickerPrice = sum([sticker.get("reference",{}).get("price",0)/100 for sticker in currentItem["item"].get("stickers",[])])
            if stickerPrice>0:
                if currentItem['reference']['base_price'] > currentItem['reference']['predicted_price']:
                    stickerPercentage = (currentItem['price']-currentItem['reference']['predicted_price'])/stickerPrice
                    if stickerPercentage < 0.1:
                         items.append({"Listing id":currentItem['id'],"Item name":currentItem['item']['market_hash_name'],"Profit margin":round(100*(1-currentItem['price']/currentItem['reference']['predicted_price']),3),"Lowest calculated price":currentItem['reference']['predicted_price'],"Sale price":currentItem['price'],"Sticker percentage":stickerPercentage,"Sticker price":stickerPrice,"Icon url":currentItem['item']['icon_url'],"def_index":currentItem['item']['def_index'],"paint_index":currentItem['item'].get('paint_index',0),"float_value":currentItem['item'].get('float_value',0),"is_stattrak":currentItem['item'].get('is_stattrak',0),"is_souvenir":currentItem['item'].get('is_souvenir',0),"sticker_index":currentItem['item'].get("sticker_index",0),"is_commodity":currentItem['item'].get('is_commodity',0),"keychain_index":currentItem['item'].get('keychain_index',0),"rarity":currentItem['item'].get('rarity',0),"target":"sjekk"})
                else:
                    stickerPercentage = (currentItem['price']-currentItem['reference']['base_price'])/stickerPrice   
                    if stickerPercentage < 0.1:
                        items.append({"Listing id":currentItem['id'],"Item name":currentItem['item']['market_hash_name'],"Profit margin":round(100*(1-currentItem['price']/currentItem['reference']['base_price']),3),"Lowest calculated price":currentItem['reference']['base_price'],"Sale price":currentItem['price'],"Sticker percentage":stickerPercentage,"Sticker price":stickerPrice,"Icon url":currentItem['item']['icon_url'],"def_index":currentItem['item']['def_index'],"paint_index":currentItem['item'].get('paint_index',0),"float_value":currentItem['item'].get('float_value',0),"is_stattrak":currentItem['item'].get('is_stattrak',0),"is_souvenir":currentItem['item'].get('is_souvenir',0),"sticker_index":currentItem['item'].get("sticker_index",0),"is_commodity":currentItem['item'].get('is_commodity',0),"keychain_index":currentItem['item'].get('keychain_index',0),"rarity":currentItem['item'].get('rarity',0),"target":"sjekk"})

        return sorted(items,key=lambda d:d['Profit margin'],reverse=False)

def timer(func1,func2):
     while True:
        print("In while loop")
        func1()
        func2()
        time.sleep(120) #ping every 2 minutes

def sendToDiscord(item):
    webhook_url = 'https://discord.com/api/webhooks/1348735436876677341/ZCEz8_VAi23TXQUAVyUXHZE9AyiP-s8Vz9PdqzLvg8sblvoOC0p9i5hyUYgPYsy4Tx56'
    embeds =[{
        "title": f":fire: {item['Item name']} :fire:", 
        "description": f"Profit margin: **{item['Profit margin']}** \n [**LISTING**](https://csfloat.com/item/{item['Listing id']})",
        "color": 1127128#,
        #"image":{"url":f"https://community.cloudflare.steamstatic.com/economy/image/{item['Icon url']}"}
    }]#,{
    #     "title": "This is :fire:",
    #     "color": 14177041
    #}]
    data = {
         "username":"csfloat scanner",
         "avatar_url":"https://imgur.com/gallery/incase-you-havent-seen-this-show-yet-NBEIFBz.png",
         "embeds":embeds
         }
    resp = requests.post(webhook_url, json=data)
    print(resp.status_code,resp.text)

def checkNotDuplicateListing(item):
    listing_id =  item["Listing id"]
    filename = "data.txt"
    id_found = -1
    with open(filename,mode="r") as file:
        entireFile = file.read()
        id_found = entireFile.find(listing_id)
        if id_found == -1:
            return True
        else:
            return False
     
def runShi():
    cheapItems = getCrazyCheap()
    # Save to a CSV file
    filename = "data.txt"  # You can use .csv as well
    if(len(cheapItems))>0:
        with open(filename, mode="a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=cheapItems[0].keys())
            for item in cheapItems:
                if(checkNotDuplicateListing(item)):
                    #writer.writeheader()  # Write column names
                    writer.writerow(item)  # Write rows
                    sendToDiscord(item)
    
    pprint.pprint(cheapItems)
    

def runShi2():
    cheapStickeredItems = getLowStickerPercentage()
    filename = "data.txt"  # You can use .csv as well
    if(len(cheapStickeredItems))>0:
        with open(filename, mode="a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=cheapStickeredItems[0].keys())
            for item in cheapStickeredItems:
                if(checkNotDuplicateListing(item)):
                    #writer.writeheader()  # Write column names
                    writer.writerow(item)  # Write rows
                    sendToDiscord(item)
    
    pprint.pprint(cheapStickeredItems)
    

t = threading.Thread(target=timer,args=(runShi,runShi2))
t.start()



