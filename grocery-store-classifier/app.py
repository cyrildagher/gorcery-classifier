import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configure style
plt.style.use('ggplot')
sns.set_palette("pastel")

# Load data
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("output/enhanced_stores.csv")
        df["size_million"] = df["size_sqrt"] / 1_000_000
        return df
    except FileNotFoundError:
        st.error("Data file not found. Please run report_generator.py first.")
        st.stop()

df = load_data()

# ===== Dashboard Layout =====
st.title("🛒 Grocery Store Intelligence Portal")

# Main Content
analysis_tab, insights_tab = st.tabs(["Competitor Analysis", "Strategic Insights"])

with analysis_tab:
    st.header("Competitor Breakdown")
    
    # Competitor Distribution
    st.subheader("1. Market Presence")
    fig1, ax1 = plt.subplots(figsize=(10, 4))
    sns.countplot(data=df, y="store_type", order=df["store_type"].value_counts().index)
    plt.xlabel("Number of Stores")
    plt.ylabel("")
    st.pyplot(fig1)
    st.markdown("""
    **What this shows:**  
    → Which competitor types dominate your market  
    → Relative market share of different store formats  
    → Identifies most common competition
    """)
    
    # Size Comparison
    st.subheader("2. Size Comparison")
    fig2, ax2 = plt.subplots(figsize=(10, 4))
    sns.boxplot(data=df, x="store_type", y="size_million")
    plt.ylabel("Size (M sqft)")
    plt.xlabel("")
    st.pyplot(fig2)
    st.markdown("""
    **Key takeaways:**  
    → Shows typical store sizes for each competitor type  
    → Identifies outliers (very large/small stores)  
    → Helps plan space optimization strategies
    """)


with insights_tab:
    st.header("Actionable Strategies")
    
    # Filter Section
    st.subheader("Filter Competitors")
    col1, col2, = st.columns(2)
    with col1:
        selected_type = st.selectbox(
            "Store Type",
            options=["All"] + list(df["store_type"].unique()))
    with col2:
        selected_country = st.selectbox(
            "Country",
            options=["All"] + list(df["location"].unique()))
    
    # Apply filters
    filtered_df = df.copy()
    if selected_type != "All":
        filtered_df = filtered_df[filtered_df["store_type"] == selected_type]
    if selected_country != "All":
        filtered_df = filtered_df[filtered_df["location"] == selected_country]


        
    # Insights Table
    st.subheader("Recommended Actions")
    if not filtered_df.empty:
        insights = {
            "bulk wholesale": [
                "📦 Create bulk-buyer membership program",
                "🔄 Allocate 20% more shelf space to bulk items",
                "💰 Offer 5% discount on bulk purchases over $200"
            ],
            "Discount": [
                "💲 Introduce loss leaders near competitor locations",
                "🎯 Highlight premium quality in weekly ads",
                "🛒 Bundle complementary discount items"
            ],
            "Organic": [
                "🌱 Partner with local organic farms",
                "🥬 Expand organic produce section by 15%",
                "📢 Feature farm-to-table stories in marketing"
            ]
        }
        
        # Show appropriate insights
        st.markdown(f"### {selected_type if selected_type != 'All' else 'General'} Strategies")
        for strategy in insights.get(
            selected_type.lower() if selected_type != "All" else "bulk wholesale", 
            ["Select specific competitor type for tailored strategies"]
        ):
            st.info(f"• {strategy}")
        
        # Competitor Details
        st.subheader("Competitor Details")
        st.dataframe(
            filtered_df[["name", "location", "store_type", "size_million"]],
            column_config={
                "size_million": st.column_config.NumberColumn("Size (M sqft)", format="%.1f")
            },
            hide_index=True,
            use_container_width=True
        )
    else:
        st.warning("No stores match your filters")

# Footer
st.markdown("---")
st.caption("Data last updated: " + pd.Timestamp.now().strftime("%Y-%m-%d"))
st.caption ("Property of KRYL")