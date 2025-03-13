import requests
import skinclass
import pprint
import threading
import time
import csv
import joblib
import pandas as pd
import statistics
import json
#api key csfloat: Rd3UmYDMXvJlqwueoFJoaI11rpyuOHgv

#all listings: https://csfloat.com/api/v1/listings
#specific listing: https://csfloat.com/api/v1/listings/<ID>
# get listing buy orders where limit is parameter: https://csfloat.com/api/v1/listings/819545332085033605/buy-orders?limit=10 https://csfloat.com/api/v1/listings/currentItem['Listing id']/buy-orders params={"limit":10}
# get similar listings of item: https://csfloat.com/api/v1/listings/819545332085033605/similar https://csfloat.com/api/v1/listings/currentItem['Listing id']/similar
# get latest sales of item: https://csfloat.com/api/v1/history/Seal%20Team%206%20Soldier%20%7C%20NSWC%20SEAL/sales https://csfloat.com/api/v1/history/currentItem['item']['Item name']/sales

#potential feature: highest_buy_order/current_item_price where closer to 1 means better price demand
#potential feature: current_sale_price < weight*median_latest_sales, where weight could be around 0.9-0.95 
csfloatAPIlink = "https://csfloat.com/api/v1/listings"
csfloat_purchaselink = "https://csfloat.com/api/v1/listings/buy"
csfloatHistory = "https://csfloat.com/api/v1/history"


with open("api_key.txt","r") as f:
        api_key = f.readline()

header={
    "Authorization": api_key
    }

purchase_header={
    "Authorization": api_key,
    "Content-Type": "application/json"
    }

loaded_model = joblib.load("./random_forest.joblib")

# desertHydraParameters={
#     "market_hash_name": "AWP | Desert Hydra (Field-Tested)",
#     "category": 1,
#     "sort_by": "most_recent",
#     "type": "buy_now",
#     "state": "listed",
#     "max_float": 0.27,
#     "max_price": 185000,
# }

#desertHydra = skinclass.Skin(desertHydraParameters)
#desertHydra.getCheapest(1650)
#print(desertHydra.cheapestItems)
def funcd(currentItem):
    similarListings = (requests.get(f"{csfloatAPIlink}/{currentItem['id']}/similar",headers=header,params={"sort_by":"lowest_price","limit":10})).json()
    buyOrders = (requests.get(f"{csfloatAPIlink}/{currentItem['id']}/buy-orders",headers=header,params={"limit":5})).json()
    latestSales = (requests.get(f"{csfloatHistory}/{currentItem['item']['market_hash_name']}/sales",headers=header,params={"limit":5})).json()
    writeJsonToFile("latestSales.json",latestSales)
    highestBuyOrder = max((buyOrder["price"] if isinstance(buyOrder,dict) else 0.0001 for buyOrder in buyOrders),default=0)
    listingPrices = []
    if(isinstance(similarListings,list) and len(similarListings)>0):
        for j in range(len(similarListings)):
            if isinstance(similarListings[j], dict) and 'price' in similarListings[j]:
                listingPrices.append(similarListings[j]['price'])
            else:
                print(f"Skipping invalid entry at index {j}: {similarListings[j]}")
        if len(listingPrices) > 0:
            lowestListingPrice = min((listingPrice for listingPrice in listingPrices if similarListings[listingPrices.index(listingPrice)]['id'] != currentItem['id']), default=float("inf"))
        else:
            lowestListingPrice = float("inf") 
    else:
        lowestListingPrice=0    
    relative_price_profit = (lowestListingPrice-currentItem['price'])/currentItem['price']
    buy_order_sell_price_ratio = highestBuyOrder/currentItem['price']
    is_lowest_price = lowestListingPrice>currentItem['price']
    if isinstance(latestSales, list):
        filtered_sales = [sale['price'] for sale in latestSales[:8] if 'price' in sale]
        median_latest_sale = statistics.median(filtered_sales) if len(filtered_sales)>0 else 0
    else:
        median_latest_sale = 0
    is_lower_median_sale = currentItem['price']<=median_latest_sale
    return [relative_price_profit,buy_order_sell_price_ratio,is_lowest_price,is_lower_median_sale]
