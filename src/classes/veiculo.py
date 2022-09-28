from classes.generico import ObjetoGenerico
from excecoes.excecao import (
    DescricaoEmBrancoException, MultiplosArgumentosException
)


class Veiculo(ObjetoGenerico):
    def __init__(self, placa=None, hora_inicial=None, hora_final=None, tipo_acesso=""):
        self.placa = placa
        self.hora_inicial = hora_inicial
        self.hora_final = hora_final
        self.tipo_acesso = tipo_acesso

        self.valida_dados_preenchidos()
        self.valida_hora_ou_acesso()

    def valida_dados_preenchidos(self):
        args_branco = self.existe_argumentos_em_branco(
            {
                "placa": self.placa,
                "hora_inicial": self.hora_inicial,
                "hora_final": self.hora_final,
            }
        )
        if args_branco and not self.tipo_acesso:
            raise DescricaoEmBrancoException(
                f"O(s) seguinte(s) argumento(s) está(ão) em branco: {args_branco}."
            )

    def valida_hora_ou_acesso(self):
        if self.hora_inicial and self.hora_inicial and self.tipo_acesso:
            raise MultiplosArgumentosException(
                "Impossível utilizar tipo de acesso em conjunto com horas."
            )

    def retorna_entrada(self):
        if self.tipo_acesso:
            return (self.TIPO_ACESSO, self.tipo_acesso)
        return (self.TIPO_HORAS, self.hora_inicial, self.hora_final)
