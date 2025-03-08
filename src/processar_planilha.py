import sys
import os
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from classes.CalculoPrecoShopee import CalculoPrecoShopee

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