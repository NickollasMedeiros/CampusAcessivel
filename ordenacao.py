def indice_prioridade(barreira, pesos):
    beneficio = (barreira["gravidade"] * pesos["gravidade"] +
                 (barreira["pessoas_dia"] / 100) * pesos["pessoas_dia"])
    return beneficio / (barreira["custo"] / 1000)


def calcular_indices(lista, pesos):
    for barreira in lista:
        barreira["indice"] = indice_prioridade(barreira, pesos)
    return lista


def _depois(esquerda, direita, chave, crescente):
    valor_esquerda = esquerda[chave]
    valor_direita = direita[chave]
    if valor_esquerda == valor_direita:
        if chave == "indice":
            return esquerda["codigo"] > direita["codigo"]
        return esquerda["codigo"] > direita["codigo"]
    if crescente:
        return valor_esquerda > valor_direita
    return valor_esquerda < valor_direita


def bubble_sort(lista, chave="indice", crescente=False):
    resultado = lista[:]
    comparacoes = 0
    trocas = 0
    limite = len(resultado) - 1
    while limite > 0:
        trocou = False
        for indice in range(limite):
            comparacoes += 1
            if _depois(resultado[indice], resultado[indice + 1], chave, crescente):
                resultado[indice], resultado[indice + 1] = resultado[indice + 1], resultado[indice]
                trocas += 1
                trocou = True
        if not trocou:
            break
        limite -= 1
    return resultado, comparacoes, trocas


def selection_sort(lista, chave="indice", crescente=False):
    resultado = lista[:]
    comparacoes = 0
    trocas = 0
    for inicio in range(len(resultado) - 1):
        melhor = inicio
        for indice in range(inicio + 1, len(resultado)):
            comparacoes += 1
            if _depois(resultado[melhor], resultado[indice], chave, crescente):
                melhor = indice
        if melhor != inicio:
            resultado[inicio], resultado[melhor] = resultado[melhor], resultado[inicio]
            trocas += 1
    return resultado, comparacoes, trocas


def insertion_sort(lista, chave="indice", crescente=False):
    resultado = lista[:]
    comparacoes = 0
    trocas = 0
    for indice in range(1, len(resultado)):
        atual = resultado[indice]
        posicao = indice - 1
        while posicao >= 0:
            comparacoes += 1
            if not _depois(resultado[posicao], atual, chave, crescente):
                break
            resultado[posicao + 1] = resultado[posicao]
            trocas += 1
            posicao -= 1
        resultado[posicao + 1] = atual
    return resultado, comparacoes, trocas


def confere_com_o_python(ordenada, chave, crescente):
    esperado = sorted(ordenada, key=lambda item: item[chave], reverse=not crescente)
    for indice in range(len(ordenada)):
        if ordenada[indice][chave] != esperado[indice][chave]:
            return False
    return True