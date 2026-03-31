import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Changping Air Quality Dashboard", layout="wide")

# Load data hasil cleaning
@st.cache_data
def load_data():
    df = pd.read_csv("main_data.csv")
    df['datetime'] = pd.to_datetime(df['datetime'])
    # Re-apply binning for dashboard
    bins = [0, 35, 75, 150, df['PM2.5'].max()]
    labels = ['Baik', 'Sedang', 'Tidak Sehat', 'Berbahaya']
    df['Kategori_Udara'] = pd.cut(df['PM2.5'], bins=bins, labels=labels, include_lowest=True)
    return df

df = load_data()

# Sidebar
st.sidebar.title("Filter Data")
year_list = df['year'].unique().tolist()
selected_year = st.sidebar.selectbox("Pilih Tahun", year_list)

# Filter data
filtered_df = df[df['year'] == selected_year]

# Main Area
st.title(f"☁️ Dashboard Kualitas Udara Changping ({selected_year})")

# Metrik Utama
col1, col2, col3 = st.columns(3)
col1.metric("Rata-rata PM2.5", f"{filtered_df['PM2.5'].mean():.2f} µg/m³")
col2.metric("Suhu Rata-rata", f"{filtered_df['TEMP'].mean():.2f} °C")
col3.metric("Total Curah Hujan", f"{filtered_df['RAIN'].sum():.2f} mm")

st.markdown("---")

# Row 1 Charts
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("Tren Rata-Rata PM2.5 per Bulan")
    monthly_trend = filtered_df.groupby('month')['PM2.5'].mean()
    fig1, ax1 = plt.subplots(figsize=(8, 5))
    sns.lineplot(x=monthly_trend.index, y=monthly_trend.values, marker='o', color='crimson', ax=ax1)
    ax1.set_xticks(range(1, 13))
    ax1.set_xlabel("Bulan")
    ax1.set_ylabel("PM2.5")
    st.pyplot(fig1)

with col_chart2:
    st.subheader("Distribusi Kategori Kualitas Udara (Binning)")
    kat_counts = filtered_df['Kategori_Udara'].value_counts().reset_index()
    kat_counts.columns = ['Kategori', 'Jumlah']
    fig2, ax2 = plt.subplots(figsize=(8, 5))
    colors = ['#2ecc71', '#f1c40f', '#e67e22', '#e74c3c']
    sns.barplot(data=kat_counts, x='Kategori', y='Jumlah', palette=colors, ax=ax2)
    ax2.set_xlabel("Kategori")
    ax2.set_ylabel("Jumlah Jam")
    st.pyplot(fig2)

st.caption("Hak Cipta © Proyek Analisis Data - Dicoding 2024")