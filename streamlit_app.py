import pandas as pd
import numpy as np
import streamlit as st
import yfinance as yf

import datetime as dt

liste={
    "BTC":"BTC-USD",
    "ETH":"ETH-USD",
    "XRP":"XRP-USD",
    "SHIB":"SHIB-USD"
}

sec=st.sidebar.selectbox("KriptoPara",liste.keys())
ticker=liste.get(sec)

def veri(ticker,baslangic="2004-01-01",bitis=dt.datetime.today().date()):
    df=yf.download(ticker,baslangic,bitis)
    df=df['Close']
    st.line_chart(df)


col1,col2,col3=st.columns(3)
with col1:
    son30 = st.button("30Gün")
with col2:
    son90 = st.button("90Gün")
with col3:
    son360 = st.button("Yıl")

bugun=dt.datetime.today().date()


if son30:
    baslangic=bugun-dt.timedelta(days=30)
    bitis=bugun
elif son90:
    baslangic = bugun - dt.timedelta(days=90)
    bitis = bugun
elif son360:
    baslangic = bugun - dt.timedelta(days=365)
    bitis = bugun
else:
    baslangic = "2004-01-01"
    bitis = bugun

veri(ticker,baslangic,bitis)
