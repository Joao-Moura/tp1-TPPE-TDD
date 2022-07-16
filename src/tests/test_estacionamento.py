from datetime import timedelta

import pytest
from unittest import TestCase
from parameterized import parameterized

from classes.estacionamento import Estacionamento
from excecoes.excecao import *
from tests.factory import EstacionamentoFactory


class TestEstacionamentoMixin:
    def defaultSetUp(self):
        self.estacionamento = Estacionamento(
            porcentagem_contratante=50,
            capacidade=10,
            valor_fracao=30,
            desconto_hora_cheia=15,
            diaria_diurna=120,
            desconto_diaria=45,
            entrada_noturna=timedelta(hours=19),
            saida_noturna=timedelta(hours=8),
            valor_mensal=600,
            valor_evento=50
        )
        self.factory = EstacionamentoFactory(self.estacionamento)


class TestFracaoQuinze(TestCase, TestEstacionamentoMixin):
    
    def setUp(self):
        self.defaultSetUp()

    @parameterized.expand([
        ('08:30', '08:56', 60),
        ('18:40', '19:20', 90),
        ('10:15', '10:30', 30)
    ])
    @pytest.mark.TesteFuncional
    def test_cadastro_fracao(self, hora_entrada, hora_saida, preco_total):
        actual = self.factory.cria_por_hora(hora_entrada, hora_saida)
        self.assertEqual(actual, preco_total)


class TestHoraCheia(TestCase, TestEstacionamentoMixin):

    def setUp(self):
        self.defaultSetUp()

    @parameterized.expand([
        ('08:30', '9:30', 102),
        ('08:30', '10:30', 204),
        ('10:15', '12:30', 234)
    ])
    @pytest.mark.TesteFuncional
    def test_cadastra_hora_cheia(self, hora_entrada, hora_saida, preco_total):
        actual = self.factory.cria_por_hora(hora_entrada, hora_saida)
        self.assertEqual(actual, preco_total)


class TestDiariaDiurna(TestCase, TestEstacionamentoMixin):

    def setUp(self):
        self.defaultSetUp()

    @parameterized.expand([
        ('08:30', '18:30'),
        ('06:00', '15:01'),
        ('09:15', '19:30')
    ])
    @pytest.mark.TesteFuncional
    def test_diaria_diurna(self, hora_entrada, hora_saida):
        actual = self.factory.cria_por_hora(hora_entrada, hora_saida)
        self.assertEqual(actual, 120)


class TestDiariaNoturna(TestCase, TestEstacionamentoMixin):

    def setUp(self):
        self.defaultSetUp()
    
    @parameterized.expand([
        ('20:00', '07:00'),
        ('19:01', '7:59'),
        ('23:15', '23:30')
    ])
    @pytest.mark.TesteFuncional
    def test_diaria_noturna(self, hora_entrada, hora_saida):
        actual = self.factory.cria_por_hora(hora_entrada, hora_saida)
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
        actual = self.factory.cria_por_acesso(tipo_acesso)
        self.assertEqual(actual, preco_total)


class TestValorContratante(TestCase, TestEstacionamentoMixin):

    def setUp(self):
        self.defaultSetUp()

    @parameterized.expand([
        ([('acesso', "Evento"), ('hora', '08:30', '18:30'), ('hora', '08:30', '09:10')], 130),
        ([('hora', '20:00', '07:00'), ('hora', '08:30', '10:30'), ('acesso', "Mensalista"), ('hora', '08:30', '09:30')], 480),
        ([('acesso', "Mensalista"), ('acesso', "Evento")], 325)
    ])
    @pytest.mark.TesteFuncional
    def test_calcula_retorno_com_multiplos_acessos(self, entradas, expected):
        for entrada in entradas:
            getattr(self.factory, f'cria_por_{entrada[0]}')(*entrada[1:])
        self.assertEqual(expected, self.estacionamento.retorno_contratante)
