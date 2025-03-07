import streamlit as st

st.set_page_config(page_title="Calculadora de Preços E-Commerce", layout="centered")

import sys
import os
import pandas as pd
from io import BytesIO


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import aba_shopee, aba_mercadolivre, aba_shopee_massa
from src.utils import load_css

# Função principal para execução
def main():
    tab1, tab2, tab3 = st.tabs(["Shopee", "Mercado Livre", "Calculo em Massa"])

    load_css("assets/styles.css")

    st.markdown(
        f'<div class="footer"> \
        Desenvolvido por <a href="https://www.linkedin.com/in/caiquegodoy" target="_blank">Caique Godoy</a> \
        </div>', 
        unsafe_allow_html=True
    )

    with tab1:
        aba_shopee.mostrar_aba_shopee()

    with tab2:
        aba_mercadolivre.mostrar_aba_mercadolivre()

    with tab3:
        aba_shopee_massa.mostrar_aba_shopee_massa()

# Executando o app
if __name__ == "__main__":
    main()
