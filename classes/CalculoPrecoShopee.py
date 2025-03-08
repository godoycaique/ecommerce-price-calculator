class CalculoPrecoShopee:
    def __init__(self, custo_produto=0, custo_embalagem=0, taxa_imposto=0, taxa_shopee=0, 
                 valor_fixo_shopee=0, outros_custos=0, considera_operacional=True, faturamento_mensal=0, custos_fixos=0, 
                 lucro_esperado=0, lucro_minimo=0):
        
        self.custo_produto = custo_produto
        self.custo_embalagem = custo_embalagem
        self.taxa_imposto = taxa_imposto / 100  # Convertendo para decimal
        self.taxa_shopee = taxa_shopee / 100  # Convertendo para decimal
        self.valor_fixo_shopee = valor_fixo_shopee
        self.outros_custos = outros_custos
        self.considera_operacional = considera_operacional
        self.faturamento_mensal = faturamento_mensal
        self.custos_fixos = custos_fixos
        self.lucro_esperado = lucro_esperado / 100  # Convertendo para decimal
        self.lucro_minimo = lucro_minimo / 100  # Convertendo para decimal
        self.custo_produto_total = self.custo_produto + self.custo_embalagem
        
        self.percentual_despesas = self.calcula_percentual_despesa()
        
        self.preco_ideal = None
        self.preco_minimo = None
        self.max_desconto = None

    def calcula_preco_venda(self):
        """Calcula o preço de venda ideal e o valor mínimo."""

        if self.considera_operacional:
            if self.percentual_despesas is None or self.taxa_shopee is None or self.taxa_imposto is None:
                return
            try:
                self.preco_ideal = (self.custo_produto_total + self.valor_fixo_shopee + self.outros_custos) / \
                    (1 - (self.percentual_despesas + self.taxa_shopee + self.taxa_imposto + self.lucro_esperado))
                self.preco_minimo = (self.custo_produto_total + self.valor_fixo_shopee + self.outros_custos) / \
                    (1 - (self.percentual_despesas + self.taxa_shopee + self.taxa_imposto + self.lucro_minimo))
                self.max_desconto = max((self.preco_ideal - self.preco_minimo) / self.preco_ideal, 0)
            except ZeroDivisionError:
                self.preco_ideal = None
                self.preco_minimo = None
                self.max_desconto = None
        else:
            try:
                self.preco_ideal = (self.custo_produto_total + self.valor_fixo_shopee + self.outros_custos) / \
                    (1 - (self.taxa_shopee + self.taxa_imposto + self.lucro_esperado))
                self.preco_minimo = (self.custo_produto_total + self.valor_fixo_shopee + self.outros_custos) / \
                    (1 - (self.taxa_shopee + self.taxa_imposto + self.lucro_minimo))
                self.max_desconto = max((self.preco_ideal - self.preco_minimo) / self.preco_ideal, 0)
            except ZeroDivisionError:
                # Tratamento de erro caso ocorra divisão por zero
                self.preco_ideal = None
                self.preco_minimo = None
                self.max_desconto = None

    def calcula_percentual_despesa(self):
        """Calcula percentual de despesa com base no faturamento mensal bruto e nos custos fixos menal da empresa"""
        if self.faturamento_mensal == 0:
            return 0
        else:
            return self.custos_fixos / self.faturamento_mensal
    
    def calcula_despesas(self):
        """Calcula as despesas totais, considerando ou não o percentual de despesas."""
        if self.preco_ideal is None:
            return 0
        
        # Cálculo base das despesas
        despesas = self.custo_produto_total + \
                (self.taxa_shopee * self.preco_ideal) + \
                self.valor_fixo_shopee + \
                self.outros_custos + \
                (self.taxa_imposto * self.preco_ideal)
        
        # Adiciona o percentual de despesas apenas se self.considera_operacional for True
        if self.considera_operacional:
            despesas += (self.percentual_despesas * self.preco_ideal)
        
        return despesas

    def calcula_lucro(self, tipo_calculo):
        """Calcula o lucro."""
        despesa_total = self.calcula_despesas()
        if tipo_calculo == "final" and self.preco_ideal is not None:
            return self.preco_ideal - despesa_total
        if tipo_calculo == "minimo" and self.preco_minimo is not None:
            return self.preco_minimo - despesa_total
        return 0

    def calcula_comissoes_impostos_receita(self, tipo_calculo):
        """Calcula as comissões, impostos e receita operacional."""
        if tipo_calculo == "final" and self.preco_ideal is not None:
            valor_comissao_shopee = self.preco_ideal * self.taxa_shopee + self.valor_fixo_shopee
            perc_comissao_shopee = valor_comissao_shopee / self.preco_ideal
            valor_imposto = self.preco_ideal * self.taxa_imposto
            receita_operacional = self.preco_ideal * self.percentual_despesas
        elif tipo_calculo == "minimo" and self.preco_minimo is not None:
            valor_comissao_shopee = self.preco_minimo * self.taxa_shopee + self.valor_fixo_shopee
            perc_comissao_shopee = valor_comissao_shopee / self.preco_minimo
            valor_imposto = self.preco_minimo * self.taxa_imposto
            receita_operacional = self.preco_minimo * self.percentual_despesas
        else:
            return 0, 0, 0, 0

        return valor_comissao_shopee, perc_comissao_shopee, valor_imposto, receita_operacional

    def sugere_aumento(self):
        """Sugere aumento de preço baseado no desconto máximo."""
        if self.max_desconto is None or self.preco_ideal is None or self.preco_minimo is None:
            return ""

        sugestao_aumento = ""
        if self.max_desconto < 0.1:
            preco_sugerido = self.preco_ideal * 1.2  # Sugestão de aumento de 20%
            max_desconto_sugerido = ((preco_sugerido - self.preco_minimo) / preco_sugerido) * 100
            sugestao_aumento = f"Se você aumentar o preço para R$ {preco_sugerido:.2f}, poderá oferecer até {max_desconto_sugerido:.2f}% de desconto."
        return sugestao_aumento