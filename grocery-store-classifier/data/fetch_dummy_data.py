import pandas as pd 
import requests 

# fetch 10 fake stores from faker API 
response = requests.get("https://fakerapi.it/api/v1/companies?_quantity=10")
data = response.json()["data"]

#customize fields(matching grocery store needs)
stores = [] 
for store in data: 
    stores.append ({
        "name" : store["name"], 
        "product_types": "organic,local" if "organic" in store["name"].lower() else "bulk.discount", #fake rule
        "pricing_model": "premium" if store["vat"].startswith("BE") else "discount", 
        "size_sqrt": int(store["phone"].split("-")[0])* 100, 
        "location": store["country"], 
    })

#SAVE TO CSV 
df = pd.DataFrame(stores)
df.to_csv("data/stores.csv", index=False)
print("✅ Dummy data saved to data/stores.csv")