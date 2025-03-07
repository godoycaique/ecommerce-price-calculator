class CalculoPrecoShopee:
    def __init__(self, custo_produto, custo_embalagem, taxa_imposto, taxa_shopee, 
                 valor_fixo_shopee, outros_custos, faturamento_mensal, custos_fixos, 
                 lucro_esperado, lucro_minimo):
        self.custo_produto = custo_produto
        self.custo_embalagem = custo_embalagem
        self.taxa_imposto = taxa_imposto / 100  # Convertendo para decimal
        self.taxa_shopee = taxa_shopee / 100  # Convertendo para decimal
        self.valor_fixo_shopee = valor_fixo_shopee
        self.outros_custos = outros_custos
        self.faturamento_mensal = faturamento_mensal
        self.custos_fixos = custos_fixos
        self.lucro_esperado = lucro_esperado / 100  # Convertendo para decimal
        self.lucro_minimo = lucro_minimo / 100  # Convertendo para decimal

        self.custo_produto_total = self.custo_produto + self.custo_embalagem
        self.percentual_despesas = self.custos_fixos / self.faturamento_mensal
        self.preco_ideal = None
        self.preco_minimo = None
        self.max_desconto = None

    def calcula_preco_venda(self):
        """Calcula o preço de venda ideal e o mínimo."""
        self.preco_ideal = (self.custo_produto_total + self.valor_fixo_shopee + self.outros_custos) / \
            (1 - (self.percentual_despesas + self.taxa_shopee + self.taxa_imposto + self.lucro_esperado))
        self.preco_minimo = (self.custo_produto_total + self.valor_fixo_shopee + self.outros_custos) / \
            (1 - (self.percentual_despesas + self.taxa_shopee + self.taxa_imposto + self.lucro_minimo))
        self.max_desconto = max((self.preco_ideal - self.preco_minimo) / self.preco_ideal, 0)

    def calcula_despesas(self):
        """Calcula as despesas totais."""
        return self.custo_produto_total + (self.percentual_despesas * self.preco_ideal) + \
            (self.taxa_shopee * self.preco_ideal) + self.valor_fixo_shopee + self.outros_custos + \
            (self.taxa_imposto * self.preco_ideal)

    def calcula_lucro(self, tipo_calculo):
        """Calcula o lucro."""
        despesa_total = self.calcula_despesas()
        if tipo_calculo == "final":
            return self.preco_ideal - despesa_total
        if tipo_calculo == "minimo":
            return self.preco_minimo - despesa_total

    def calcula_comissoes_impostos_receita(self, tipo_calculo):
        """Calcula as comissões, impostos e receita operacional."""
        if tipo_calculo == "final":
            valor_comissao_shopee = self.preco_ideal * self.taxa_shopee + self.valor_fixo_shopee
            perc_comissao_shopee = valor_comissao_shopee / self.preco_ideal
            valor_imposto = self.preco_ideal * self.taxa_imposto
            receita_operacional = self.preco_ideal * self.percentual_despesas
        if tipo_calculo == "minimo":
            valor_comissao_shopee = self.preco_minimo * self.taxa_shopee + self.valor_fixo_shopee
            perc_comissao_shopee = valor_comissao_shopee / self.preco_minimo
            valor_imposto = self.preco_minimo * self.taxa_imposto
            receita_operacional = self.preco_minimo * self.percentual_despesas

        return valor_comissao_shopee, perc_comissao_shopee, valor_imposto, receita_operacional

    def sugere_aumento(self):
        """Sugere aumento de preço baseado no desconto máximo."""
        sugestao_aumento = ""
        if self.max_desconto < 0.1:
            preco_sugerido = self.preco_ideal * 1.2  # Sugestão de aumento de 20%
            max_desconto_sugerido = ((preco_sugerido - self.preco_minimo) / preco_sugerido) * 100
            sugestao_aumento = f"Se você aumentar o preço para R$ {preco_sugerido:.2f}, poderá oferecer até {max_desconto_sugerido:.2f}% de desconto."
        return sugestao_aumento