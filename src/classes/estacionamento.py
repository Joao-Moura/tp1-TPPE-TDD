from math import ceil


class Estacionamento:
    def __init__(self, valor_fracao=None, desconto_hora_cheia=None, diaria_diurna=None):
        self.valor_fracao = valor_fracao
        self.desconto_hora_cheia = desconto_hora_cheia
        self.diaria_diurna = diaria_diurna
        
    @property
    def hora_cheia_descontada(self):
        return self.valor_fracao * 4 * ((100 - self.desconto_hora_cheia) / 100)

    def calcula_preco(self, hora_inicial, hora_final):
        fracoes = ceil((hora_final - hora_inicial).seconds / (60 * 15))

        if fracoes > 36:
            return 120
        if fracoes >= 4:
            return ((fracoes // 4) * self.hora_cheia_descontada) + (fracoes % 4) * self.valor_fracao

        return fracoes * self.valor_fracao
