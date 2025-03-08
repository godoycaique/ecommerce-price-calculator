import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src import config

# Função para pegar parâmetros do Streamlit
def define_campos_inputs_principal():
    col1, col2 = st.columns(2, gap="small", border=True)

    with col1:
        custo_produto = st.number_input("Custo do Produto (R$)", value=0.00, help=config.custo_produto_help)
        custo_embalagem = st.number_input("Custo da Embalagem (R$)", value=0.00, help=config.custo_embalagem_help)
        taxa_imposto = st.number_input("Taxa de Imposto (%)", value=0.00, help=config.taxa_imposto_help)
        taxa_shopee = st.number_input("Taxa Shopee (%)", value=20.0, help=config.taxa_shopee_help)
        valor_fixo_shopee = st.number_input("Valor Fixo Shopee (R$)", value=4.0, help=config.valor_fixo_shopee_help)
        outros_custos = st.number_input("Outros Custos (R$)", value=0.0, help=config.outros_custos_help)
    with col2:
        considera_operacional = st.checkbox("Considera Custos Operacionais", value=True)
        faturamento_mensal = st.number_input("Faturamento Mensal (R$)", value=0.00, help=config.faturamento_mensal_help)
        custos_fixos = st.number_input("Custos Fixos (R$)", value=0.00, help=config.custos_fixos_help)
        lucro_esperado = st.slider("Lucro Esperado (%):", min_value=10.0, max_value=60.0, value=20.0, help=config.lucro_esperado_help)
        lucro_minimo = st.slider("Lucro Mínimo (%):", min_value=10.0, max_value=60.0, value=10.0, help=config.lucro_minimo_help)

    return custo_produto, custo_embalagem, taxa_imposto, taxa_shopee, valor_fixo_shopee, outros_custos, considera_operacional, faturamento_mensal, custos_fixos, lucro_esperado, lucro_minimo


def define_campos_inputs_massa():
    col1, col2 = st.columns(2, gap="small", border=True)

    with col1:
        taxa_imposto = st.number_input(
            "Taxa de Imposto (%)", 
            value=0.00, 
            help=config.taxa_imposto_help, 
            key="taxa_imposto_input"
        )

        taxa_shopee = st.number_input(
            "Taxa Shopee (%)", 
            value=20.0, 
            help=config.taxa_shopee_help,
            key="taxa_shopee_input")
        
        valor_fixo_shopee = st.number_input(
            "Valor Fixo Shopee (R$)", 
            value=4.0, 
            help=config.valor_fixo_shopee_help,
            key="valor_fixo_shopee_input")
        
    with col2:
        considera_operacional = st.checkbox(
            "Considera Custos Operacionais", 
            value=True,
            key="considera_operacional_input"
        )
        
        faturamento_mensal = st.number_input(
            "Faturamento Mensal (R$)", 
            value=0.00, 
            help=config.faturamento_mensal_help,
            key="faturamento_mensal_input"
        )

        custos_fixos = st.number_input(
            "Custos Fixos (R$)", 
            value=0.00, 
            help=config.custos_fixos_help,
            key="custos_fixos_input"
        
        )
        lucro_esperado = st.slider(
            "Lucro Esperado (%):", 
            min_value=10.0, 
            max_value=60.0, 
            value=20.0, 
            help=config.lucro_esperado_help,
            key="lucro_esperado_input"
        )

        lucro_minimo = st.slider(
            "Lucro Mínimo (%):", 
            min_value=10.0, 
            max_value=60.0, 
            value=10.0, 
            help=config.lucro_minimo_help,
            key="lucro_minimo_input"
        )

    return taxa_imposto, taxa_shopee, valor_fixo_shopee, considera_operacional, faturamento_mensal, custos_fixos, lucro_esperado, lucro_minimo


# Função para carregar o CSS
def load_css(file_path):
    with open(file_path, "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)