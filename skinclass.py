import requests
class Skin:
    csfloatAPIlink = "https://csfloat.com/api/v1/listings"
    api_key="Rd3UmYDMXvJlqwueoFJoaI11rpyuOHgv"
    header={
    "Authorization": api_key
    }

    def __init__(self,parameters):
        self.parameters = parameters
    
    def getPrices(self):
        items = []
        response = requests.get(Skin.csfloatAPIlink,headers=Skin.header,params=self.parameters)
        jsonData = response.json()

        for i in range(len(jsonData["data"])):
            dataPoint = jsonData["data"][i]
            #print(dataPoint["item"]["market_hash_name"] ,"Price: ",dataPoint["price"]/100," USD","Listing id:",dataPoint["id"],"Stickers applied: ",[sticker["name"] for sticker in dataPoint["item"].get("stickers",[])])
            items.append({"Item": dataPoint["item"]["market_hash_name"],"Price": dataPoint["price"]/100,"Listing id":dataPoint["id"],"Stickers applied": [sticker["name"] for sticker in dataPoint["item"].get("stickers",[])]})
        return items
    
    def getCheapest(self,maxPrice):
        itemList = self.getPrices()
        updatedList = []

        for i in range(len(itemList)):
            if itemList[i]["Price"] < maxPrice:
                updatedList.append(itemList[i])

        sortedItems = sorted(updatedList,key=lambda d:d["Price"])
        print(sortedItems)
        return sortedItems
