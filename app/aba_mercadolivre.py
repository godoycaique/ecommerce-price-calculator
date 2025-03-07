import streamlit as st
import sys
import os
from io import BytesIO


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import utils
from classes.CalculoPrecoShopee import CalculoPrecoShopee

utils.load_css("assets/styles.css")

def mostrar_aba_mercadolivre():
    st.header("📊 Calculadora de Preço para Mercado Livre")
    st.write("Preencha os campos abaixo para calcular o preço ideal do seu produto.")