#Legg t logikk i "getCrazyCheap" som sjekker at et outputtet item faktisk er den billigste av den typen på markedet.
def writeJsonToFile(filename,data):
    with open(filename,mode='w') as file:
        json.dump(data,file,indent=4)

def getCrazyCheap():
        items = []
        response = requests.get(csfloatAPIlink,headers=header,params={"sort_by":"most_recent","min_ref_qty":20,"category":0,"type":"buy_now","max_price":165000})
        jsonData = response.json()
        for i in range(len(jsonData['data'])):
            currentItem = jsonData['data'][i]
            
            stickerPrice = sum([sticker.get("reference",{}).get("price",0) for sticker in currentItem["item"].get("stickers",[])])

            if currentItem['reference']['base_price'] > currentItem['reference']['predicted_price']:
                if stickerPrice>0:
                        stickerPercentage = (currentItem['price']-currentItem['reference']['predicted_price'])/stickerPrice
                else:
                    stickerPercentage = 0

                if currentItem['price'] < currentItem['reference']['predicted_price']:
                    array = funcd(currentItem)
                    items.append({"Listing id":currentItem['id'],"Item name":currentItem['item']['market_hash_name'],"Profit margin":round(100*(1-currentItem['price']/currentItem['reference']['predicted_price']),3),"Lowest calculated price":currentItem['reference']['predicted_price'],"Sale price":currentItem['price'],"Sticker percentage":stickerPercentage,"Sticker price":stickerPrice,"Icon url":currentItem['item']['icon_url'],"def_index":currentItem['item']['def_index'],"paint_index":currentItem['item'].get('paint_index',0),"float_value":currentItem['item'].get('float_value',0),"is_stattrak":currentItem['item'].get('is_stattrak',0),"is_souvenir":currentItem['item'].get('is_souvenir',0),"sticker_index":currentItem['item'].get("sticker_index",0),"is_commodity":currentItem['item'].get('is_commodity',0),"keychain_index":currentItem['item'].get('keychain_index',0),"rarity":currentItem['item'].get('rarity',0),"relative_price_profit":array[0],"is_lowest_price":array[2],"is_lower_median_sale":array[3],"sellprice_buyorder_ratio":array[1],"paint_seed":currentItem['item'].get("paint_seed",0),"target":"sjekk"})
                elif stickerPrice > 0 and stickerPercentage< 0.1:
                    array = funcd(currentItem)
                    items.append({"Listing id":currentItem['id'],"Item name":currentItem['item']['market_hash_name'],"Profit margin":round(100*(1-currentItem['price']/currentItem['reference']['predicted_price']),3),"Lowest calculated price":currentItem['reference']['predicted_price'],"Sale price":currentItem['price'],"Sticker percentage":stickerPercentage,"Sticker price":stickerPrice,"Icon url":currentItem['item']['icon_url'],"def_index":currentItem['item']['def_index'],"paint_index":currentItem['item'].get('paint_index',0),"float_value":currentItem['item'].get('float_value',0),"is_stattrak":currentItem['item'].get('is_stattrak',0),"is_souvenir":currentItem['item'].get('is_souvenir',0),"sticker_index":currentItem['item'].get("sticker_index",0),"is_commodity":currentItem['item'].get('is_commodity',0),"keychain_index":currentItem['item'].get('keychain_index',0),"rarity":currentItem['item'].get('rarity',0),"relative_price_profit":array[0],"is_lowest_price":array[2],"is_lower_median_sale":array[3],"sellprice_buyorder_ratio":array[1],"paint_seed":currentItem['item'].get("paint_seed",0),"target":"sjekk"})                
            else:
                if stickerPrice>0:
                        stickerPercentage = (currentItem['price']-currentItem['reference']['base_price'])/stickerPrice
                else:
                    stickerPercentage = 0

                if currentItem['price'] < currentItem['reference']['base_price']:
                    array = funcd(currentItem)
                    items.append({"Listing id":currentItem['id'],"Item name":currentItem['item']['market_hash_name'],"Profit margin":round(100*(1-currentItem['price']/currentItem['reference']['base_price']),3),"Lowest calculated price":currentItem['reference']['base_price'],"Sale price":currentItem['price'],"Sticker percentage":stickerPercentage,"Sticker price":stickerPrice,"Icon url":currentItem['item']['icon_url'],"def_index":currentItem['item']['def_index'],"paint_index":currentItem['item'].get('paint_index',0),"float_value":currentItem['item'].get('float_value',0),"is_stattrak":currentItem['item'].get('is_stattrak',0),"is_souvenir":currentItem['item'].get('is_souvenir',0),"sticker_index":currentItem['item'].get("sticker_index",0),"is_commodity":currentItem['item'].get('is_commodity',0),"keychain_index":currentItem['item'].get('keychain_index',0),"rarity":currentItem['item'].get('rarity',0),"relative_price_profit":array[0],"is_lowest_price":array[2],"is_lower_median_sale":array[3],"sellprice_buyorder_ratio":array[1],"paint_seed":currentItem['item'].get("paint_seed",0),"target":"sjekk"})                
                elif stickerPrice > 0 and stickerPercentage< 0.1:
                    array = funcd(currentItem)
                    items.append({"Listing id":currentItem['id'],"Item name":currentItem['item']['market_hash_name'],"Profit margin":round(100*(1-currentItem['price']/currentItem['reference']['base_price']),3),"Lowest calculated price":currentItem['reference']['base_price'],"Sale price":currentItem['price'],"Sticker percentage":stickerPercentage,"Sticker price":stickerPrice,"Icon url":currentItem['item']['icon_url'],"def_index":currentItem['item']['def_index'],"paint_index":currentItem['item'].get('paint_index',0),"float_value":currentItem['item'].get('float_value',0),"is_stattrak":currentItem['item'].get('is_stattrak',0),"is_souvenir":currentItem['item'].get('is_souvenir',0),"sticker_index":currentItem['item'].get("sticker_index",0),"is_commodity":currentItem['item'].get('is_commodity',0),"keychain_index":currentItem['item'].get('keychain_index',0),"rarity":currentItem['item'].get('rarity',0),"relative_price_profit":array[0],"is_lowest_price":array[2],"is_lower_median_sale":array[3],"sellprice_buyorder_ratio":array[1],"paint_seed":currentItem['item'].get("paint_seed",0),"target":"sjekk"})                
    
        # responseBestDeal = requests.get(csfloatAPIlink,headers=header,params={"sort_by":"best_deal","category":0,"type":"buy_now","max_price":165000,"min_ref_qty":20})
        # jsonData2 = responseBestDeal.json()
        # for i in range(len(jsonData2['data'])):
        #     currentItem = jsonData2['data'][i]
        #     stickerPrice = sum([sticker.get("reference",{}).get("price",0)/100 for sticker in currentItem["item"].get("stickers",[])])
        #     if currentItem['reference']['base_price'] > currentItem['reference']['predicted_price']:
        #         if currentItem['price'] < currentItem['reference']['predicted_price']:
        #             if stickerPrice>0:
        #                 stickerPercentage = (currentItem['price']-currentItem['reference']['predicted_price'])/stickerPrice
        #             else:
        #                 stickerPercentage = 0
        #             items.append({"Listing id":currentItem['id'],"Item name":currentItem['item']['market_hash_name'],"Profit margin":round(100*(1-currentItem['price']/currentItem['reference']['predicted_price']),3),"Lowest calculated price":currentItem['reference']['predicted_price'],"Sale price":currentItem['price'],"Sticker percentage":stickerPercentage,"Sticker price":stickerPrice,"Icon url":currentItem['item']['icon_url'],"def_index":currentItem['item']['def_index'],"paint_index":currentItem['item'].get('paint_index',0),"float_value":currentItem['item'].get('float_value',0),"is_stattrak":currentItem['item'].get('is_stattrak',0),"is_souvenir":currentItem['item'].get('is_souvenir',0),"sticker_index":currentItem['item'].get("sticker_index",0),"is_commodity":currentItem['item'].get('is_commodity',0),"keychain_index":currentItem['item'].get('keychain_index',0),"rarity":currentItem['item'].get('rarity',0),"target":"sjekk"})
        #     else:
        #         if currentItem['price'] < currentItem['reference']['base_price']:
        #             if stickerPrice>0:
        #                 stickerPercentage = (currentItem['price']-currentItem['reference']['base_price'])/stickerPrice
        #             else:
        #                 stickerPercentage = 0
        #             items.append({"Listing id":currentItem['id'],"Item name":currentItem['item']['market_hash_name'],"Profit margin":round(100*(1-currentItem['price']/currentItem['reference']['base_price']),3),"Lowest calculated price":currentItem['reference']['base_price'],"Sale price":currentItem['price'],"Sticker percentage":stickerPercentage,"Sticker price":stickerPrice,"Icon url":currentItem['item']['icon_url'],"def_index":currentItem['item']['def_index'],"paint_index":currentItem['item'].get('paint_index',0),"float_value":currentItem['item'].get('float_value',0),"is_stattrak":currentItem['item'].get('is_stattrak',0),"is_souvenir":currentItem['item'].get('is_souvenir',0),"sticker_index":currentItem['item'].get("sticker_index",0),"is_commodity":currentItem['item'].get('is_commodity',0),"keychain_index":currentItem['item'].get('keychain_index',0),"rarity":currentItem['item'].get('rarity',0),"target":"sjekk"})


        return sorted(items,key=lambda d:d['Profit margin'],reverse=False)

