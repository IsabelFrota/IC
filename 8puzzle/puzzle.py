import random


class Estado:

    def __init__(self, tamanho_n):
        self.tamanho_n = tamanho_n
        self.tamanho_t = pow(self.tamanho_n, 2)
        self.objetivo = range(1, self.tamanho_t)
        self.objetivo.append(0)

    def mostra_estado(self, estado):
        for (indice, valor) in enumerate(estado):
            print ' %s ' % valor,
            if indice in [x for x in range(self.tamanho_n - 1, self.tamanho_t,
                                          self.tamanho_n)]:
                print
        print

    def get_valor(self, key):
        values = [1, -1, self.tamanho_n, -self.tamanho_n]
        valid = []
        for x in values:
            if 0 <= key + x < self.tamanho_t:
                if x == 1 and key in range(self.tamanho_n - 1, self.tamanho_t,
                                           self.tamanho_n):
                    continue
                if x == -1 and key in range(0, self.tamanho_t, self.tamanho_n):
                    continue
                valid.append(x)
        return valid

    def expandir(self, st):
        pexpands = {}
        for key in range(self.tamanho_t):
            pexpands[key] = self.get_valor(key)
        pos = st.index(0)
        moves = pexpands[pos]
        expstates = []
        for mv in moves:
            nstate = st[:]
            (nstate[pos + mv], nstate[pos]) = (nstate[pos], nstate[pos +
                    mv])
            expstates.append(nstate)
        return expstates

    def one_of_poss(self, st):
        exp_sts = self.expandir(st)
        rand_st = random.choice(exp_sts)
        return rand_st

    def inicia_estado(self, seed=1000):
        start_st = self.objetivo[:]
        for sts in range(seed):
            start_st = self.one_of_poss(start_st)
        return start_st

    def objetivo_alcancado(self, st):
        return st == self.objetivo

    def manhattan_distance(self, st):
        mdist = 0
        for node in st:
            if node != 0:
                gdist = abs(self.objetivo.index(node) - st.index(node))
                (jumps, steps) = (gdist // self.tamanho_n, gdist % self.tamanho_n)
                mdist += jumps + steps
        return mdist

    def huristica_proximo_estado(self, st):
        exp_sts = self.expandir(st)
        mdists = []
        for st in exp_sts:
            mdists.append(self.manhattan_distance(st))
        mdists.sort()
        short_path = mdists[0]
        if mdists.count(short_path) > 1:
            least_paths = [st for st in exp_sts if self.manhattan_distance(st) == short_path]
            return random.choice(least_paths)
        else:
            for st in exp_sts:
                if self.manhattan_distance(st) == short_path:
                    return st

    def solucionar(self, st):
        while not self.objetivo_alcancado(st):
            st = self.huristica_proximo_estado(st)
            self.mostra_estado(st)


if __name__ == '__main__':
    print 10 * '-'
    state = Estado(3)
    print 'O Estado Inicial e:'
    start = state.inicia_estado(5)
    state.mostra_estado(start)
    print 'O Objetivo e:'
    state.mostra_estado(state.objetivo)
    print 'Solucao:'
    state.mostra_estado(start)
    state.solucionar(start)