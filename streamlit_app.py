import streamlit as st
from passporteye.mrz.image import MRZPipeline
from passporteye import read_mrz
import pytesseract

picture = st.camera_input("")

if picture!=None:
  mrz = read_mrz(picture)
  st.write(mrz)

