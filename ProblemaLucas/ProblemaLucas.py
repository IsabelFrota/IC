from copy import copy


class Estados:
    def __init__(self, estado_inicial, solucao=[" ", "<", "<", "<", "_", ">", ">", ">", " "]):
        self.estado = estado_inicial
        self.solucao = solucao
        self.no_pai = None
        self.no_filho = []

    def estado_esperado(self):
        for j, i in enumerate(self.estado):
            if i != self.solucao[j]:
                return False
        return True

    def estado_possivel(self, estado_atual):
        estado = Estados(estado_atual)
        estado.no_pai = self
        self.no_filho.append(estado)

    def geracao_possibilidades(self):
        for i in range(len(self.estado)):
            estado_copia = copy(self.estado)
            if self.estado[i] == '<':

                if self.estado[i - 1] == '>' and self.estado[i - 2] == '_':
                    estado_copia[i] = self.estado[i - 2]
                    estado_copia[i - 2] = self.estado[i]
                    self.estado_possivel(estado_copia)

                if self.estado[i - 1] == '_':
                    estado_copia[i] = self.estado[i - 1]
                    estado_copia[i - 1] = self.estado[i]
                    self.estado_possivel(estado_copia)

            if self.estado[i] == '>':

                if self.estado[i + 1] == '<' and self.estado[i + 2] == '_':
                    estado_copia[i] = self.estado[i + 2]
                    estado_copia[i + 2] = self.estado[i]
                    self.estado_possivel(estado_copia)

                if self.estado[i + 1] == '_':
                    estado_copia[i] = self.estado[i + 1]
                    estado_copia[i + 1] = self.estado[i]
                    self.estado_possivel(estado_copia)



    def __str__(self):
        resultado = ""
        for i in self.estado[1:-1]:
            resultado += i
        return resultado


class ProblemaLucas:

    def __init__(self):
        self.arvore = [Estados([" ", ">", ">", ">", "_", "<", "<", "<", " "])]
        self.solucao = None

    def gerar_solucao(self):
        for elemento in self.arvore:
            if elemento.estado_esperado():
                self.solucao = [elemento]
                while elemento.no_pai:
                    self.solucao.insert(0, elemento.no_pai)
                    elemento = elemento.no_pai
                break
            elemento.geracao_possibilidades()
            self.arvore.extend(elemento.no_filho)


problemaLuc = ProblemaLucas()
problemaLuc.gerar_solucao()

print "     ESTADO INICIAL "
# i = 1
for i in range(1,len(problemaLuc.solucao)+1):
    print 25 * '-'
    print "\t \t", problemaLuc.solucao[i-1], "\t"
    print 25 * '-'
    if(i == len(problemaLuc.solucao)):
        print "         FIM ",
    else:
        print "      MOVIMENTO", i

# for sol in problemaLuc.solucao:
#     print 25 * '-'
#     print "\t \t", sol, "\t"
#     print 25 * '-'
#     print "      MOVIMENTO ",i
#     i+=1
#
