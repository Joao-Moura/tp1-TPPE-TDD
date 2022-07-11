from math import ceil


class Estacionamento:
    def __init__(
            self,
            valor_fracao=None, 
            desconto_hora_cheia=None,
            diaria_diurna=None,
            desconto_diaria=None,
            entrada_noturna=None,
            saida_noturna=None,
            valor_mensal=None
        ):
        self.valor_fracao = valor_fracao
        self.desconto_hora_cheia = desconto_hora_cheia
        self.diaria_diurna = diaria_diurna
        self.desconto_diaria = desconto_diaria
        self.entrada_noturna = entrada_noturna
        self.saida_noturna = saida_noturna
        self.valor_mensal = valor_mensal
        
    @property
    def hora_cheia_descontada(self):
        return self.valor_fracao * 4 * ((100 - self.desconto_hora_cheia) / 100)

    def calcula_preco(self, hora_inicial=None, hora_final=None, tipo_acesso=""):
        if tipo_acesso == "Mensalista":
            return self.valor_mensal

        fracoes = ceil((hora_final - hora_inicial).seconds / (60 * 15))

        if hora_inicial > self.entrada_noturna and (hora_final < self.saida_noturna or hora_final > self.entrada_noturna):
            return self.diaria_diurna * (self.desconto_diaria / 100)
        if fracoes > 36:
            return self.diaria_diurna
        if fracoes >= 4:
            return ((fracoes // 4) * self.hora_cheia_descontada) + (fracoes % 4) * self.valor_fracao

        return fracoes * self.valor_fracao
