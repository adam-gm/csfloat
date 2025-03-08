import requests
import skinclass
#api key csfloat: Rd3UmYDMXvJlqwueoFJoaI11rpyuOHgv

#all listings: https://csfloat.com/api/v1/listings
#specific listing: https://csfloat.com/api/v1/listings/<ID>


desertHydraParameters={
    "market_hash_name": "AWP | Desert Hydra (Field-Tested)",
    "category": 1,
    "sort_by": "most_recent",
    "type": "buy_now",
    "state": "listed",
    "max_float": 0.27,
    "max_price": 185000,
}

desertHydra = skinclass.Skin(desertHydraParameters)
desertHydra.getCheapest(1650)
# response = requests.get("https://csfloat.com/api/v1/listings",headers=header,params=parameters)
# jsonData = response.json()

#heapHydras = []

# for i in range(len(jsonData["data"])):
#     dataPoint = jsonData["data"][i]
#     print("AWP Desert Hydra price: ",dataPoint["price"]/100," USD","Listing id:",dataPoint["id"],"Stickers applied: ",[sticker["name"] for sticker in dataPoint["item"].get("stickers",[])])
#     if(dataPoint["price"]/100 < 1650):
#         cheapHydras.append({"id": dataPoint["id"],"price": dataPoint["price"]/100,"Stickers":[sticker["name"] for sticker in dataPoint["item"].get("stickers",[])],"Float value": dataPoint["item"]["float_value"]})
# #.get for dictionaries returns the value after comma if the key does not exist. This is good for avoiding KeyError in terminal.
# print("Cheap hydras: ", sorted(cheapHydras,key=lambda d:d["price"])) #Sort array by AWP price. Basically cheapHydras['price']


