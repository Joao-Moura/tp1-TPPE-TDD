from math import ceil


class Estacionamento:
    def __init__(
            self,
            porcentagem_contratante,
            valor_fracao=None, 
            desconto_hora_cheia=None,
            diaria_diurna=None,
            desconto_diaria=None,
            entrada_noturna=None,
            saida_noturna=None,
            valor_mensal=None,
            valor_evento=None
        ):
        self.valor_fracao = valor_fracao
        self.desconto_hora_cheia = desconto_hora_cheia
        self.diaria_diurna = diaria_diurna
        self.desconto_diaria = desconto_diaria
        self.entrada_noturna = entrada_noturna
        self.saida_noturna = saida_noturna
        self.valor_mensal = valor_mensal
        self.valor_evento = valor_evento

        self.porcentagem_contratante = porcentagem_contratante
        self.retorno_contratante = 0

    @property
    def hora_cheia_descontada(self):
        return self.valor_fracao * 4 * ((100 - self.desconto_hora_cheia) / 100)

    def calcula_preco(self, hora_inicial=None, hora_final=None, tipo_acesso=""):
        valor_estacionamento = 0

        if tipo_acesso:
            if tipo_acesso == "Mensalista":
                valor_estacionamento = self.valor_mensal
            elif tipo_acesso == "Evento":
                valor_estacionamento = self.valor_evento
        else:
            fracoes = ceil((hora_final - hora_inicial).seconds / (60 * 15))
            if hora_inicial > self.entrada_noturna and (hora_final < self.saida_noturna or hora_final > self.entrada_noturna):
                valor_estacionamento = self.diaria_diurna * (self.desconto_diaria / 100)
            elif fracoes > 36:
                valor_estacionamento = self.diaria_diurna
            elif fracoes >= 4:
                valor_estacionamento = ((fracoes // 4) * self.hora_cheia_descontada) + (fracoes % 4) * self.valor_fracao
            else:
                valor_estacionamento = fracoes * self.valor_fracao

        self.retorno_contratante += (valor_estacionamento * (self.porcentagem_contratante / 100))
        return valor_estacionamento
