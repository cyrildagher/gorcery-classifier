import pandas as pd 

#load data 
df = pd.read_csv("data/stores.csv")

#define classification rules 
def classify_store(row): 
    if "organic" in row ["product_types"].lower(): 
        return "organic"
    elif "bulk" in row ["product_types"].lower() and row["size_sqrt"] > 3000: 
        return "bulk_wholesale"
    elif row["pricing_model"] == "discount" : 
        return "discount" 
    else: 
        return "General Retail"
    
profitability_score = {
    "organic" : 5, #Highest priority 
    "Bulk Wholesale" : 3, 
    "Discount" : 1, 
    "General Retail" : 2
}
    
#apply classification 
df ["store_type"] = df.apply(classify_store, axis=1)

#save results 
df.to_csv("output/classified_stores.csv", index=False)
print("✅ classification complete! Saved to output/classified_stores.csv")



# Generate insights 
insights = {
    "organic" : "Competes on quality -> Price premium products strategically", 
    "Bulk Wholesale" : "Competes on Volume -> Offer bundle deals", 
    "Discount" : "Price-sensitive -> Natch / undercut key items"
}

df["Insights"] = df["store_type"].map(insights)

#save with insights 
df.to_csv("Output/classified_stores_with_insights.csv", index=False)