import requests
class Skin:
    csfloatAPIlink = "https://csfloat.com/api/v1/listings"
    
    with open("api_key.txt","r") as f:
        api_key = f.readline()

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
             #.get for dictionaries returns the value after comma if the key does not exist. This is good for avoiding KeyError in terminal.
        return items
    
    def getCheapest(self,maxPrice):
        itemList = self.getPrices()
        updatedList = []

        for i in range(len(itemList)):
            if itemList[i]["Price"] < maxPrice:
                updatedList.append(itemList[i])

        self.cheapestItems = sorted(updatedList,key=lambda d:d["Price"]) #Sort array by price by using lambda function. Basically updatedList['price']


    #Make method to return items cheaper than recommended
    def getCrazyCheap(self):
        items = []
        response = requests.get(Skin.csfloatAPIlink,headers=Skin.header,params={"type":"buy_now","max_price":165000})
        jsonData = response.json()

        for i in range(len(jsonData['data'])):
            currentItem = jsonData['data'][i]
            if currentItem['price'] < currentItem['reference']['predicted_price']:
                items.append({"Listing id":currentItem['id'],"Item name":currentItem['item']['market_hash_name'],"Profit after fee":(-currentItem['price']+currentItem['reference']['predicted_price'])*0.98})