import pandas as pd
from io import BytesIO
import streamlit as st

from src import utils

# Título do app
st.title("Calculadora de Preços para Múltiplos Produtos")

# Upload da planilha
uploaded_file = st.file_uploader("Faça o upload da planilha (Excel ou CSV)", type=["xlsx", "csv"])

if uploaded_file is not None:
    # Lendo o arquivo
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    # Verificando as colunas necessárias
    colunas_necessarias = ["Custo Produto", "Taxa Imposto", "Taxa Shopee", "Valor Fixo Shopee", "Lucro Esperado", "Lucro Minimo"]
    if all(coluna in df.columns for coluna in colunas_necessarias):
        # Processando a planilha
        df_resultados = utils.processar_planilha(df)

        # Exibindo os resultados
        st.write("### Resultados")
        st.dataframe(df_resultados)

        # Botão para exportar os resultados para Excel
        output = BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df_resultados.to_excel(writer, index=False, sheet_name="Resultados")
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