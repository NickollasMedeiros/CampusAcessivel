import json


CAMPOS = [
    "caminho", "codigo", "ambiente", "tipo", "descricao", "medida",
    "unidade", "referencia_norma", "gravidade", "pessoas_dia", "custo",
    "intervencao", "coletado_por", "data_coleta"
]


def _numero(valor):
    return float(valor.strip().replace(",", "."))


def validar_registro(barreira, codigos_usados=None):
    problemas = []
    if codigos_usados is None:
        codigos_usados = []

    for campo in CAMPOS:
        if campo not in barreira or str(barreira[campo]).strip() == "":
            problemas.append("campo ausente: " + campo)

    codigo = barreira.get("codigo", "")
    if codigo in codigos_usados:
        problemas.append("codigo repetido: " + codigo)

    try:
        gravidade = int(barreira.get("gravidade", 0))
        if gravidade < 1 or gravidade > 5:
            problemas.append("gravidade deve estar entre 1 e 5")
    except (TypeError, ValueError):
        problemas.append("gravidade invalida")

    try:
        if float(barreira.get("custo", 0)) <= 0:
            problemas.append("custo deve ser maior que zero")
    except (TypeError, ValueError):
        problemas.append("custo invalido")

    try:
        if float(barreira.get("medida", 0)) < 0:
            problemas.append("medida nao pode ser negativa")
    except (TypeError, ValueError):
        problemas.append("medida invalida")

    if len(str(barreira.get("descricao", "")).strip()) < 15:
        problemas.append("descricao curta demais")
    return problemas


def validar_setor(no, codigos=None):
    if codigos is None:
        codigos = []
    problemas = []
    for barreira in no.get("barreiras", []):
        problemas_registro = validar_registro(barreira, codigos)
        problemas.extend(problemas_registro)
        codigo = barreira.get("codigo")
        if codigo not in codigos:
            codigos.append(codigo)
    for subsetor in no.get("subsetores", []):
        problemas.extend(validar_setor(subsetor, codigos))
    return problemas


def importar_ficha_campo(caminho):
    registros = []
    erros = []
    with open(caminho, "r", encoding="utf-8") as arquivo:
        linhas = arquivo.readlines()

    for numero_linha, linha in enumerate(linhas[1:], 2):
        if not linha.strip():
            continue
        campos = linha.rstrip("\n").split(";")
        if len(campos) != len(CAMPOS):
            erros.append("linha {}: esperados 14 campos".format(numero_linha))
            continue
        registro = {}
        for indice, campo in enumerate(CAMPOS):
            registro[campo] = campos[indice].strip()
        try:
            registro["medida"] = _numero(registro["medida"])
            registro["referencia_norma"] = _numero(registro["referencia_norma"])
            registro["gravidade"] = int(registro["gravidade"])
            registro["pessoas_dia"] = int(registro["pessoas_dia"])
            registro["custo"] = _numero(registro["custo"])
        except (TypeError, ValueError):
            erros.append("linha {}: valor numerico invalido".format(numero_linha))
            continue
        problemas = validar_registro(registro)
        if problemas:
            erros.append("linha {}: {}".format(numero_linha, ", ".join(problemas)))
        else:
            registros.append(registro)
    return registros, erros


def registros_para_setor(registros):
    raiz = {"nome": "Academia Fusion", "barreiras": [], "subsetores": []}
    for registro in registros:
        partes = [parte.strip() for parte in registro["caminho"].split(">")]
        no = raiz
        for parte in partes[1:]:
            encontrado = None
            for subsetor in no["subsetores"]:
                if subsetor["nome"] == parte:
                    encontrado = subsetor
                    break
            if encontrado is None:
                encontrado = {"nome": parte, "barreiras": [], "subsetores": []}
                no["subsetores"].append(encontrado)
            no = encontrado
        no["barreiras"].append(registro)
    return raiz


def gravar_inventario(caminho, setor):
    with open(caminho, "w", encoding="utf-8") as arquivo:
        json.dump(setor, arquivo, ensure_ascii=False, indent=2)


def ler_inventario(caminho):
    with open(caminho, "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)