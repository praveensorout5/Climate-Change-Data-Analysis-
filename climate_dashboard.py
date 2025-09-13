import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import os

st.set_page_config(page_title="Global Climate Dashboard", layout="wide")
st.title("🌍 Global Climate Dashboard")

# -------------------------
# 1. Load CSV
# -------------------------
@st.cache_data
def load_data(path="sample_climate_data.csv"):
    if not os.path.exists(path):
        st.error(f"CSV file not found: {path}")
        return None
    
    df = pd.read_csv(path)
    
    # Ensure Year column is numeric
    if 'Year' not in df.columns:
        st.error("CSV must contain a 'Year' column")
        return None
    
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
    df = df.dropna(subset=['Year'])
    df['Year'] = df['Year'].astype(int)
    
    # Convert all other columns to numeric if possible
    for col in df.columns:
        if col != "Year" and col != "Country":
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    return df

data = load_data()
if data is None:
    st.stop()

st.write("Sample data preview:")
st.dataframe(data.head())

# -------------------------
# 2. Sidebar Filters
# -------------------------
st.sidebar.header("Filters")

# Year range
year_range = st.sidebar.slider(
    "Select Year Range",
    int(data['Year'].min()),
    int(data['Year'].max()),
    (int(data['Year'].min()), int(data['Year'].max()))
)
filtered_data = data[(data['Year'] >= year_range[0]) & (data['Year'] <= year_range[1])]

# Country selection
countries = st.sidebar.multiselect(
    "Select Countries",
    options=filtered_data["Country"].unique(),
    default=filtered_data["Country"].unique()
)
filtered_data = filtered_data[filtered_data["Country"].isin(countries)]

# -------------------------
# 3. Metric Selection
# -------------------------
numeric_cols = filtered_data.select_dtypes(include=np.number).columns.tolist()
numeric_cols = [col for col in numeric_cols if col != "Year"]

if not numeric_cols:
    st.warning("No numeric columns available for plotting.")
    st.stop()

selected_metric = st.sidebar.selectbox(
    "Select Metric to Plot",
    options=numeric_cols
)

# -------------------------
# 4. Line Chart
# -------------------------
st.subheader(f"Line Chart: {selected_metric} over Years")
fig_line = px.line(
    filtered_data,
    x="Year",
    y=selected_metric,
    color="Country",
    markers=True,
    title=f"{selected_metric} over Years"
)
st.plotly_chart(fig_line, use_container_width=True)

# -------------------------
# 5. Scatter Plot
# -------------------------
st.subheader(f"Scatter Plot: {selected_metric} vs Year")
fig_scatter = px.scatter(
    filtered_data,
    x="Year",
    y=selected_metric,
    color="Country",
    size=selected_metric,
    hover_data=["Country"],
    title=f"{selected_metric} Scatter Plot"
)
st.plotly_chart(fig_scatter, use_container_width=True)
