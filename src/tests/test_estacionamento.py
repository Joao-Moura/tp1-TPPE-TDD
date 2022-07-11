from datetime import timedelta

import pytest
from unittest import TestCase
from parameterized import parameterized

from classes.estacionamento import Estacionamento

class TestEstacionamentoMixin:
    def defaultSetUp(self):
        self.estacionamento = Estacionamento(
            valor_fracao=30,
            desconto_hora_cheia=15,
            diaria_diurna=120,
            entrada_noturna=timedelta(hours=19),
            saida_noturna=timedelta(hours=8)
        )


class TestFacaoQuinze(TestCase, TestEstacionamentoMixin):
    
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
    
    @pytest.mark.TesteFuncional
    def test_diaria_noturna_um(self):
        actual = self.estacionamento.calcula_preco(timedelta(hours=20), timedelta(hours=7))
        self.assertEqual(actual, 54)
    