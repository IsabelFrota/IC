import math


class ArvoreDecisao:
    def __init__(self):
        pass

    def ler_arquivo(self, filename):
        arquivo = open(filename, "r")
        data = []
        d = []
        for line in arquivo.readlines():
            d.append(line.strip())
        for d1 in d:
            data.append(d1.split(","))
        arquivo.close()

        self.nomeCaracteristicas = self.get_caracteristicas(data)
        data = data[1:]
        self.classes = self.get_classes(data)
        data = self.get_dados_puros(data)

        return data, self.classes, self.nomeCaracteristicas

    def get_classes(self, data):
        data = data[1:]
        classes = []
        for d in range(len(data)):
            classes.append(data[d][-1])

        return classes

    def get_caracteristicas(self, data):
        caracteristicas = data[0]
        caracteristicas = caracteristicas[:-1]
        return caracteristicas

    def get_dados_puros(self, linha):
        linha = linha[1:]
        for d in range(len(linha)):
            linha[d] = linha[d][:-1]
        return linha

    def zero_list(self, size):
        d = []
        for i in range(size):
            d.append(0)
        return d

    def get_argmax(self, arr):
        m = max(arr)
        ix = arr.index(m)
        return ix

    def get_valores_diferentes(self, data_list):
        valores_diferentes = []
        for item in data_list:
            if valores_diferentes.count(item) == 0:
                valores_diferentes.append(item)
        return valores_diferentes

    def get_valores_diferentes_tabela(self, data_table, coluna):
        valores_diferentes= []
        for row in data_table:
            if valores_diferentes.count(row[coluna]) == 0:
                valores_diferentes.append(row[coluna])
        return valores_diferentes

    def get_entropia(self, p):
        if p != 0:
            return -p * math.log(p + 1e-30, 2)
        else:
            return 0

    def criar_arvore(self, dados_treino, classes, caracteristicas, nivel_max=-1, nivel=0):
        n_data = len(dados_treino)
        n_features = len(caracteristicas)

        try:
            self.nomeCaracteristicas
        except:
            self.nomeCaracteristicas = caracteristicas

        novas_classes = self.get_valores_diferentes(classes)
        frequencia = self.zero_list(len(novas_classes))
        entropia_total = 0
        index = 0
        for a_class in novas_classes:
            frequencia[index] = classes.count(a_class)
            prob = float(frequencia[index]) / n_data
            entropia_total += self.get_entropia(prob)
            index += 1

        default = classes[self.get_argmax(frequencia)]
        if n_data == 0 or n_features == 0 or (0 <= nivel_max < nivel):
            return default
        elif classes.count(classes[0]) == n_data:
            return classes[0]
        else:
            ganho = self.zero_list(n_features)
            for caracteristica in range(n_features):
                g = self.get_ganho(dados_treino, classes, caracteristica)
                ganho[caracteristica] = entropia_total - g

            melhor_caracteristica = self.get_argmax(ganho)
            nova_arvore = {caracteristicas[melhor_caracteristica]: {}}

            values = self.get_valores_diferentes_tabela(dados_treino, melhor_caracteristica)
            for value in values:
                novo_dado = []
                novas_classes = []
                index = 0
                for linha in dados_treino:
                    if linha[melhor_caracteristica] == value:
                        if melhor_caracteristica == 0:
                            nova_linha = linha[1:]
                            novo_nome = caracteristicas[1:]
                        elif melhor_caracteristica == n_features:
                            nova_linha = linha[:-1]
                            novo_nome = caracteristicas[:-1]
                        else:
                            nova_linha = linha[:melhor_caracteristica]
                            nova_linha.extend(linha[melhor_caracteristica + 1:])
                            novo_nome = caracteristicas[:melhor_caracteristica]
                            novo_nome.extend(caracteristicas[melhor_caracteristica + 1:])
                        novo_dado.append(nova_linha)
                        novas_classes.append(classes[index])
                    index += 1

                sub_arvore = self.criar_arvore(novo_dado, novas_classes, novo_nome, nivel_max, nivel + 1)

                nova_arvore[caracteristicas[melhor_caracteristica]][value] = sub_arvore
            return nova_arvore

    def get_ganho(self, data, classes, feature):
        ganho = 0
        ndata = len(data)

        values = self.get_valores_diferentes_tabela(data, feature)
        qtd_caracteristicas = self.zero_list(len(values))
        entropia = self.zero_list(len(values))
        value_index = 0
        for value in values:
            data_index = 0
            novas_classes = []
            for linha in data:
                if linha[feature] == value:
                    qtd_caracteristicas[value_index] += 1
                    novas_classes.append(classes[data_index])
                data_index += 1

            valores_classes = self.get_valores_diferentes(novas_classes)
            qtd_classes = self.zero_list(len(valores_classes))
            index_classes = 0
            for classValue in valores_classes:
                for aclass in novas_classes:
                    if aclass == classValue:
                        qtd_classes[index_classes] += 1
                index_classes += 1

            for index_classes in range(len(valores_classes)):
                pr = float(qtd_classes[index_classes]) / sum(qtd_classes)
                entropia[value_index] += self.get_entropia(pr)

            pn = float(qtd_caracteristicas[value_index]) / ndata
            ganho = ganho + pn * entropia[value_index]

            value_index += 1
        return ganho

    def mostrar_arvore(self, dic, separador):
        if type(dic) == dict:
            for item in dic.items():
                print(separador, item[0])
                self.mostrar_arvore(item[1], separador + " | ")
        else:
            print(separador + " -> (", dic + ")")

arvore = ArvoreDecisao()
dados_treino, class_, atributos = arvore.ler_arquivo('restaurante.dat')

res = arvore.criar_arvore(dados_treino, class_, atributos)

arvore.mostrar_arvore(res, ' ')