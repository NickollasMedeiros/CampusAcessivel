"""
Módulo de Busca - Campus Acessível
Implementa busca sequencial, busca binária iterativa e busca binária recursiva.
Cada função devolve (posicao, comparacoes), onde posicao e o indice do registro
na lista (ou -1 se nao encontrado) e comparacoes e a quantidade de verificacoes feitas.
"""


def busca_sequencial(lista, codigo):
    """
    Percorre a lista elemento por elemento procurando pelo código informado.
    Devolve (posicao, comparacoes); -1 se não encontrar.
    Não exige que a lista esteja ordenada.
    """
    comparacoes = 0
    for indice, item in enumerate(lista):
        comparacoes += 1
        if item["codigo"] == codigo:
            return indice, comparacoes
    return -1, comparacoes


def busca_binaria_iterativa(lista, codigo):
    """
    Realiza a busca binária de forma iterativa utilizando divisões sucessivas.
    Exige que a lista esteja ordenada pelo campo 'codigo'.
    Devolve (posicao, comparacoes); -1 se não encontrar.
    """
    inicio = 0
    fim = len(lista) - 1
    comparacoes = 0
    while inicio <= fim:
        meio = (inicio + fim) // 2
        comparacoes += 1
        if lista[meio]["codigo"] == codigo:
            return meio, comparacoes
        elif lista[meio]["codigo"] < codigo:
            inicio = meio + 1
        else:
            fim = meio - 1
    return -1, comparacoes


def busca_binaria_recursiva(lista, codigo, inicio=0, fim=None, contador=None):
    """
    Realiza a busca binária de forma recursiva.
    Exige que a lista esteja ordenada pelo campo 'codigo'.
    Devolve (posicao, comparacoes); -1 se não encontrar.
    
    Possui dois casos base identificados em comentários:
    1. Intervalo esgotado (chave não encontrada)
    2. Elemento encontrado na posição média
    """
    if contador is None:
        contador = [0]
    if fim is None:
        fim = len(lista) - 1

    # Caso base 1: o intervalo tornou-se invalido (inicio > fim), codigo inexistente.
    if inicio > fim:
        return -1, contador[0]

    meio = (inicio + fim) // 2
    contador[0] += 1

    # Caso base 2: o elemento do meio possui exatamente o codigo procurado.
    if lista[meio]["codigo"] == codigo:
        return meio, contador[0]
    elif lista[meio]["codigo"] < codigo:
        return busca_binaria_recursiva(lista, codigo, meio + 1, fim, contador)
    else:
        return busca_binaria_recursiva(lista, codigo, inicio, meio - 1, contador)

