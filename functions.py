
import pandas as pd
import numpy as np
from urllib.request import urlopen
import xml.etree.ElementTree as et
import urllib

import sqlite3
import datetime




def newsroot(link):
    req = urllib.request.Request(link, headers={'User-Agent': "Magic Browser"})
    con = urllib.request.urlopen(req)
    xml = et.ElementTree(file=con)
    root = xml.getroot()
    return root


def gazeteoku(link):
    x = newsroot(link)
    x[0][1][2].tag
    ls = link.split("/")
    haber_rows = []
    for a in ls:
        if "www." in a or ".com" in a:
            haber_site = a
    for a in x.findall(x[0].tag):
        haber_link = a[0].text
        haber_tarih = a[1][1].text
        haber_baslik = a[1][2].text

        haber_row = {
            "haber_site": haber_site,
            "haber_link": haber_link,
            "haber_tarih": haber_tarih,
            "haber_baslik": haber_baslik
        }

        haber_rows.append(haber_row)

    return haber_rows





def dbTrendEkle():
    gun = str(datetime.date.today())
    trendler = trendgetir()
    conn = sqlite3.connect("haberasistan.sqlite3")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS trendler(kelime TEXT,tarih TEXT)")
    conn.commit()
    say = 0
    for kelime in trendler:
        c.execute("SELECT * FROM trendler WHERE kelime=? AND tarih=?", (kelime, gun))
        degerler = c.fetchall()
        if len(degerler) == 0:
            c.execute("INSERT INTO trendler VALUES(?,?)", (kelime, gun))
            conn.commit()
            say = say + 1

    return say


def habergetir():
    conn = sqlite3.connect("haberasistan.sqlite3")
    c = conn.cursor()
    c.execute("SELECT * FROM haberler")
    c.fetchall()


def dbHaberEkle(link):
    satirlar = gazeteoku(link)
    conn = sqlite3.connect("haberasistan.sqlite3")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS haberler(haber_site TEXT,haber_link TEXT,haber_tarih TEXT,haber_baslik TEXT)")
    conn.commit()
    eklenen = 0
    for row in satirlar:
        haber_link = row['haber_link']
        satir = tuple(row.values())
        c.execute("SELECT * FROM haberler WHERE haber_link=?", (haber_link,))
        getir = c.fetchone()
        if getir == None:
            eklenen = eklenen + 1
            c.execute("INSERT INTO haberler VALUES(?,?,?,?)", satir)
            conn.commit()
        elif len(getir) == 0:
            eklenen = eklenen + 1
            c.execute("INSERT INTO haberler VALUES(?,?,?,?)", satir)
            conn.commit()

    return eklenen


def topluHaberEkle():
    sozluk = {
        "https://www.gazeteoku.com/export/newsmap": "",
        "https://www.haber24.com/sitemap-news.xml": "",
        "https://www.kamugundemi.com/export/newsmap": "",
        "https://www.gazeteciler.com/export/newsmap": "",

    }
    for url in sozluk.keys():
        dbHaberEkle(url)


def haberGetir():
    conn = sqlite3.connect("haberasistan.sqlite3")
    c = conn.cursor()
    c.execute("SELECT haber_baslik,haber_tarih,haber_link FROM haberler")
    haberler = c.fetchall()
    df = pd.DataFrame(haberler)
    df.columns = ["Başlık", "Tarih", "URL"]
    # df['Tarih']=pd.to_datetime(df['Tarih'])+(pd.Timedelta(hours=3))

    now = datetime.datetime.now()
    now = now + datetime.timedelta(hours=3)
    df['Tarih'] = (pd.to_datetime(df['Tarih']))
    df['Tarih'] = df['Tarih'].dt.tz_localize(None)
    df['kalan'] = now - df['Tarih']
    df = df[df.kalan.dt.total_seconds() < 15800]
    df=df.sort_index(ascending=False)
    df=df[~df["Başlık"].str.contains(":")]

    df2=df[["Başlık","kalan"]]

    return df2

def trendsfull():
    link="https://trends.google.com.tr/trends/trendingsearches/daily/rss?geo=TR"
    req = urllib.request.Request(link, headers={'User-Agent' : "Magic Browser"}) 
    con = urllib.request.urlopen( req )
    xml=et.ElementTree(file=con)
    root=xml.getroot()
    gun=datetime.datetime.today()
    conn=sqlite3.connect("haberasistan.sqlite3")
    c=conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS trends(kelime TEXT,tarih TEXT)")
    conn.commit()
    for a in root[0].findall("item"):
        k=a[0].text
        t=gun.date()
        c.execute("SELECT * FROM trends WHERE kelime=? AND tarih=?",(k,t))
        tgetir=c.fetchall()
        if len(tgetir)==0:
            c.execute("INSERT INTO trends VALUES(?,?)",(k,t))
            conn.commit()
        
    c.execute("SELECT * FROM trends ORDER BY rowid DESC LIMIT 20")
    sonuc=c.fetchall()
    return sonuc