# def getLowStickerPercentage():
#         items = []
#         response = requests.get(csfloatAPIlink,headers=header,params={"sort_by":"most_recent","category":1,"type":"buy_now","min_ref_qty":20,"max_price":165000})
#         jsonData = response.json()
#         for i in range(len(jsonData['data'])):
#             currentItem = jsonData['data'][i]
#             stickerPrice = sum([sticker.get("reference",{}).get("price",0)/100 for sticker in currentItem["item"].get("stickers",[])])
#             if stickerPrice>0:
#                 if currentItem['reference']['base_price'] > currentItem['reference']['predicted_price']:
#                     stickerPercentage = (currentItem['price']-currentItem['reference']['predicted_price'])/stickerPrice
#                     if stickerPercentage < 0.1:
#                          items.append({"Listing id":currentItem['id'],"Item name":currentItem['item']['market_hash_name'],"Profit margin":round(100*(1-currentItem['price']/currentItem['reference']['predicted_price']),3),"Lowest calculated price":currentItem['reference']['predicted_price'],"Sale price":currentItem['price'],"Sticker percentage":stickerPercentage,"Sticker price":stickerPrice,"Icon url":currentItem['item']['icon_url'],"def_index":currentItem['item']['def_index'],"paint_index":currentItem['item'].get('paint_index',0),"float_value":currentItem['item'].get('float_value',0),"is_stattrak":currentItem['item'].get('is_stattrak',0),"is_souvenir":currentItem['item'].get('is_souvenir',0),"sticker_index":currentItem['item'].get("sticker_index",0),"is_commodity":currentItem['item'].get('is_commodity',0),"keychain_index":currentItem['item'].get('keychain_index',0),"rarity":currentItem['item'].get('rarity',0),"target":"sjekk"})
#                 else:
#                     stickerPercentage = (currentItem['price']-currentItem['reference']['base_price'])/stickerPrice        
#                     if stickerPercentage < 0.1:
#                         items.append({"Listing id":currentItem['id'],"Item name":currentItem['item']['market_hash_name'],"Profit margin":round(100*(1-currentItem['price']/currentItem['reference']['base_price']),3),"Lowest calculated price":currentItem['reference']['base_price'],"Sale price":currentItem['price'],"Sticker percentage":stickerPercentage,"Sticker price":stickerPrice,"Icon url":currentItem['item']['icon_url'],"def_index":currentItem['item']['def_index'],"paint_index":currentItem['item'].get('paint_index',0),"float_value":currentItem['item'].get('float_value',0),"is_stattrak":currentItem['item'].get('is_stattrak',0),"is_souvenir":currentItem['item'].get('is_souvenir',0),"sticker_index":currentItem['item'].get("sticker_index",0),"is_commodity":currentItem['item'].get('is_commodity',0),"keychain_index":currentItem['item'].get('keychain_index',0),"rarity":currentItem['item'].get('rarity',0),"target":"sjekk"})
        
