from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

sns.set_theme(style="whitegrid")
st.set_page_config(page_title="Kualitas Udara Beijing", page_icon="🌫️", layout="wide")

DATA_PATH = Path(__file__).parent / "main_data.csv"
CATEGORY_ORDER = ["Baik", "Sedang", "Tidak Sehat (Sensitif)", "Tidak Sehat", "Sangat Tidak Sehat", "Berbahaya"]
WD_ORDER = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]


@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH, parse_dates=["date"])


df = load_data()

# Sidebar filter
st.sidebar.header("Filter")
min_date, max_date = df["date"].min().date(), df["date"].max().date()
date_range = st.sidebar.date_input("Rentang tanggal", (min_date, max_date), min_value=min_date, max_value=max_date)
stations = st.sidebar.multiselect("Stasiun", sorted(df["station"].unique()), default=sorted(df["station"].unique()))

if len(date_range) != 2 or not stations:
    st.warning("Pilih rentang tanggal (awal dan akhir) dan minimal satu stasiun.")
    st.stop()

start, end = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])
data = df[df["date"].between(start, end) & df["station"].isin(stations)]
if data.empty:
    st.warning("Tidak ada data untuk filter yang dipilih.")
    st.stop()

st.title("🌫️ Dashboard Kualitas Udara Beijing")
st.caption("Data PRSA 12 stasiun pemantau, Maret 2013 – Februari 2017 (agregasi harian).")

# Ringkasan
worst = data.groupby("station")["PM25"].mean().idxmax()
unhealthy_share = (data["PM25"] > 55.4).mean() * 100
c1, c2, c3, c4 = st.columns(4)
c1.metric("Rata-rata PM2.5", f"{data['PM25'].mean():.1f} µg/m³")
c2.metric("PM2.5 harian maksimum", f"{data['PM25'].max():.0f} µg/m³")
c3.metric("Hari tidak sehat (>55,4)", f"{unhealthy_share:.1f}%")
c4.metric("Stasiun paling tercemar", worst)

tab1, tab2 = st.tabs(["Tren & Stasiun", "Pengaruh Cuaca"])

with tab1:
    st.subheader("Tren PM2.5 bulanan")
    monthly = data.set_index("date")["PM25"].resample("MS").mean()
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.plot(monthly.index, monthly.values, color="#c0392b", marker="o", markersize=3)
    ax.set_ylabel("PM2.5 (µg/m³)")
    ax.set_xlabel(None)
    st.pyplot(fig)

    left, right = st.columns(2)
    with left:
        st.subheader("Pola musiman (per bulan)")
        by_month = data.groupby("month")["PM25"].mean().reindex(range(1, 13))
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.bar(by_month.index, by_month.values, color=sns.color_palette("RdYlBu_r", 12))
        ax.set_xticks(range(1, 13))
        ax.set_xlabel("Bulan")
        ax.set_ylabel("PM2.5 (µg/m³)")
        st.pyplot(fig)
    with right:
        st.subheader("Rata-rata PM2.5 per stasiun")
        by_station = data.groupby("station")["PM25"].mean().sort_values(ascending=False)
        colors = ["#c0392b" if i < 3 else "#bdc3c7" for i in range(len(by_station))]
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.barplot(x=by_station.values, y=by_station.index, hue=by_station.index, palette=colors, legend=False, ax=ax)
        ax.set_xlabel("PM2.5 (µg/m³)")
        ax.set_ylabel(None)
        st.pyplot(fig)

    st.subheader("Proporsi hari menurut kategori PM2.5")
    cat = data["pm25_category"].value_counts(normalize=True).reindex(CATEGORY_ORDER).fillna(0) * 100
    fig, ax = plt.subplots(figsize=(12, 3))
    ax.barh(cat.index[::-1], cat.values[::-1], color=sns.color_palette("RdYlGn_r", len(cat))[::-1])
    ax.set_xlabel("Persentase hari-stasiun (%)")
    st.pyplot(fig)

with tab2:
    st.subheader("Korelasi cuaca dengan PM2.5")
    cols = ["TEMP", "PRES", "DEWP", "RAIN", "WSPM", "PM25"]
    corr = data[cols].corr(method="spearman")
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="RdBu_r", center=0, ax=ax)
    st.pyplot(fig)

    left, right = st.columns(2)
    with left:
        st.subheader("PM2.5 menurut kecepatan angin")
        wind_bin = pd.cut(data["WSPM"], bins=[-0.01, 1, 2, 3, 5, float("inf")], labels=["0-1", "1-2", "2-3", "3-5", ">5"])
        wind_pm = data.groupby(wind_bin, observed=True)["PM25"].mean()
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.bar(wind_pm.index.astype(str), wind_pm.values, color="#2980b9")
        ax.set_xlabel("Kecepatan angin (m/s)")
        ax.set_ylabel("PM2.5 (µg/m³)")
        st.pyplot(fig)
    with right:
        st.subheader("PM2.5 menurut arah angin")
        wd_pm = data.groupby("wd")["PM25"].mean().reindex(WD_ORDER)
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.barplot(x=wd_pm.index, y=wd_pm.values, color="#8e44ad", ax=ax)
        ax.set_xlabel("Arah angin")
        ax.set_ylabel("PM2.5 (µg/m³)")
        plt.setp(ax.get_xticklabels(), rotation=60)
        st.pyplot(fig)

    st.subheader("Hujan vs tidak hujan")
    rain_pm = data.assign(status=data["RAIN"].gt(0).map({True: "Hujan", False: "Tidak hujan"})).groupby("status")["PM25"].mean()
    st.bar_chart(rain_pm)
