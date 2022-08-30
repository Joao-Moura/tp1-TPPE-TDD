class ObjetoGenerico:

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

