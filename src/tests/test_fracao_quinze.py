from datetime import time

import pytest
from unittest import TestCase

from classes.estacionamento import Estacionamento


class TestFacaoQuinze(TestCase):
    
    def setUp(self):
        self.estacionamento = Estacionamento(valor_fracao=30)

    @pytest.mark.TesteFuncional
    def test_cadastro_uma_fracao(self):
        actual = self.estacionamento.calcula_preco(
            time.fromisoformat('08:30'), time.fromisoformat('08:56'))
        self.assertEqual(actual, 60)
