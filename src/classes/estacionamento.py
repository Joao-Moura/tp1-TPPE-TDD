from math import ceil


class Estacionamento:
    def __init__(self, valor_fracao=None, desconto_hora_cheia=None):
        self.valor_fracao = valor_fracao
        self.desconto_hora_cheia = desconto_hora_cheia

    def calcula_preco(self, hora_inicial, hora_final):
        fracoes = ceil((hora_final - hora_inicial).seconds / (60 * 15))

        if fracoes >= 4:
            return 102

        return fracoes * self.valor_fracao
