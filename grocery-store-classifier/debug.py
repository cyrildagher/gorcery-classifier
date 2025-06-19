import pandas as pd 

df = pd.read_csv("data/stores.csv")
print("colums in your csv:", list(df.columns))