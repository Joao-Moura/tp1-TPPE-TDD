from math import ceil


class Estacionamento:
    def __init__(self, valor_fracao):
        self.valor_fracao = valor_fracao

    def calcula_preco(self, hora_inicial, hora_final):
        return ceil((hora_final - hora_inicial).seconds / (60 * 15)) * self.valor_fracao
