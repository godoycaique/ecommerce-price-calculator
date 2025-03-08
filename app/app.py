import streamlit as st

st.set_page_config(page_title="Calculadora de Preços E-Commerce", layout="centered")

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import aba_shopee, aba_mercadolivre, aba_shopee_massa
from src.utils import load_css

# Função principal para execução
def main():
    tab1, tab2 = st.tabs(["Shopee", "Mercado Livre"])

    load_css("assets/styles.css")

    st.markdown(
        f'<div class="footer"> \
        Desenvolvido por <a href="https://www.linkedin.com/in/caiquegodoy" target="_blank">Caique Godoy</a> | \
        <a href="https://godoycaique.github.io/ecommerce-price-calculator//" target="_blank">Documentação do Aplicativo</a> \
        </div>', 
        unsafe_allow_html=True
    )

    with tab1:
        tab_unit, tab_massa = st.tabs(['Calculo unitário', 'Calculo em massa'])
        
        with tab_unit:
            aba_shopee.mostrar_aba_shopee()
        with tab_massa:
            aba_shopee_massa.mostrar_aba_shopee_massa()

    with tab2:
        aba_mercadolivre.mostrar_aba_mercadolivre()

# Executando o app
if __name__ == "__main__":
    main()
