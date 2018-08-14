# coding=utf-8
class Margem:
    def __init__(self, margem_a_missionario, margem_b_missionario, margem_a_canibal, margem_b_canibal, margem):
        self.margem_a_missionario = margem_a_missionario
        self.margem_b_missionario = margem_b_missionario
        self.margem_a_canibal = margem_a_canibal
        self.margem_b_canibal = margem_b_canibal
        self.margem = margem
        self.pai = None
        self.filho = []

    def estado_esperado(self):
        resultado_margem_a = self.margem_a_missionario == self.margem_a_canibal == 0
        resultado_margem_b = self.margem_b_missionario == self.margem_b_canibal == 3
        return resultado_margem_a and resultado_margem_b

    def estado_possivel(self):
        if (self.margem_a_missionario < 0) or (self.margem_b_missionario < 0) or (self.margem_a_canibal < 0) or (
                self.margem_b_canibal < 0):
            return False
        else:
            return ((self.margem_a_missionario == 0 or self.margem_a_missionario >= self.margem_a_canibal) and
                    (self.margem_b_missionario == 0 or self.margem_b_missionario >= self.margem_b_canibal))



    def geracao_possibilidades(self):
        nova_margem = 'B' if self.margem == 'A' \
            else 'A'
        estados_possiveis = [
            {'miss': 1, 'cani': 1},
            {'miss': 0, 'cani': 1},
            {'miss': 0, 'cani': 2},
            {'miss': 2, 'cani': 0},
            {'miss': 1, 'cani': 0}
           ,
        ]
        for estado in estados_possiveis:
            if self.margem == 'A':
                canibal_margem_a = self.margem_a_canibal - estado['cani']
                canibal_margem_b = self.margem_b_canibal + estado['cani']
                missionario_margem_a = self.margem_a_missionario - estado['miss']
                missionario_margem_b = self.margem_b_missionario + estado['miss']

            else:
                canibal_margem_b = self.margem_b_canibal - estado['cani']
                canibal_margem_a = self.margem_a_canibal + estado['cani']
                missionario_margem_b = self.margem_b_missionario - estado['cani']
                missionario_margem_a = self.margem_a_missionario + estado['miss']

            possibilidade = Margem(missionario_margem_a, missionario_margem_b, canibal_margem_a,
                         canibal_margem_b, nova_margem)
            possibilidade.pai = self
            if possibilidade.estado_possivel():
                self.filho.append(possibilidade)

    def __str__(self):
        return '    MARGEM A     |     |    MARGEM B \n Missionários: {} | RIO | Missionários: {}\n Canibais:     {} |     | Canibais:     {}'.format(
            self.margem_a_missionario, self.margem_b_missionario, self.margem_a_canibal, self.margem_b_canibal
        )
class MissionarioXCanibal:
    def __init__(self):
        self.arvore = [Margem(3, 0, 3, 0, 'A')]
        self.solucao = None

    def gerar_solucao(self):
        for element in self.arvore:
            if element.estado_esperado():
                self.solucao = [element]
                while element.pai:
                    self.solucao.insert(0, element.pai)
                    element = element.pai
                break
            element.geracao_possibilidades()
            self.arvore.extend(element.filho)


problem = MissionarioXCanibal()
problem.gerar_solucao()
for state in problem.solucao:
    print 42 * '-'
    print state
    print 42 * '-'