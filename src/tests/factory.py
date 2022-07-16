import string

from datetime import timedelta, datetime

from random import sample

from classes.estacionamento import Estacionamento


class EstacionamentoFactory:

    def __init__(self, estacionamento, placa=None):
        self.estacionamento = estacionamento
        self.placa = placa

    def _str2time(self, hora):
        h = datetime.strptime(hora, "%H:%M")
        return timedelta(hours=h.hour, minutes=h.minute, seconds=h.second)

    @property
    def _placa_random(self):
        return self.placa or ''.join(sample(string.ascii_uppercase + string.digits, 5))

    def cria_por_hora(self, hora_inicial, hora_final):
        return self.estacionamento.calcula_preco(
            self._placa_random, self._str2time(hora_inicial), self._str2time(hora_final))

    def cria_por_acesso(self, tipo_acesso):
        return self.estacionamento.calcula_preco(self._placa_random, tipo_acesso=tipo_acesso)
