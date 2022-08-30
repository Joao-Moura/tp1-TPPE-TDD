from math import ceil

from classes.generico import ObjetoGenerico
from excecoes.excecao import *


class Estacionamento(ObjetoGenerico):
    def __init__(
            self,
            porcentagem_contratante,
            capacidade,
            valor_fracao=None, 
            desconto_hora_cheia=None,
            diaria_diurna=None,
            desconto_diaria=None,
            entrada_noturna=None,
            saida_noturna=None,
            valor_mensal=None,
            valor_evento=None
        ):

        args_branco_estacionamento = self.existe_argumentos_em_branco({
            'porcentagem_contratante': porcentagem_contratante,
            'capacidade': capacidade,
            'valor_fracao': valor_fracao, 
            'desconto_hora_cheia': desconto_hora_cheia,
            'diaria_diurna': diaria_diurna,
            'desconto_diaria': desconto_diaria,
            'entrada_noturna': entrada_noturna,
            'saida_noturna': saida_noturna,
            'valor_mensal': valor_mensal,
            'valor_evento': valor_evento
        })

        if args_branco_estacionamento:
            raise DescricaoEmBrancoException(f'O(s) seguinte(s) argumento(s) está(ão) em branco: {args_branco_estacionamento}.')

        args_negativos = self.valida_argumento_positivos({
            'porcentagem_contratante': porcentagem_contratante,
            'capacidade': capacidade,
            'valor_fracao': valor_fracao, 
            'desconto_hora_cheia': desconto_hora_cheia,
            'diaria_diurna': diaria_diurna,
            'desconto_diaria': desconto_diaria,
            'valor_mensal': valor_mensal,
            'valor_evento': valor_evento
        })
        if args_negativos:
            raise ValorAcessoInvalidoException(f'Não pode haver valores de acesso inválidos, existem alguns negativos: {args_negativos}')
        
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

        self.capacidade = capacidade
        self.estacionados = dict()

    @property
    def hora_cheia_descontada(self):
        # NOTE: Função usada para cálculo de uma hora cheia descontada
        return self.valor_fracao * 4 * ((100 - self.desconto_hora_cheia) / 100)

    @property
    def horarios_ordenados(self):
        # NOTE: Função que ordena todos os carros estacionados (por hora) pelo seu horário de saida
        return sorted(filter(lambda v: True if v[1][0] == 'H' else False, self.estacionados.items()), key=lambda v: v[1][2])

    def valida_dados_preenchidos(self, placa, hora_inicial, hora_final, tipo_acesso):
        args_branco = self.existe_argumentos_em_branco({'placa':placa, 'hora_inicial':hora_inicial, 'hora_final':hora_final})
        if args_branco and not tipo_acesso:
            raise DescricaoEmBrancoException(f'O(s) seguinte(s) argumento(s) está(ão) em branco: {args_branco}.')

    def valida_hora_ou_acesso(self, hora_inicial, hora_final, tipo_acesso):
        if hora_inicial and hora_inicial and tipo_acesso:
            raise MultiplosArgumentosException('Impossível utilizar tipo de acesso em conjunto com horas.')

    def valida_se_carro_ja_estacionado(self, placa, hora_inicial, tipo_acesso):
        if self.estacionados.get(placa) and ((self.estacionados[placa] == ('A', tipo_acesso)) or self.estacionados[placa][2] > hora_inicial):
            raise VagaInvalidaException(f'Veículo com placa {placa} já se encontra no estacionamento.')

    def valida_capacidade_e_libera(self, hora_inicial, tipo_acesso):
        if self.capacidade == len(self.estacionados):
            if tipo_acesso or hora_inicial < self.horarios_ordenados[0][1][2]:
                raise VagaInvalidaException('Estacionamento lotado.')
            else:
                del self.estacionados[self.horarios_ordenados[0][0]]

    def valida_atributos(self, placa, hora_inicial, hora_final, tipo_acesso):
        self.valida_dados_preenchidos(placa, hora_inicial, hora_final, tipo_acesso)
        self.valida_hora_ou_acesso(hora_inicial, hora_final, tipo_acesso)
        self.valida_se_carro_ja_estacionado(placa, hora_inicial, tipo_acesso)
        self.valida_capacidade_e_libera(hora_inicial, tipo_acesso)

    def calcula_preco(self, placa=None, hora_inicial=None, hora_final=None, tipo_acesso=""):
        self.valida_atributos(placa, hora_inicial, hora_final, tipo_acesso)

        self.estacionados[placa] = ('A', tipo_acesso) if tipo_acesso else ('H', hora_inicial, hora_final)
        valor_estacionamento = 0

        if tipo_acesso:
            valor_estacionamento = self.calcula_por_tipo_de_acesso(tipo_acesso)
        else:
            valor_estacionamento = self.calcula_por_horas(hora_inicial, hora_final)

        self.retorno_contratante += (valor_estacionamento * (self.porcentagem_contratante / 100))
        return valor_estacionamento

    def calcula_por_tipo_de_acesso(self, tipo_acesso):
        if tipo_acesso == "Mensalista":
            return self.valor_mensal
        return self.valor_evento

    def calcula_por_horas(self, hora_inicial, hora_final):
        fracoes = ceil((hora_final - hora_inicial).seconds / (60 * 15))
        if hora_inicial > self.entrada_noturna and (hora_final < self.saida_noturna or hora_final > self.entrada_noturna):
            return self.diaria_diurna * (self.desconto_diaria / 100)
        elif fracoes > 36:
            return self.diaria_diurna
        elif fracoes >= 4:
            return ((fracoes // 4) * self.hora_cheia_descontada) + (fracoes % 4) * self.valor_fracao
        return fracoes * self.valor_fracao
