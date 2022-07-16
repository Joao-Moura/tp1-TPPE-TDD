from datetime import timedelta, datetime

from classes.estacionamento import Estacionamento


class EstacionamentoFactory:

    def __init__(self, estacionamento):
        self.estacionamento = estacionamento

    def _str2time(self, hora):
        h = datetime.strptime(hora, "%H:%M")
        return timedelta(hours=h.hour, minutes=h.minute, seconds=h.second)

    def cria_por_hora(self, hora_inicial, hora_final):
        return self.estacionamento.calcula_preco(
            self._str2time(hora_inicial), self._str2time(hora_final))

    def cria_por_acesso(self, tipo_acesso):
        return self.estacionamento.calcula_preco(tipo_acesso=tipo_acesso)
