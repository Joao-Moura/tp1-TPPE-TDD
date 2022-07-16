from datetime import timedelta

import pytest
from unittest import TestCase
from parameterized import parameterized

from classes.estacionamento import Estacionamento
from tests.factory import EstacionamentoFactory


class TestEstacionamentoMixin:
    def defaultSetUp(self):
        self.estacionamento = Estacionamento(
            porcentagem_contratante=50,
            valor_fracao=30,
            desconto_hora_cheia=15,
            diaria_diurna=120,
            desconto_diaria=45,
            entrada_noturna=timedelta(hours=19),
            saida_noturna=timedelta(hours=8),
            valor_mensal=600,
            valor_evento=50
        )


class TestFracaoQuinze(TestCase, TestEstacionamentoMixin):
    
    def setUp(self):
        self.defaultSetUp()

    @parameterized.expand([
        (timedelta(hours=8, minutes=30), timedelta(hours=8, minutes=56), 60),
        (timedelta(hours=18, minutes=40), timedelta(hours=19, minutes=20), 90),
        (timedelta(hours=10, minutes=15), timedelta(hours=10, minutes=30), 30)
    ])
    @pytest.mark.TesteFuncional
    def test_cadastro_fracao(self, hora_entrada, hora_saida, preco_total):
        actual = self.estacionamento.calcula_preco(hora_entrada, hora_saida)
        self.assertEqual(actual, preco_total)


class TestHoraCheia(TestCase, TestEstacionamentoMixin):

    def setUp(self):
        self.defaultSetUp()

    @parameterized.expand([
        (timedelta(hours=8, minutes=30), timedelta(hours=9, minutes=30), 102),
        (timedelta(hours=8, minutes=30), timedelta(hours=10, minutes=30), 204),
        (timedelta(hours=10, minutes=15), timedelta(hours=12, minutes=30), 234)
    ])
    @pytest.mark.TesteFuncional
    def test_cadastra_hora_cheia(self, hora_entrada, hora_saida, preco_total):
        actual = self.estacionamento.calcula_preco(hora_entrada, hora_saida)
        self.assertEqual(actual, preco_total)


class TestDiariaDiurna(TestCase, TestEstacionamentoMixin):

    def setUp(self):
        self.defaultSetUp()

    @parameterized.expand([
        (timedelta(hours=8, minutes=30), timedelta(hours=18, minutes=30)),
        (timedelta(hours=6), timedelta(hours=15, minutes=1)),
        (timedelta(hours=9, minutes=15), timedelta(hours=19, minutes=30))
    ])
    @pytest.mark.TesteFuncional
    def test_diaria_diurna(self, hora_entrada, hora_saida):
        actual = self.estacionamento.calcula_preco(hora_entrada, hora_saida)
        self.assertEqual(actual, 120)


class TestDiariaNoturna(TestCase, TestEstacionamentoMixin):

    def setUp(self):
        self.defaultSetUp()
    
    @parameterized.expand([
        (timedelta(hours=20), timedelta(hours=7)),
        (timedelta(hours=19, seconds=1), timedelta(hours=7, minutes=59, seconds=59)),
        (timedelta(hours=23, minutes=15), timedelta(hours=23, minutes=30))
    ])
    @pytest.mark.TesteFuncional
    def test_diaria_noturna_um(self, hora_entrada, hora_saida):
        actual = self.estacionamento.calcula_preco(hora_entrada, hora_saida)
        self.assertEqual(actual, 54)


class TestTipoAcesso(TestCase, TestEstacionamentoMixin):

    def setUp(self):
        self.defaultSetUp()

    @parameterized.expand([
        ("Mensalista", 600),
        ("Evento", 50)
    ])
    @pytest.mark.TesteFuncional
    def test_tipo_acesso(self, tipo_acesso, preco_total):
        actual = self.estacionamento.calcula_preco(tipo_acesso=tipo_acesso)
        self.assertEqual(actual, preco_total)


class TestValorContratante(TestCase, TestEstacionamentoMixin):

    def setUp(self):
        self.defaultSetUp()
        self.factory = EstacionamentoFactory(self.estacionamento)

    @parameterized.expand([
        ([('acesso', "Evento"), ('hora', '08:30', '18:30'), ('hora', '08:30', '09:10')], 130),
        ([('hora', '20:00', '07:00'), ('hora', '08:30', '10:30'), ('acesso', "Mensalista"), ('hora', '08:30', '09:30')], 480),
        ([('acesso', "Mensalista"), ('acesso', "Evento")], 325)
    ])
    @pytest.mark.TesteFuncional
    def test_calcula_retorno_com_multiplos_acessos(self, acessos, expected):
        for acesso in acessos:
            getattr(self.factory, f'cria_por_{acesso[0]}')(*acesso[1:])
        self.assertEqual(expected, self.estacionamento.retorno_contratante)
