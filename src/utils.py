import streamlit as st
import sys
import os
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src import config
from classes.CalculoPrecoShopee import CalculoPrecoShopee

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


# Função para processar a planilha
def processar_planilha(df, taxa_imposto, taxa_shopee, valor_fixo_shopee, considera_operacional, faturamento_mensal, custos_fixos, lucro_esperado, lucro_minimo):
    resultados = []
    for index, row in df.iterrows():
        # Criando uma instância da classe para cada produto
        calculadora = CalculoPrecoShopee(
            custo_produto = row["Custo Produto"],
            custo_embalagem = row.get("Custo Embalagem", 0),  # Valor padrão se a coluna não existir
            taxa_imposto = taxa_imposto,
            taxa_shopee = taxa_shopee,
            valor_fixo_shopee = valor_fixo_shopee,
            outros_custos = row.get("Outros Custos", 0),
            considera_operacional = considera_operacional,
            faturamento_mensal = faturamento_mensal,
            custos_fixos = custos_fixos,
            lucro_esperado = lucro_esperado,
            lucro_minimo = lucro_minimo
        )

        # Calculando os valores
        calculadora.calcula_preco_venda()

        valor_comissao_shopee, perc_comissao_shopee, valor_imposto, receita_operacional = calculadora.calcula_comissoes_impostos_receita('final')
        lucro = calculadora.calcula_lucro('final')

        sugestao_aumento = calculadora.sugere_aumento()

        # Armazenando os resultados
        resultados.append({
            "Nome Produto": row.get("Nome Produto", f"Produto {index + 1}"),  # Nome do produto (se existir)
            "Preço de Venda": calculadora.preco_ideal,
            "Lucro (R$)": lucro,
            "Desconto Máximo": calculadora.max_desconto * 100,  # Em porcentagem
            "Comissão Shopee (R$)": valor_comissao_shopee,
            "% Comissão Shopee": perc_comissao_shopee * 100,  # Em porcentagem
            "Valor Imposto (R$)": valor_imposto,
            "Receita Operacional (R$)": receita_operacional,
            "Sugestão de Aumento": sugestao_aumento
        })

    return pd.DataFrame(resultados)
