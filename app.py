import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="MLB BvP Matchups", layout="wide")

st.title("⚾ MLB Batter vs Pitcher Matchups (BvP)")

st.markdown("""
**Hitters Criteria:**  
- Batting Avg ≥ .200 vs Pitcher  
- Min 5 AB  
""")

# -------------------------
# Scraper Function
# -------------------------
def scrape_bvp():
    """
    Scrape BvP stats from SwishAnalytics.
    This is a simplified example; we can adjust once the final URL is confirmed.
    """
    url = "https://swishanalytics.com/optimus/mlb/batter-vs-pitcher-stats"  # Update if needed
    resp = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(resp.text, "html.parser")

    # Look for all tables in page
    tables = pd.read_html(str(soup))
    if not tables:
        return pd.DataFrame(columns=["Batter", "Pitcher", "AB", "H", "XBH", "HR", "BB", "K", "AVG", "OBP", "SLG", "OPS"])

    # Assume first table is our BvP table
    df = tables[0]

    # Rename columns if needed
    df.columns = [c.strip() for c in df.columns]

    # Filter based on criteria
    if 'AB' in df.columns and 'AVG' in df.columns:
        df = df[(df['AB'] >= 5) & (df['AVG'] >= 0.200)]

    return df.reset_index(drop=True)

# -------------------------
# Load Data
# -------------------------
with st.spinner("Scraping BvP data..."):
    bvp_df = scrape_bvp()

if bvp_df.empty:
    st.error("No data found. Check source URL or adjust scraping logic.")
else:
    st.dataframe(bvp_df, use_container_width=True)

st.caption("Data from SwishAnalytics / RotoWire (for demonstration purposes)")
