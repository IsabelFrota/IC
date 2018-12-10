import numpy as np
import operator
import pandas as pd


def distancia_euclidiana(data1, data2, tamanho):
    distance = 0
    for x in range(tamanho):
        distance += np.square(data1[x] - data2[x])
    return np.sqrt(distance)


def dmc(conj_treino, conj_teste):
    classes = ['Iris-setosa', 'Iris-versicolor', 'Iris-virginica']
    centroides = [[0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0]]
    cont = 0
    for x in range(len(classes)):
        for y in range(len(conj_treino)):
            atual = [conj_treino.iloc[y]['SepalLength'], conj_treino.iloc[y]['SepalWidth'],
                       conj_treino.iloc[y]['PetalLength'], conj_treino.iloc[y]['PetalWidth']]
            iris_class = conj_treino.iloc[y][-1]
            if iris_class == classes[x]:
                cont += 1
                centroides[x] = [centroides[x][0] + atual[0], centroides[x][1] + atual[1],
                                centroides[x][2] + atual[2], centroides[x][3] + atual[3]]

        for i in range(len(centroides[x])):
            centroides[x][i] = centroides[x][i] / cont

        centroides[x].append(classes[x])
        cont = 0

    centroides_teste = pd.DataFrame(centroides)
    distancias = {}

    tamanho = conj_teste.shape[1]
    for x in range(len(centroides_teste)):
        dist = distancia_euclidiana(conj_teste, centroides_teste.iloc[x], tamanho)
        distancias[x] = dist[0]

    sorted_d = sorted(distancias.items(), key=operator.itemgetter(1))

    vizinho = sorted_d[0][0]
    resp = centroides_teste.iloc[vizinho][4]

    return resp, vizinho

def knn(conj_treino, conj_teste, k):
    distancias = {}
    tamanho = conj_teste.shape[1]

    for x in range(len(conj_treino)):
        dist = distancia_euclidiana(conj_teste, conj_treino.iloc[x], tamanho)
        distancias[x] = dist[0]

    sorted_d = sorted(distancias.items(), key=operator.itemgetter(1))

    vizinhos = []

    for x in range(k):
        vizinhos.append(sorted_d[x][0])
    votos = {}

    for x in range(len(vizinhos)):
        resp = conj_treino.iloc[vizinhos[x]][-1]

        if resp in votos:
            votos[resp] += 1
        else:
            votos[resp] = 1

    votos_ord = sorted(votos.items(), key=operator.itemgetter(1), reverse=True)
    return votos_ord[0][0], vizinhos

def nn(conj_treino, conj_teste):
    distancias = {}
    tamanho = conj_teste.shape[1]

    for x in range(len(conj_treino)):
        dist = distancia_euclidiana(conj_teste, conj_treino.iloc[x], tamanho)
        distancias[x] = dist[0]

    sorted_d = sorted(distancias.items(), key=operator.itemgetter(1))

    vizinho = sorted_d[0][0]
    resp = conj_treino.iloc[vizinho][-1]

    return resp, vizinho

data = pd.read_csv("iris.csv")
teste = [[7.5, 3.4, 5.0, 2.4]]
res = pd.DataFrame(teste)
k = 5
res1, n1 = nn(data, res)
res2, n2 = knn(data, res, k)
res3, n3 = dmc(data, res)

print("\nResultados: ")
print("DMC\n\tResultado: {} - Vizinho(Centroide): {}".format(res3, n3))
print("NN\n\tResultado: {} - Vizinho: {}".format(res1, n1))
print("KNN\n\tResultado: {} - Vizinho: {}".format(res2, n2))
