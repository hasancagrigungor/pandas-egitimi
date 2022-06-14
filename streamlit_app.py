import streamlit as st
from passporteye.mrz.image import MRZPipeline
from passporteye import read_mrz

picture = st.camera_input("Çek çek çek")
mrz = read_mrz(picture)
st.write(mrz)

