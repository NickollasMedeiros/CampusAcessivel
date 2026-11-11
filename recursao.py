import ordenacao


def custo_total(no):
    # Caso base: se o nó não tiver barreiras nem subsetores, o custo é zero.
    total = 0.0
    for barreira in no.get("barreiras", []):
        total += barreira["custo"]
    for subsetor in no.get("subsetores", []):
        total += custo_total(subsetor)
    return total


def contar_barreiras(no):
    # Caso base: se o nó não tiver barreiras nem subsetores, a contagem é zero.
    total = len(no.get("barreiras", []))
    for subsetor in no.get("subsetores", []):
        total += contar_barreiras(subsetor)
    return total


def contar_por_tipo(no, tipo):
    # Caso base: se o nó estiver vazio, não há barreiras desse tipo para contar.
    total = 0
    for barreira in no.get("barreiras", []):
        if barreira["tipo"] == tipo:
            total += 1
    for subsetor in no.get("subsetores", []):
        total += contar_por_tipo(subsetor, tipo)
    return total


def profundidade(no):
    # Caso base: se o nó não tiver subsetores, ele é uma folha de profundidade 1.
    if len(no.get("subsetores", [])) == 0:
        return 1
    maior = 0
    for subsetor in no["subsetores"]:
        atual = profundidade(subsetor)
        if atual > maior:
            maior = atual
    return maior + 1


def achatar(no, caminho=""):
    # Caso base: se o nó for uma folha, retorna apenas suas próprias barreiras.
    caminho_atual = caminho
    if caminho_atual == "":
        caminho_atual = no["nome"]
    resultado = []
    for barreira in no.get("barreiras", []):
        copia = barreira.copy()
        copia["caminho"] = caminho_atual
        resultado.append(copia)
    for subsetor in no.get("subsetores", []):
        proximo = caminho_atual + " > " + subsetor["nome"]
        resultado.extend(achatar(subsetor, proximo))
    return resultado


def caminho_da_barreira(no, codigo, caminho=""):
    # Caso base: se a folha não tiver o código, encerra a busca nesse ramo.
    caminho_atual = caminho
    if caminho_atual == "":
        caminho_atual = no["nome"]
    for barreira in no.get("barreiras", []):
        if barreira["codigo"] == codigo:
            return caminho_atual
    for subsetor in no.get("subsetores", []):
        proximo = caminho_atual + " > " + subsetor["nome"]
        encontrado = caminho_da_barreira(subsetor, codigo, proximo)
        if encontrado is not None:
            return encontrado
    return None


def resumo_hierarquico(no, nivel=0):
    recuo = "  " * nivel
    print("{}{} - {} barreiras - R$ {:.2f}".format(
        recuo, no["nome"], contar_barreiras(no), custo_total(no)))
    # Caso base: quando o nó não possui subsetores, o laço for não é executado e a chamada retorna.
    for subsetor in no.get("subsetores", []):
        resumo_hierarquico(subsetor, nivel + 1)


def podar_inviaveis(barreiras, orcamento):
    """
    Descarta as barreiras cujo custo individual excede o orçamento total disponível.
    Esta é uma poda prévia legítima porque itens que sozinhos estouram o teto
    jamais poderão compor qualquer solução válida.
    """
    candidatos = []
    for barreira in barreiras:
        if barreira["custo"] <= orcamento:
            candidatos.append(barreira)
    return candidatos


def pacote_guloso(barreiras, orcamento, pesos):
    """
    Estratégia gulosa para o problema da mochila/intervenção:
    Ordena pelo índice de prioridade decrescente e inclui barreiras
    enquanto couber no orçamento disponível.
    Devolve (beneficio, custo, lista_de_codigos).
    """
    copia = [b.copy() for b in barreiras]
    ordenacao.calcular_indices(copia, pesos)
    ordenadas, _, _ = ordenacao.insertion_sort(copia, chave="indice", crescente=False)

    beneficio_total = 0.0
    custo_total_acumulado = 0.0
    codigos_escolhidos = []

    for b in ordenadas:
        if custo_total_acumulado + b["custo"] <= orcamento:
            custo_total_acumulado += b["custo"]
            beneficio_total += _beneficio(b, pesos)
            codigos_escolhidos.append(b["codigo"])

    return beneficio_total, custo_total_acumulado, codigos_escolhidos


def melhor_pacote_exaustivo(barreiras, orcamento, pesos, indice=0, contador=None):
    # Caso base: todas as barreiras já foram decididas.
    if contador is None:
        contador = [0]
    contador[0] += 1
    if indice == len(barreiras):
        return 0.0, 0.0, [], contador[0]

    sem_barreira = melhor_pacote_exaustivo(
        barreiras, orcamento, pesos, indice + 1, contador)
    barreira = barreiras[indice]
    com_barreira = None
    if barreira["custo"] <= orcamento:
        restante = melhor_pacote_exaustivo(
            barreiras, orcamento - barreira["custo"], pesos, indice + 1, contador)
        beneficio = restante[0] + _beneficio(barreira, pesos)
        codigos = [barreira["codigo"]] + restante[2]
        com_barreira = (beneficio, restante[1] + barreira["custo"], codigos, contador[0])

    if com_barreira is not None and com_barreira[0] > sem_barreira[0]:
        return com_barreira
    return sem_barreira


def _beneficio(barreira, pesos):
    return (barreira["gravidade"] * pesos["gravidade"] +
            (barreira["pessoas_dia"] / 100) * pesos["pessoas_dia"])
