import streamlit as st
import pandas as pd
import requests

st.title("Batter vs Pitcher (BvP) Matchups")
st.write("**Criteria:** AVG ≥ .200 and Minimum 5 AB")

# Example: SwishAnalytics URL (replace with your actual)
swish_url = "https://www.swishanalytics.com/mlb/batter-vs-pitcher-matchups"

# Example: RotoWire URL (replace with your actual)
rotowire_url = "https://www.rotowire.com/baseball/daily-lineups.php"

# Function to load and filter tables
def load_bvp_table(url):
    try:
        tables = pd.read_html(url)
        df = tables[0]
        # Rename columns if needed for uniformity
        df.columns = [col.strip() for col in df.columns]
        # Filter: AB ≥ 5 and AVG ≥ .200 if columns exist
        if "AB" in df.columns and "AVG" in df.columns:
            df = df[(df["AB"] >= 5) & (df["AVG"] >= 0.200)]
        return df
    except Exception as e:
        st.error(f"Failed to scrape {url}: {e}")
        return pd.DataFrame()

swish_df = load_bvp_table(swish_url)
rotowire_df = load_bvp_table(rotowire_url)

if not swish_df.empty:
    st.subheader("SwishAnalytics BvP Matchups")
    st.dataframe(swish_df)

if not rotowire_df.empty:
    st.subheader("RotoWire BvP Matchups")
    st.dataframe(rotowire_df)

if swish_df.empty and rotowire_df.empty:
    st.warning("No BvP matchups available or scraping blocked today.")
