import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils import define_campos_inputs_principal, load_css
from classes.CalculoPrecoShopee import CalculoPrecoShopee

load_css("assets/styles.css")

def mostrar_aba_shopee():
    """
    Cria a página de cálculo de preço de venda unitário para produtos da shopee

    Exemplo de uso:
    Realizar a chamada da função no arquivo app.py
    """

    st.header("📊 Calculadora de Preços - Shopee")
    st.write("Preencha os campos abaixo para calcular o preço ideal do seu produto.")

    # Pegando os parâmetros do Streamlit
    custo_produto, custo_embalagem, taxa_imposto, taxa_shopee, valor_fixo_shopee, outros_custos, considera_operacional, faturamento_mensal, custos_fixos, lucro_esperado, lucro_minimo = define_campos_inputs_principal()

    # Calculando o preço de venda, despesas, lucro e comissões
    # Criando a instância da classe
    calculadora = CalculoPrecoShopee(custo_produto, custo_embalagem, taxa_imposto, taxa_shopee, valor_fixo_shopee, outros_custos, considera_operacional, faturamento_mensal, custos_fixos, lucro_esperado, lucro_minimo)
    calculadora.calcula_preco_venda()


    valor_comissao_shopee, perc_comissao_shopee, valor_imposto, receita_operacional = calculadora.calcula_comissoes_impostos_receita('final')
    valor_comissao_shopee_min, perc_comissao_shopee_min, valor_imposto_min, receita_operacional_min = calculadora.calcula_comissoes_impostos_receita('minimo')

    lucro = calculadora.calcula_lucro('final')
    lucro_com_desconto = calculadora.calcula_lucro('minimo')
    sugestao_aumento = calculadora.sugere_aumento()

    st.subheader("Valores Detalhados", divider="gray")

    # Colunas de Valores, Lucro e descontos
    col1, col2 = st.columns(2, gap="small", border=False)

    with col1:
        st.markdown(
            f'<div class="coluna-verde"> \
            <b>Valor de Venda:</b> R${calculadora.preco_ideal:.2f}<br> \
            <b>Desconto Máximo:</b> {calculadora.max_desconto * 100:.2f}%</div>', 
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f'<div class="coluna-verde"> \
            <b>Lucro por Venda:</b> R${lucro:.2f}<br> \
            <b>Lucro com Valor Mínimo:</b> {lucro_com_desconto:.2f}</div>', 
            unsafe_allow_html=True
        )

    st.html("<br>")
    if sugestao_aumento:
        st.warning(sugestao_aumento)

    st.html("<br>")
    st.subheader("Despesas", divider="gray")
    st.write("Despesas com base no valor de venda original sugerido.")

    # Colunas de Despesas
    col5, col6 = st.columns(2, gap="small", border=False)

    with col5:
        st.markdown(
            f'<div class="coluna-vermelha"> \
            <b>Comissão Shopee:</b> R${valor_comissao_shopee:.2f}<br> \
            <b>Valor de Imposto:</b> R${valor_imposto:.2f}<br> \
            <b>Receita Operacional:</b> R${receita_operacional:.2f}</div>', 
            unsafe_allow_html=True
        )

    with col6:
        st.markdown(
            f'<div class="coluna-vermelha"> \
            <b>% Comissão Shopee:</b> {perc_comissao_shopee * 100:.2f}%<br> \
            <b>% Imposto:</b> R${taxa_imposto:.2f}<br> \
            <b>% Custo Operacional:</b> {calculadora.percentual_despesas * 100:.2f}%</div>', 
            unsafe_allow_html=True
        )

    st.html("<br>")
    st.write("Despesas com base no valor de venda com valor mínimo.")

    col7, col8 = st.columns(2, gap="small", border=False)

    with col7:
        st.markdown(
            f'<div class="coluna-vermelha"> \
            <b>Comissão Shopee:</b> R${valor_comissao_shopee_min:.2f}<br> \
            <b>Valor de Imposto:</b> R${valor_imposto_min:.2f}<br> \
            <b>Receita Operacional:</b> R${receita_operacional_min:.2f}</div>', 
            unsafe_allow_html=True
        )

    with col8:
        st.markdown(
            f'<div class="coluna-vermelha"> \
            <b>% Comissão Shopee:</b> {perc_comissao_shopee_min * 100:.2f}%<br> \
            <b>% Imposto:</b> R${taxa_imposto:.2f}%<br> \
            <b>% Custo Operacional:</b> {calculadora.percentual_despesas * 100:.2f}%</div>', 
            unsafe_allow_html=True
        )