#         responseStattrack = requests.get(csfloatAPIlink,headers=header,params={"sort_by":"most_recent","category":2,"type":"buy_now","min_ref_qty":20,"max_price":165000})
#         jsonData2 = responseStattrack.json()
#         for i in range(len(jsonData2['data'])):
#             currentItem = jsonData2['data'][i]
#             stickerPrice = sum([sticker.get("reference",{}).get("price",0)/100 for sticker in currentItem["item"].get("stickers",[])])
#             if stickerPrice>0:
#                 if currentItem['reference']['base_price'] > currentItem['reference']['predicted_price']:
#                     stickerPercentage = (currentItem['price']-currentItem['reference']['predicted_price'])/stickerPrice
#                     if stickerPercentage < 0.1:
#                          items.append({"Listing id":currentItem['id'],"Item name":currentItem['item']['market_hash_name'],"Profit margin":round(100*(1-currentItem['price']/currentItem['reference']['predicted_price']),3),"Lowest calculated price":currentItem['reference']['predicted_price'],"Sale price":currentItem['price'],"Sticker percentage":stickerPercentage,"Sticker price":stickerPrice,"Icon url":currentItem['item']['icon_url'],"def_index":currentItem['item']['def_index'],"paint_index":currentItem['item'].get('paint_index',0),"float_value":currentItem['item'].get('float_value',0),"is_stattrak":currentItem['item'].get('is_stattrak',0),"is_souvenir":currentItem['item'].get('is_souvenir',0),"sticker_index":currentItem['item'].get("sticker_index",0),"is_commodity":currentItem['item'].get('is_commodity',0),"keychain_index":currentItem['item'].get('keychain_index',0),"rarity":currentItem['item'].get('rarity',0),"target":"sjekk"})
#                 else:
#                     stickerPercentage = (currentItem['price']-currentItem['reference']['base_price'])/stickerPrice   
#                     if stickerPercentage < 0.1:
#                         items.append({"Listing id":currentItem['id'],"Item name":currentItem['item']['market_hash_name'],"Profit margin":round(100*(1-currentItem['price']/currentItem['reference']['base_price']),3),"Lowest calculated price":currentItem['reference']['base_price'],"Sale price":currentItem['price'],"Sticker percentage":stickerPercentage,"Sticker price":stickerPrice,"Icon url":currentItem['item']['icon_url'],"def_index":currentItem['item']['def_index'],"paint_index":currentItem['item'].get('paint_index',0),"float_value":currentItem['item'].get('float_value',0),"is_stattrak":currentItem['item'].get('is_stattrak',0),"is_souvenir":currentItem['item'].get('is_souvenir',0),"sticker_index":currentItem['item'].get("sticker_index",0),"is_commodity":currentItem['item'].get('is_commodity',0),"keychain_index":currentItem['item'].get('keychain_index',0),"rarity":currentItem['item'].get('rarity',0),"target":"sjekk"})

