from datetime import timedelta

import pytest
from unittest import TestCase

from classes.estacionamento import Estacionamento


class TestFacaoQuinze(TestCase):
    
    def setUp(self):
        self.estacionamento = Estacionamento(valor_fracao=30)

    @pytest.mark.TesteFuncional
    def test_cadastro_fracao_um(self):
        actual = self.estacionamento.calcula_preco(
            timedelta(hours=8, minutes=30), timedelta(hours=8, minutes=56))
        self.assertEqual(actual, 60)

    @pytest.mark.TesteFuncional
    def test_cadastro_fracao_dois(self):
        actual = self.estacionamento.calcula_preco(
            timedelta(hours=18, minutes=40), timedelta(hours=19, minutes=20))
        self.assertEqual(actual, 90)
