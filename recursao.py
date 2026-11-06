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
    for subsetor in no.get("subsetores", []):
        resumo_hierarquico(subsetor, nivel + 1)


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