#         return sorted(items,key=lambda d:d['Profit margin'],reverse=False)

def timer(func1):
     while True:
        print("In while loop")
        func1()
        #func2()
        time.sleep(180) 

def sendToDiscord(item):
    webhook_url = 'https://discord.com/api/webhooks/1348735436876677341/ZCEz8_VAi23TXQUAVyUXHZE9AyiP-s8Vz9PdqzLvg8sblvoOC0p9i5hyUYgPYsy4Tx56'
    embeds =[{
        "title": f":fire: {item['Item name']} :fire:", 
        "description": f"Profit margin: **{item['Profit margin']}** \n [**LISTING**](https://csfloat.com/item/{item['Listing id']})",
        "color": 112712,
        "image":{"url":f"https://community.cloudflare.steamstatic.com/economy/image/{item['Icon url']}"}
        }]
    data = {
         "username":"csfloat scanner",
         "avatar_url":"https://imgur.com/gallery/incase-you-havent-seen-this-show-yet-NBEIFBz.png",
         "embeds":embeds
         }
    requests.post(webhook_url, json=data)
    

def checkNotDuplicateListing(item):
    listing_id = item["Listing id"]
    filename = "new_data.txt"
    id_found = -1
    with open(filename,mode="r") as file:
        entireFile = file.read()
        id_found = entireFile.find(listing_id)
        if id_found == -1:
            return True
        else:
            return False
     
