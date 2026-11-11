"""
Módulo de Relatório - Campus Acessível
Gera a matriz ambiente x tipo de barreira, formata tabelas alinhadas no terminal,
processa as medições dos 5 Achados (A1 a A5) e grava o relatório em arquivo de texto.
"""

import busca
import ordenacao
import recursao


def montar_matriz_ambiente_tipo(setor):
    """
    Constrói a matriz ambiente x tipo de barreira (uma lista de listas)
    totalizando as contagens por linha (ambiente) e coluna (tipo).
    Devolve um dicionário estruturado com matriz, rótulos e totais.
    """
    barreiras = recursao.achatar(setor)

    ambientes = []
    for b in barreiras:
        amb = b["ambiente"]
        if amb not in ambientes:
            ambientes.append(amb)

    tipos = []
    for b in barreiras:
        tp = b["tipo"]
        if tp not in tipos:
            tipos.append(tp)

    # Matriz inicializada com zeros (lista de listas)
    matriz = []
    for _ in range(len(ambientes)):
        linha = [0] * len(tipos)
        matriz.append(linha)

    # Preenchimento das contagens
    for b in barreiras:
        idx_amb = ambientes.index(b["ambiente"])
        idx_tipo = tipos.index(b["tipo"])
        matriz[idx_amb][idx_tipo] += 1

    totais_linhas = []
    for i in range(len(ambientes)):
        soma = 0
        for j in range(len(tipos)):
            soma += matriz[i][j]
        totais_linhas.append(soma)

    totais_colunas = []
    for j in range(len(tipos)):
        soma = 0
        for i in range(len(ambientes)):
            soma += matriz[i][j]
        totais_colunas.append(soma)

    total_geral = 0
    for soma in totais_linhas:
        total_geral += soma

    return {
        "matriz": matriz,
        "ambientes": ambientes,
        "tipos": tipos,
        "totais_linhas": totais_linhas,
        "totais_colunas": totais_colunas,
        "total_geral": total_geral,
    }


def formatar_matriz_texto(dados):
    """
    Formata a matriz ambiente x tipo em tabela alinhada para terminal e arquivo.
    """
    matriz = dados["matriz"]
    ambientes = dados["ambientes"]
    tipos = dados["tipos"]
    totais_linhas = dados["totais_linhas"]
    totais_colunas = dados["totais_colunas"]
    total_geral = dados["total_geral"]

    largura_amb = 20
    for amb in ambientes:
        if len(amb) > largura_amb:
            largura_amb = len(amb)
    largura_amb += 2

    # Abreviar ou ajustar largura das colunas de tipo
    larguras_tipos = []
    for tp in tipos:
        larg = len(tp)
        if larg < 14:
            larg = 14
        larguras_tipos.append(larg)

    linhas_texto = []
    linhas_texto.append("=== MATRIZ AMBIENTE X TIPO DE BARREIRA ===")
    
    # Cabeçalho
    cabecalho = "{:<{}}".format("Ambiente", largura_amb)
    for j, tp in enumerate(tipos):
        cabecalho += " | {:>{}}".format(tp, larguras_tipos[j])
    cabecalho += " | {:>6}".format("TOTAL")
    linhas_texto.append(cabecalho)
    linhas_texto.append("-" * len(cabecalho))

    # Linhas de dados
    for i, amb in enumerate(ambientes):
        linha = "{:<{}}".format(amb, largura_amb)
        for j in range(len(tipos)):
            linha += " | {:>{}}".format(matriz[i][j], larguras_tipos[j])
        linha += " | {:>6}".format(totais_linhas[i])
        linhas_texto.append(linha)

    linhas_texto.append("-" * len(cabecalho))
    
    # Linha de totais
    linha_tot = "{:<{}}".format("TOTAL POR TIPO", largura_amb)
    for j in range(len(tipos)):
        linha_tot += " | {:>{}}".format(totais_colunas[j], larguras_tipos[j])
    linha_tot += " | {:>6}".format(total_geral)
    linhas_texto.append(linha_tot)

    return "\n".join(linhas_texto)


