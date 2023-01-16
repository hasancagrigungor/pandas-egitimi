import streamlit as st
from duckduckgo_search import ddg
import requests
import json
import pandas as pd

from duckduckgo_search import ddg


def domainbul(link):
    url = link.split("/")
    for i in url:
        if ("www." in i) or (".com" in i) or (".net" in i):
            domain = i
            break
        else:
            domain = ""

    return domain


input = st.text_area("Anahtar Kelimeleri Aralarında Virgül İle Giriniz Örnek Merve Kurs,Merve Kayıt")
keywordss = input.split(",")
marka = st.text_input("Marka örnek Merve")
sozluk = {}
buton=st.button("getir")
if buton:
    for keywords in keywordss:
        for i in range(1, 6):
            results = ddg(keywords, region='tr-tr', safesearch='Off', time='y', page=i)

            for a in results:
                dm = domainbul(a['href'])

                if len(dm) > 0 and marka in a['href']:
                    if dm in sozluk.keys():
                        liste = sozluk[dm]
                        if a['href'] not in liste:
                            liste.append(a['href'])
                            sozluk[dm] = liste
                    else:
                        sozluk[dm] = [a['href']]
        for w in sozluk.keys():
            sorgu = w + " " + marka
            results2 = ddg(keywords, region='tr-tr', safesearch='Off', time='y', page=1)
            for e in results2:
                if marka in e['href'] and w in e['href']:
                    liste2 = sozluk[w]
                    if e['href'] not in liste2:
                        liste2.append(e['href'])
                        sozluk[w] = liste2
    
    
    for site in sozluk:
        st.title(site)
        listeler=sozluk[site]
        
        
        
        
        for ur in listeler:
            st.write(ur)
            df.append({"domain":site,"url":ur},ignore_index=True)


   