def runShi():
    #entries_to_remove = ('target', 'Listing id', 'Item name', 'Icon url')
    cheapItems = getCrazyCheap()
    pprint.pprint(cheapItems)
    # Save to a CSV file
    filename = "new_data.txt"  # You can use .csv as well
    if(len(cheapItems))>0:
        with open(filename, mode="a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=cheapItems[0].keys())
            for item in cheapItems:
                if(checkNotDuplicateListing(item)):
                    #writer.writeheader()  # Write column names
                    writer.writerow(item)  # Write row
                    sendToDiscord(item)
                    #editItem = item.copy()
                    #for k in entries_to_remove:
                    #    editItem.pop(k, None)
                    #df = pd.DataFrame([editItem])
                    #prediction = loaded_model.predict(df)
                    #if(prediction[0]>0.5):
                    #    print(f"Prediction for buying {item['Item name']}: ", prediction)
                    #    sendToDiscord(item)
                   # else:
                   #     print(f"Prediction for buying {item['Item name']}: ", prediction)
    

# def runShi2():
#     entries_to_remove = ('target', 'Listing id', 'Item name', 'Icon url')
#     cheapStickeredItems = getLowStickerPercentage()
#     pprint.pprint(cheapStickeredItems)
#     filename = "data.txt"  # You can use .csv as well
#     if(len(cheapStickeredItems))>0:
#         with open(filename, mode="a", newline="") as file:
#             writer = csv.DictWriter(file, fieldnames=cheapStickeredItems[0].keys())
#             for item in cheapStickeredItems:
#                 if(checkNotDuplicateListing(item)):
#                     #writer.writeheader()  # Write column names
#                     writer.writerow(item)  # Write rows
#                     editItem = item.copy()
#                     for k in entries_to_remove:
#                         editItem.pop(k, None)
#                     df = pd.DataFrame([editItem])
#                     prediction = loaded_model.predict(df)
#                     if(prediction[0]>0.5):
#                         print(f"Prediction for buying {item['Item name']}: ", prediction)
#                         sendToDiscord(item)
#                     else:
#                         print(f"Prediction for buying {item['Item name']}: ", prediction)

t = threading.Thread(target=timer,args=(runShi,))
t.start()



