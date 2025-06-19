import pandas as pd



def enhance_data():
    # Load your existing classified data
    df = pd.read_csv("output/classified_stores.csv")  
    
    # 1. Clean size_sqrt (example: divide by 1e9 to get realistic sqft)
    df["size_sqrt"] = df["size_sqrt"] / 1_000_000_000  # Converts to "sqft in billions"
    
    # 2. Add profitability scores
    profitability_scores = {
        "bulk wholesale": 3,
        "Discount": 1,
        "Organic": 5  # (Add if present in your data)
    }
    df["profit_score"] = df["store_type"].map(profitability_scores)
    
    # 3. Add insights
    insights = {
        "bulk wholesale": "🚛 Compete with bulk-order discounts",
        "Discount": "💸 Monitor their weekly promotions",
        "Organic": "🌱 Highlight your local/organic partnerships"  # (Add if present)
    }
    df["insight"] = df["store_type"].map(insights)
    
    # Save enhanced data
    df.to_csv("output/enhanced_stores.csv", index=False)
    print("✅ Saved enhanced_stores.csv with scores + insights")

enhance_data()