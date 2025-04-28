import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load Cleaned Data
yearly = pd.read_csv("Cleaned_data.csv")

# KPI Metrics
total_consumption = yearly['Total Primary Energy Consumption'].sum()
total_production = yearly['Total Primary Energy Production'].sum()
self_sufficiency_ratio = total_production / total_consumption

# Streamlit App
st.title("World Energy Overview Dashboard - Cleaned Data")

# Metrics Cards
col1, col2, col3 = st.columns(3)
col1.metric("Total Production", f"{total_production:.2f}")
col2.metric("Total Consumption", f"{total_consumption:.2f}")
col3.metric("Self Sufficiency Ratio", f"{self_sufficiency_ratio:.2f}")

# Sidebar filter
year_range = st.sidebar.slider('Select Year Range', int(yearly['Year'].min()), int(yearly['Year'].max()), (yearly['Year'].min(), yearly['Year'].max()))
filtered = yearly[(yearly['Year'] >= year_range[0]) & (yearly['Year'] <= year_range[1])]

# Tabs for 4 Pilar Visualisasi
tab1, tab2, tab3, tab4 = st.tabs(["Distribution", "Composition", "Relationship", "Comparison"])

with tab1:
    st.subheader("Distribution of Total Primary Energy Consumption")
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=filtered, x='Year', y='Total Primary Energy Consumption', color='royalblue')
    plt.title("Distribusi Konsumsi Energi Utama per Tahun")
    plt.ylabel("Konsumsi Energi (EJ)")
    plt.xlabel("Tahun")
    plt.grid(True)
    st.pyplot(plt)

with tab2:
    st.subheader("Composition of Energy Production")
    plt.figure(figsize=(14, 6))
    plt.stackplot(
        filtered['Year'],
        filtered['Total Fossil Fuels Production'],
        filtered['Nuclear Electric Power Production'],
        filtered['Total Renewable Energy Production'],
        labels=['Fosil', 'Nuklir', 'Terbarukan'],
        colors=['#d95f02', '#7570b3', '#1b9e77']
    )
    plt.legend(loc='upper left')
    plt.title("Komposisi Produksi Energi per Tahun")
    plt.ylabel("Produksi Energi (EJ)")
    plt.xlabel("Tahun")
    plt.grid(True)
    st.pyplot(plt)

with tab3:
    st.subheader("Relationship between Production and Consumption")
    plt.figure(figsize=(10, 6))
    sns.regplot(
        data=filtered,
        x='Total Primary Energy Production',
        y='Total Primary Energy Consumption',
        scatter_kws={'s': 60, 'color': '#2c7bb6'},
        line_kws={'color': '#d7191c'}
    )
    plt.title("Korelasi Produksi vs Konsumsi Energi")
    plt.xlabel("Produksi Energi (EJ)")
    plt.ylabel("Konsumsi Energi (EJ)")
    plt.grid(True)
    st.pyplot(plt)

with tab4:
    st.subheader("Comparison of Production vs Consumption")
    plt.figure(figsize=(14, 6))
    plt.plot(filtered['Year'], filtered['Total Primary Energy Production'], label='Produksi', color='#1b9e77', linewidth=2.5)
    plt.plot(filtered['Year'], filtered['Total Primary Energy Consumption'], label='Konsumsi', color='#d95f02', linewidth=2.5)
    plt.fill_between(
        filtered['Year'],
        filtered['Total Primary Energy Production'],
        filtered['Total Primary Energy Consumption'],
        where=(filtered['Total Primary Energy Consumption'] > filtered['Total Primary Energy Production']),
        color='lightcoral',
        alpha=0.3,
        label='Defisit Energi'
    )
    plt.title("Perbandingan Produksi vs Konsumsi Energi")
    plt.xlabel("Tahun")
    plt.ylabel("Energi (EJ)")
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)
