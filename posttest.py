import requests
csfloatAPIlink = "https://csfloat.com/api/v1/listings/buy"

with open("api_key.txt","r") as f:
        api_key = f.readline()

header={
    "Authorization": api_key,
    "Content-Type": "application/json"
    }

response = requests.post(csfloatAPIlink,headers=header,json={"total_price":14,'contract_ids':['819569039931213619']})
print(response)