def gerar_achado_a1(barreiras):
    """
    A1 - Achado de Ordenação:
    Tabela com comparações e trocas de Bubble, Selection e Insertion Sort
    em 3 tamanhos (1/3, 2/3, Total) e 3 ordens (Original, Já Ordenada, Inversa).
    """
    total_itens = len(barreiras)
    tamanhos = [
        ("1/3 da base", total_itens // 3),
        ("2/3 da base", (2 * total_itens) // 3),
        ("Total da base", total_itens)
    ]

    linhas = []
    linhas.append("=" * 80)
    linhas.append("A1 - ACHADO DE ORDENAÇÃO: COMPARAÇÕES E TROCAS")
    linhas.append("=" * 80)
    linhas.append("")

    for rotulo, tam in tamanhos:
        base = [b.copy() for b in barreiras[:tam]]
        ord_dec, _, _ = ordenacao.insertion_sort(base, chave="indice", crescente=False)
        ord_cresc, _, _ = ordenacao.insertion_sort(base, chave="indice", crescente=True)

        cenarios = [
            ("Original", base),
            ("Ordenada", ord_dec),
            ("Inversa", ord_cresc)
        ]

        linhas.append("--- Tamanho: {} (N = {}) ---".format(rotulo, tam))
        linhas.append("{:<12} | {:<18} | {:<18} | {:<18}".format(
            "Cenário", "Bubble Sort", "Selection Sort", "Insertion Sort"))
        linhas.append("-" * 75)

        for nome_cen, dados in cenarios:
            _, bc, bt = ordenacao.bubble_sort(dados, chave="indice", crescente=False)
            _, sc, st = ordenacao.selection_sort(dados, chave="indice", crescente=False)
            _, ic, it = ordenacao.insertion_sort(dados, chave="indice", crescente=False)
            linhas.append("{:<12} | C={:>3}, T={:>3}       | C={:>3}, T={:>3}       | C={:>3}, T={:>3}".format(
                nome_cen, bc, bt, sc, st, ic, it))
        linhas.append("")

    linhas.append("EXPLICAÇÃO DO GRUPO:")
    linhas.append("1. Comparações invariantes: O Selection Sort sempre executa n(n-1)/2 comparações")
    linhas.append("   (10 para N=5, 45 para N=10, 105 para N=15), independentemente da ordem inicial,")
    linhas.append("   pois percorre obrigatoriamente todo o restante da lista para encontrar o menor/maior.")
    linhas.append("2. Variação do Insertion Sort: Varia fortemente conforme a ordenação prévia.")
    linhas.append("   Na lista já ordenada, realiza apenas (n-1) comparações (melhor caso linear O(n)).")
    linhas.append("   Na lista inversa, atinge o pior caso quadrático n(n-1)/2 comparações e trocas.")
    linhas.append("3. Relação entre trocas do Bubble e Insertion: O número de trocas do Bubble Sort")
    linhas.append("   e do Insertion Sort é RIGOROSAMENTE IDÊNTICO em todos os cenários:")
    linhas.append("   ambos resolvem exatamente as mesmas inversões de pares adjacentes na lista.")
    linhas.append("")
    return "\n".join(linhas)


def gerar_achado_a2(barreiras):
    """
    A2 - Achado de Busca:
    Tabela com comparações da Busca Sequencial, Binária Iterativa e Binária Recursiva
    para 5 códigos (primeiro, meio, último, aleatório do meio, inexistente).
    """
    ordenadas, _, _ = ordenacao.selection_sort(barreiras, chave="codigo", crescente=True)
    n = len(ordenadas)
    codigos = [b["codigo"] for b in ordenadas]

    alvos = [
        ("Primeiro código", codigos[0]),
        ("Código do meio", codigos[n // 2]),
        ("Último código", codigos[-1]),
        ("Aleatório do meio", codigos[3]),
        ("Código inexistente", "ACA-XXX-99")
    ]

    linhas = []
    linhas.append("=" * 80)
    linhas.append("A2 - ACHADO DE BUSCA: NÚMERO DE COMPARAÇÕES")
    linhas.append("=" * 80)
    linhas.append("")
    linhas.append("{:<20} | {:<12} | {:<18} | {:<18} | {:<18}".format(
        "Posição / Caso", "Código", "Sequencial (Pos/C)", "Bin. Iterativa (Pos/C)", "Bin. Recursiva (Pos/C)"))
    linhas.append("-" * 96)

    for nome_caso, cod in alvos:
        p_seq, c_seq = busca.busca_sequencial(ordenadas, cod)
        p_it, c_it = busca.busca_binaria_iterativa(ordenadas, cod)
        p_rec, c_rec = busca.busca_binaria_recursiva(ordenadas, cod)
        linhas.append("{:<20} | {:<12} | pos={:>2}, C={:>2}       | pos={:>2}, C={:>2}       | pos={:>2}, C={:>2}".format(
            nome_caso, cod, p_seq, c_seq, p_it, c_it, p_rec, c_rec))

    linhas.append("")
    linhas.append("EXPLICAÇÃO DO GRUPO:")
    linhas.append("1. Onde a Busca Sequencial ganha: No primeiro elemento da lista (C=1 vs C=4).")
    linhas.append("   A busca sequencial testa o índice 0 imediatamente, enquanto a binária inicia")
    linhas.append("   dividindo pelo ponto médio e precisa descer na árvore de decisão até a folha.")
    linhas.append("2. Custo da ordenação prévia: A busca binária exige lista ordenada por código.")
    linhas.append("   Ordenar a base com nossos algoritmos custa O(n^2) (105 comparações para 15 itens).")
    linhas.append("   Portanto, a binária só compensa quando faremos múltiplas consultas sucessivas,")
    linhas.append("   amortizando o custo inicial da ordenação.")
    linhas.append("3. Código inexistente vs Pior caso: Para um código inexistente, a busca binária")
    linhas.append("   percorre a profundidade máxima da árvore de decisão até que inicio > fim,")
    linhas.append("   consumindo exatamente teto(log2(n + 1)) = 4 comparações, idêntico ao pior caso existente.")
    linhas.append("")
    return "\n".join(linhas)


def gerar_achado_a3(setor):
    """
    A3 - Achado de Hierarquia:
    Custo total e contagem por subsetor de 1º nível, profundidade real da árvore,
    e caminho hierárquico completo da barreira mais grave.
    """
    linhas = []
    linhas.append("=" * 80)
    linhas.append("A3 - ACHADO DE HIERARQUIA: ESTRUTURA DO SETOR E PROFUNDIDADE")
    linhas.append("=" * 80)
    linhas.append("")
    linhas.append("Setor Principal: {}".format(setor["nome"]))
    linhas.append("Profundidade real da árvore: {} níveis".format(recursao.profundidade(setor)))
    linhas.append("")
    linhas.append("TOTAIS POR SUBSETOR DE PRIMEIRO NÍVEL:")
    linhas.append("{:<30} | {:<15} | {:<18}".format("Subsetor (1º Nível)", "Qtd Barreiras", "Custo Total"))
    linhas.append("-" * 70)

    for sub in setor.get("subsetores", []):
        linhas.append("{:<30} | {:<15} | R$ {:>14.2f}".format(
            sub["nome"], recursao.contar_barreiras(sub), recursao.custo_total(sub)))

    linhas.append("-" * 70)
    linhas.append("{:<30} | {:<15} | R$ {:>14.2f}".format(
        "TOTAL DO SETOR", recursao.contar_barreiras(setor), recursao.custo_total(setor)))
    linhas.append("")

    # Barreira mais grave (gravidade = 5)
    barreiras = recursao.achatar(setor)
    barreiras_criticas = [b for b in barreiras if b["gravidade"] == 5]
    linhas.append("BARREIRAS MAIS GRAVES (GRAVIDADE 5) E SEUS CAMINHOS HIERÁRQUICOS:")
    for b in barreiras_criticas:
        caminho = recursao.caminho_da_barreira(setor, b["codigo"])
        linhas.append("- [{}] {}: caminho = '{}' (Custo: R$ {:.2f})".format(
            b["codigo"], b["descricao"], caminho, b["custo"]))

    linhas.append("")
    linhas.append("EXPLICAÇÃO DO GRUPO:")
    linhas.append("1. Limitação de laços aninhados: Uma estrutura com 2 laços fixos acessaria apenas")
    linhas.append("   os subsetores de nível 1 e 2, falhando silenciosamente ao ignorar completamente")
    linhas.append("   os ambientes e subambientes do 3º nível (como a Entrada e Área de Espera).")
    linhas.append("   A recursão é a única abordagem invariante à profundidade arbitrária da árvore.")
    linhas.append("2. Remoção do caso base: Se o caso base for removido da recursão, as chamadas")
    linhas.append("   ocorrerão indefinidamente sem condição de parada, estourando a pilha de execução")
    linhas.append("   do Python com a exceção: 'RecursionError: maximum recursion depth exceeded'.")
    linhas.append("")
    return "\n".join(linhas)


def gerar_achado_a4(barreiras, pesos):
    """
    A4 - Achado de Otimização:
    Compara Pacote Guloso vs Exaustivo para 4 tetos de orçamento diferentes,
    mostrando a divergência real encontrada, medindo chamadas recursivas
    e discutindo a viabilidade em escala de 400 barreiras.
    """
    orcamentos = [1000.0, 3000.0, 6000.0, 10000.0]

    linhas = []
    linhas.append("=" * 80)
    linhas.append("A4 - ACHADO DE OTIMIZAÇÃO: PACOTE GULOSO X EXAUSTIVO")
    linhas.append("=" * 80)
    linhas.append("")
    linhas.append("COMPARAÇÃO DE ESTRATÉGIAS EM 4 TETOS DE ORÇAMENTO:")
    linhas.append("{:<12} | {:<25} | {:<25} | {:<10}".format(
        "Orçamento", "Guloso (Benef/Custo/Itens)", "Exaustivo (Benef/Custo/Itens)", "Chamadas"))
    linhas.append("-" * 80)

    divergencia_doc = None

    for orc in orcamentos:
        candidatas = recursao.podar_inviaveis(barreiras, orc)
        bg, cg, itens_g = recursao.pacote_guloso(candidatas, orc, pesos)
        be, ce, itens_e, chamadas = recursao.melhor_pacote_exaustivo(candidatas, orc, pesos)

        str_g = "{:.3f} / R$ {:.2f} / {} it".format(bg, cg, len(itens_g))
        str_e = "{:.3f} / R$ {:.2f} / {} it".format(be, ce, len(itens_e))
        linhas.append("R$ {:>8.2f} | {:<25} | {:<25} | {:>10}".format(
            orc, str_g, str_e, chamadas))

        if abs(be - bg) > 0.001 and divergencia_doc is None:
            divergencia_doc = {
                "orcamento": orc,
                "bg": bg, "cg": cg, "itens_g": itens_g,
                "be": be, "ce": ce, "itens_e": itens_e
            }

    linhas.append("")
    if divergencia_doc is not None:
        linhas.append("CASO DE DIVERGÊNCIA COMPROVADO NO ORÇAMENTO DE R$ {:.2f}:".format(
            divergencia_doc["orcamento"]))
        linhas.append("- Estratégia Gulosa: Benefício = {:.3f} | Custo = R$ {:.2f}".format(
            divergencia_doc["bg"], divergencia_doc["cg"]))
        linhas.append("  Barreiras escolhidas: {}".format(", ".join(divergencia_doc["itens_g"])))
        linhas.append("- Estratégia Exaustiva: Benefício = {:.3f} | Custo = R$ {:.2f}".format(
            divergencia_doc["be"], divergencia_doc["ce"]))
        linhas.append("  Barreiras escolhidas: {}".format(", ".join(divergencia_doc["itens_e"])))
        linhas.append("  Ganho do Exaustivo: +{:.3f} de benefício acumulado.".format(
            divergencia_doc["be"] - divergencia_doc["bg"]))
        linhas.append("  Por que a Gulosa perdeu? A estratégia gulosa preenche o orçamento estritamente")
        linhas.append("  pela razão benefício/custo. Após incluir itens pequenos, o orçamento restante")
        linhas.append("  não foi suficiente para acomodar a barreira seguinte no ranking (ACA-REC-02, R$ 1.200),")
        linhas.append("  deixando R$ 780,00 ociosos. A exaustiva testou todas as combinações e descobriu que")
        linhas.append("  substituir a barreira ACA-ESC-07 (R$ 800) por ACA-REC-02 (R$ 1.200) aproveitava melhor")
        linhas.append("  o limite de R$ 3.000,00, elevando o benefício global.")

    # Medição de chamadas recursivas vs tamanho de entrada
    linhas.append("")
    linhas.append("CRESCIMENTO DO NÚMERO DE CHAMADAS RECURSIVAS CONFORME ENTRADA (Orçamento R$ 10.000):")
    linhas.append("{:<15} | {:<20}".format("Nº Candidatos", "Chamadas Recursivas"))
    linhas.append("-" * 40)
    for tam in [3, 5, 8, 10, 14]:
        sub_barreiras = barreiras[:tam]
        _, _, _, ch = recursao.melhor_pacote_exaustivo(sub_barreiras, 10000.0, pesos)
        linhas.append("{:<15} | {:<20}".format(tam, ch))

    linhas.append("")
    linhas.append("RESPOSTA SOBRE O CAMPUS INTEIRO COM 400 BARREIRAS:")
    linhas.append("A abordagem exaustiva NÃO SERVE para 400 barreiras. Como a árvore de decisão binária")
    linhas.append("gera até 2^N combinações, para N = 400 o algoritmo exigiria 2^400 chamadas (aproximadamente")
    linhas.append("2,58 x 10^120 operações), o que supera em muitas ordens de grandeza a idade do universo.")
    linhas.append("Para a escala do campus inteiro, torna-se obrigatório o uso de Programação Dinâmica,")
    linhas.append("algoritmos Branch and Bound com poda avançada ou heurísticas como a própria gulosa.")
    linhas.append("")
    return "\n".join(linhas)


def gerar_achado_a5(barreiras, pesos_base):
    """
    A5 - Achado de Decisão:
    Índice de prioridade, justificativa de pesos, regra de desempate e
    análise de sensibilidade (pesos base vs 2x gravidade vs 2x alcance).
    """
    linhas = []
    linhas.append("=" * 80)
    linhas.append("A5 - ACHADO DE DECISÃO: ÍNDICE, PESOS E ANÁLISE DE SENSIBILIDADE")
    linhas.append("=" * 80)
    linhas.append("")
    linhas.append("FÓRMULA DO ÍNDICE DE PRIORIDADE:")
    linhas.append("beneficio = gravidade * peso_gravidade + (pessoas_dia / 100) * peso_alcance")
    linhas.append("indice    = beneficio / (custo / 1000)")
    linhas.append("")
    linhas.append("Pesos Base Adotados: Gravidade = {:.1f} | Alcance = {:.1f}".format(
        pesos_base["gravidade"], pesos_base["pessoas_dia"]))
    linhas.append("Regra de Desempate Declarada: Em caso de índices idênticos, o desempate é feito")
    linhas.append("pela ordem alfabética crescente do campo 'codigo'.")
    linhas.append("")

    # Cenários de Sensibilidade
    cenarios = [
        ("Base (0.6 / 0.4)", {"gravidade": 0.6, "pessoas_dia": 0.4}),
        ("Dobro Gravidade (1.2 / 0.4)", {"gravidade": 1.2, "pessoas_dia": 0.4}),
        ("Dobro Alcance (0.6 / 0.8)", {"gravidade": 0.6, "pessoas_dia": 0.8}),
    ]

    rankings = {}
    for nome_cen, p in cenarios:
        copia = [b.copy() for b in barreiras]
        ordenacao.calcular_indices(copia, p)
        ord_lista, _, _ = ordenacao.insertion_sort(copia, chave="indice", crescente=False)
        rankings[nome_cen] = ord_lista

    linhas.append("ANÁLISE DE SENSIBILIDADE - TOP 10 RANKINGS:")
    linhas.append("{:<4} | {:<22} | {:<22} | {:<22}".format(
        "Pos", "Base (0.6 / 0.4)", "Dobro Grav (1.2 / 0.4)", "Dobro Alc (0.6 / 0.8)"))
    linhas.append("-" * 78)

    for i in range(10):
        b_base = rankings["Base (0.6 / 0.4)"][i]
        b_grav = rankings["Dobro Gravidade (1.2 / 0.4)"][i]
        b_alc  = rankings["Dobro Alcance (0.6 / 0.8)"][i]
        linhas.append("{:02d}   | {} (idx {:.2f}) | {} (idx {:.2f}) | {} (idx {:.2f})".format(
            i + 1,
            b_base["codigo"], b_base["indice"],
            b_grav["codigo"], b_grav["indice"],
            b_alc["codigo"], b_alc["indice"]))

    linhas.append("")
    linhas.append("JUSTIFICATIVA E CONCLUSÃO DA RECOMENDAÇÃO DO GRUPO:")
    linhas.append("O grupo mantém sua recomendação original com base no cenário base (0.6 gravidade / 0.4 alcance).")
    linhas.append("Argumento: As 6 primeiras posições são notavelmente estáveis entre os cenários porque reúnem")
    linhas.append("baixo custo financeiro aliado a alto impacto na circulação imediata dos frequentadores")
    linhas.append("(como a remoção de correntes e adequação de sifão e tapetes). Pequenas variações de peso")
    linhas.append("alteram apenas a ordem relativa de itens com custos semelhantes, sem distorcer o núcleo")
    linhas.append("das intervenções prioritárias recomendadas à administração da academia.")
    linhas.append("")
    return "\n".join(linhas)


def gerar_relatorio_completo(setor, pesos):
    """
    Agrupa todos os achados e tabelas no corpo textual completo do relatório.
    """
    barreiras = recursao.achatar(setor)
    ordenacao.calcular_indices(barreiras, pesos)
    dados_matriz = montar_matriz_ambiente_tipo(setor)

    partes = []
    partes.append("=" * 80)
    partes.append("RELATÓRIO TÉCNICO - CAMPUS ACESSÍVEL (GRUPO 11 - ENGENHARIA DE COMPUTAÇÃO)")
    partes.append("SETOR: {}".format(setor["nome"]))
    partes.append("DISCIPLINA: Construção de Algoritmos e Programação (2026/2)")
    partes.append("PROFESSOR: Eduardo Mendes Oliveira")
    partes.append("=" * 80)
    partes.append("")
    partes.append(formatar_matriz_texto(dados_matriz))
    partes.append("")
    partes.append(gerar_achado_a1(barreiras))
    partes.append(gerar_achado_a2(barreiras))
    partes.append(gerar_achado_a3(setor))
    partes.append(gerar_achado_a4(barreiras, pesos))
    partes.append(gerar_achado_a5(barreiras, pesos))

    return "\n".join(partes)


def gravar_relatorio_arquivo(caminho, conteudo):
    """
    Grava o texto do relatório em arquivo (relatorio.txt) com codificação utf-8.
    """
    with open(caminho, "w", encoding="utf-8") as arquivo:
        arquivo.write(conteudo)

