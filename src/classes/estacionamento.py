from math import ceil

from excecoes.excecao import *


class Estacionamento:
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

    def existe_argumentos_em_branco(self, args={}):
        invalidArgs=[]
        for arg, val in args.items():
            if not val:
                invalidArgs.append(arg)
        return invalidArgs

    def calcula_preco(self, placa=None, hora_inicial=None, hora_final=None, tipo_acesso=""):
        valor_estacionamento = 0

        args_branco = self.existe_argumentos_em_branco({'placa':placa, 'hora_inicial':hora_inicial, 'hora_final':hora_final})
        # Levanta exceção caso tenha algum placa, hora_inicial ou hora_final não preenchidos
        if args_branco and not tipo_acesso:
            raise DescricaoEmBrancoException(f'O(s) seguinte(s) argumento(s) está(ão) em branco: {args_branco}.')

        # NOTE: Se o carro já estiver estacionado e seu tipo for de acesso
        # ou se seus horários colidirem, levanta exceção
        if self.estacionados.get(placa) and ((self.estacionados[placa] == ('A', tipo_acesso)) or self.estacionados[placa][2] > hora_inicial):
            raise VagaInvalidaException(f'Veículo com placa {placa} já se encontra no estacionamento.')

        if self.capacidade == len(self.estacionados):
            # NOTE: Se o seu tipo for de acesso ou se o horário do primeiro carro que
            # for sair do estacionamento colidir com o de entrada, levanta exceção.
            # Se não, apaga ele do estacionamento e adiciona o novo
            if tipo_acesso or hora_inicial < self.horarios_ordenados[0][1][2]:
                raise VagaInvalidaException('Estacionamento lotado.')
            else:
                del self.estacionados[self.horarios_ordenados[0][0]]

        self.estacionados[placa] = ('A', tipo_acesso) if tipo_acesso else ('H', hora_inicial, hora_final)

        if tipo_acesso:
            # NOTE: Valor caso ele seja do tipo acesso
            if tipo_acesso == "Mensalista":
                valor_estacionamento = self.valor_mensal
            elif tipo_acesso == "Evento":
                valor_estacionamento = self.valor_evento
        else:
            # NOTE: Valor caso ele seja do tipo hora, para esse caso precisamos
            # saber quantas frações ele gastou dentro do estacionamento
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