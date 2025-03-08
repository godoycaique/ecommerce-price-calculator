import streamlit as st
import sys
import os
from io import BytesIO
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils import define_campos_inputs_massa, load_css
from src.processar_planilha import processar_planilha

load_css("assets/styles.css")

def mostrar_aba_shopee_massa():
    """
    Cria a página de cálculo de preço de venda em massa da Shopee

    Exemplo de uso:
    Realizar a chamada da função no arquivo app.py
    """
     
    st.header("📊 Calculadora de Preços em Massa")
    st.write("Faça o cálculo em massa do preço de venda de seus produtos!")

    # Pegando os parâmetros do Streamlit
    taxa_imposto_input, taxa_shopee_input, valor_fixo_shopee_input, considera_operacional_input, faturamento_mensal_input, custos_fixos_input, lucro_esperado_input, lucro_minimo_input = define_campos_inputs_massa()

    arquivo_exemplo = "data/planilha_custos.xlsx"

    st.warning  ("Para não incluir um arquivo inválido, faça o download do nosso arquivo excel de exemplo padronizado, preencha e depois faça o upload acima.")
    try:
        with open(arquivo_exemplo, "rb") as file:
            btn = st.download_button(
                label="Baixar Arquivo de Exemplo",
                data=file,
                file_name="planilha_custos.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    except FileNotFoundError:
        st.error("Arquivo não encontrado. Verifique o caminho do arquivo.")
        
    uploaded_file = st.file_uploader("Faça o upload da planilha (Excel ou CSV)", type=["xlsx", "csv"])

    if uploaded_file is not None:
        # Lendo o arquivo
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        # Verificando as colunas necessárias
        colunas_necessarias = ["Custo Produto", "Custo Embalagem", "Outros Custos"]

        if all(coluna in df.columns for coluna in colunas_necessarias):
            # Processando a planilha
            df_resultados = processar_planilha(
                df, 
                taxa_imposto_input, 
                taxa_shopee_input,
                valor_fixo_shopee_input, 
                considera_operacional_input, 
                faturamento_mensal_input, 
                custos_fixos_input, 
                lucro_esperado_input, 
                lucro_minimo_input
            )

            df_resultados.set_index("Nome Produto", inplace=True)

            # Exibindo os resultados
            st.write("### Resultados")
            st.dataframe(df_resultados)

            # Botão para exportar os resultados para Excel
            output = BytesIO()
            with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                df_resultados.to_excel(writer, index=False, sheet_name="analise_venda")
            output.seek(0)

            st.download_button(
                label="Exportar para Excel",
                data=output,
                file_name="resultados.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"    
            )
        else:
            st.error(f"A planilha deve conter as colunas: {', '.join(colunas_necessarias)}")
    else:
        st.info("Faça o upload de uma planilha para começar.")