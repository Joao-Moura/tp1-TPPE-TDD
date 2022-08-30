class ObjetoGenerico:
    QTD_HORA_COMPLETA = 4
    QTD_NOVE_HORAS = 36
    PORCENTAGEM = 100
    SECONDS_TO_HOUR = 900
    MENSALISTA = "Mensalista"
    TIPO_ACESSO = 'A'
    TIPO_HORAS = 'H'

    def existe_argumentos_em_branco(self, args={}):
        invalidArgs=[]
        for arg, val in args.items():
            if not val:
                invalidArgs.append(arg)
        return invalidArgs

    def valida_argumento_positivos(self, args={}):
        invalidArgs=[]
        for arg, val in args.items():
            if val < 0:
                invalidArgs.append(arg)
        return invalidArgs

