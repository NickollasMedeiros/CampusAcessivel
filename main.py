"""
Campus Acessível - Academia Fusion
Módulo Principal - Interface de Linha de Comando (Terminal)
UNASP - Engenharia de Computação (2026/2)
"""

import os
import sys

import busca
import coleta
import ordenacao
import recursao
import relatorio


PESOS = {"gravidade": 0.6, "pessoas_dia": 0.4}
ARQUIVO_FICHA = "ficha_de_campo.txt"
ARQUIVO_INVENTARIO = "inventario.json"
ARQUIVO_RELATORIO = "relatorio.txt"


def carregar_setor():
    if os.path.exists(ARQUIVO_INVENTARIO):
        return coleta.ler_inventario(ARQUIVO_INVENTARIO)
    registros, erros = coleta.importar_ficha_campo(ARQUIVO_FICHA)
    if erros:
        print("Erros encontrados na ficha:")
        for erro in erros:
            print("- " + erro)
    setor = coleta.registros_para_setor(registros)
    coleta.gravar_inventario(ARQUIVO_INVENTARIO, setor)
    return setor


def opcao_importar_ficha(setor):
    print("\n--- 1. IMPORTAR FICHA DE CAMPO ---")
    caminho = input("Caminho do arquivo [Enter para '{}']: ".format(ARQUIVO_FICHA)).strip()
    if not caminho:
        caminho = ARQUIVO_FICHA

    if not os.path.exists(caminho):
        print("Erro: Arquivo '{}' não encontrado.".format(caminho))
        return setor

    registros, erros = coleta.importar_ficha_campo(caminho)
    if erros:
        print("\nForam encontrados erros durante a importação:")
        for erro in erros:
            print("- " + erro)
        return setor

    novo_setor = coleta.registros_para_setor(registros)
    problemas = coleta.validar_setor(novo_setor)
    if problemas:
        print("\nProblemas de validação na árvore:")
        for p in problemas:
            print("- " + p)
        return setor

    coleta.gravar_inventario(ARQUIVO_INVENTARIO, novo_setor)
    print("\nSucesso: {} barreiras importadas e salvas em '{}'.".format(
        len(registros), ARQUIVO_INVENTARIO))
    return novo_setor


def opcao_cadastrar_editar_remover(setor):
    while True:
        print("\n--- 2. CADASTRAR / EDITAR / REMOVER BARREIRA ---")
        print("1. Cadastrar nova barreira")
        print("2. Editar barreira existente")
        print("3. Remover barreira")
        print("0. Voltar ao menu principal")
        sub_op = input("Escolha uma opção: ").strip()

        if sub_op == "1":
            print("\n[Cadastro de Nova Barreira]")
            caminho = input("Caminho (ex: Academia > Área de Treino > Musculação): ").strip()
            codigo = input("Código único (ex: ACA-TRE-16): ").strip().upper()
            ambiente = input("Ambiente: ").strip()
            tipo = input("Tipo da barreira: ").strip()
            descricao = input("Descrição detalhada: ").strip()
            try:
                medida = float(input("Medida observada (numérico): ").strip().replace(",", "."))
                unidade = input("Unidade (cm ou m): ").strip()
                referencia_norma = float(input("Referência da norma: ").strip().replace(",", "."))
                gravidade = int(input("Gravidade (1 a 5): ").strip())
                pessoas_dia = int(input("Alcance de pessoas/dia: ").strip())
                custo = float(input("Custo estimado (R$): ").strip().replace(",", "."))
            except ValueError:
                print("Erro: Um dos campos numéricos recebeu valor inválido.")
                continue

            intervencao = input("Intervenção recomendada: ").strip()
            coletado_por = input("Nome do coletor: ").strip()
            data_coleta = input("Data da coleta (AAAA-MM-DD): ").strip()

            nova = {
                "caminho": caminho,
                "codigo": codigo,
                "ambiente": ambiente,
                "tipo": tipo,
                "descricao": descricao,
                "medida": medida,
                "unidade": unidade,
                "referencia_norma": referencia_norma,
                "gravidade": gravidade,
                "pessoas_dia": pessoas_dia,
                "custo": custo,
                "intervencao": intervencao,
                "coletado_por": coletado_por,
                "data_coleta": data_coleta
            }

            sucesso, msg = coleta.cadastrar_barreira(setor, nova)
            if sucesso:
                coleta.gravar_inventario(ARQUIVO_INVENTARIO, setor)
                print("Sucesso: " + msg)
            else:
                print("Falha ao cadastrar:")
                for p in msg:
                    print("- " + p)

        elif sub_op == "2":
            print("\n[Edição de Barreira]")
            codigo = input("Informe o código da barreira a editar: ").strip().upper()
            barreira = coleta.localizar_barreira(setor, codigo)
            if barreira is None:
                print("Erro: Barreira com código '{}' não encontrada.".format(codigo))
                continue

            print("Barreira encontrada: [{}] {}".format(barreira["codigo"], barreira["descricao"]))
            print("Pressione Enter para manter o valor atual.")

            novos_dados = {}
            novo_desc = input("Nova descrição [{}]: ".format(barreira["descricao"])).strip()
            if novo_desc:
                novos_dados["descricao"] = novo_desc

            novo_custo_str = input("Novo custo (R$) [{:.2f}]: ".format(barreira["custo"])).strip()
            if novo_custo_str:
                try:
                    novos_dados["custo"] = float(novo_custo_str.replace(",", "."))
                except ValueError:
                    print("Custo inválido.")

            nova_grav_str = input("Nova gravidade (1-5) [{}]: ".format(barreira["gravidade"])).strip()
            if nova_grav_str:
                try:
                    novos_dados["gravidade"] = int(nova_grav_str)
                except ValueError:
                    print("Gravidade inválida.")

            novo_alcance_str = input("Novo alcance (pessoas/dia) [{}]: ".format(barreira["pessoas_dia"])).strip()
            if novo_alcance_str:
                try:
                    novos_dados["pessoas_dia"] = int(novo_alcance_str)
                except ValueError:
                    print("Alcance inválido.")

            if not novos_dados:
                print("Nenhuma alteração informada.")
                continue

            sucesso, msg = coleta.editar_barreira(setor, codigo, novos_dados)
            if sucesso:
                coleta.gravar_inventario(ARQUIVO_INVENTARIO, setor)
                print("Sucesso: " + msg)
            else:
                print("Falha ao editar:")
                for p in msg:
                    print("- " + p)

        elif sub_op == "3":
            print("\n[Remoção de Barreira]")
            codigo = input("Informe o código da barreira a remover: ").strip().upper()
            confirmacao = input("Tem certeza que deseja remover '{}'? (s/n): ".format(codigo)).strip().lower()
            if confirmacao == "s":
                sucesso, msg = coleta.remover_barreira(setor, codigo)
                if sucesso:
                    coleta.gravar_inventario(ARQUIVO_INVENTARIO, setor)
                    print("Sucesso: " + msg)
                else:
                    print("Erro: " + msg)
            else:
                print("Operação cancelada.")

        elif sub_op == "0":
            break
        else:
            print("Opção inválida.")


def opcao_ver_estrutura(setor):
    print("\n--- 3. ESTRUTURA DO SETOR (RESUMO HIERÁRQUICO) ---")
    recursao.resumo_hierarquico(setor)
    print("\nMÉTRICAS GERAIS:")
    print("Total de barreiras: {}".format(recursao.contar_barreiras(setor)))
    print("Custo total estimado: R$ {:.2f}".format(recursao.custo_total(setor)))
    print("Profundidade real da árvore: {} níveis".format(recursao.profundidade(setor)))


def opcao_ranking_prioridade(setor):
    print("\n--- 4. RANKING DE PRIORIDADE ---")
    print("Escolha o algoritmo de ordenação:")
    print("1. Bubble Sort")
    print("2. Selection Sort")
    print("3. Insertion Sort")
    escolha = input("Opção [1, 2 ou 3]: ").strip()

    algoritmo_nome = ""
    algoritmo_fn = None
    if escolha == "1":
        algoritmo_nome = "BUBBLE SORT"
        algoritmo_fn = ordenacao.bubble_sort
    elif escolha == "2":
        algoritmo_nome = "SELECTION SORT"
        algoritmo_fn = ordenacao.selection_sort
    elif escolha == "3":
        algoritmo_nome = "INSERTION SORT"
        algoritmo_fn = ordenacao.insertion_sort
    else:
        print("Opção inválida.")
        return

    barreiras = recursao.achatar(setor)
    ordenacao.calcular_indices(barreiras, PESOS)

    ranking, comparacoes, trocas = algoritmo_fn(barreiras, chave="indice", crescente=False)
    conferido = ordenacao.confere_com_o_python(ranking, "indice", False)

    print("\n" + "=" * 90)
    print("RANKING DE PRIORIDADE - {}".format(algoritmo_nome))
    print("Pesos Adotados: Gravidade = {:.1f} | Alcance = {:.1f}".format(
        PESOS["gravidade"], PESOS["pessoas_dia"]))
    print("Conferência com sorted() do Python: {}".format("APROVADO (Idêntico)" if conferido else "DIVERGENTE"))
    print("=" * 90)
    print("{:<4} | {:<12} | {:<8} | {:<12} | {:<4} | {:<6} | {:<15} | {:<20}".format(
        "Pos", "Código", "Índice", "Custo (R$)", "Grav", "Pessoas", "Ambiente", "Descrição"))
    print("-" * 90)

    for pos, b in enumerate(ranking, 1):
        desc = b["descricao"]
        if len(desc) > 20:
            desc = desc[:17] + "..."
        print("{:02d}   | {:<12} | {:>8.3f} | R$ {:>9.2f} | {:>4} | {:>7} | {:<15} | {:<20}".format(
            pos, b["codigo"], b["indice"], b["custo"], b["gravidade"], b["pessoas_dia"], b["ambiente"], desc))

    print("-" * 90)
    print("MÉTRICAS DO ALGORITMO: Comparações = {} | Trocas = {}".format(comparacoes, trocas))


def opcao_localizar_barreira(setor):
    print("\n--- 5. LOCALIZAR BARREIRA POR CÓDIGO ---")
    codigo = input("Informe o código da barreira (ex: ACA-REC-01): ").strip().upper()
    if not codigo:
        print("Código não informado.")
        return

    print("Escolha o método de busca:")
    print("1. Busca Sequencial")
    print("2. Busca Binária Iterativa")
    print("3. Busca Binária Recursiva")
    escolha = input("Opção [1, 2 ou 3]: ").strip()

    barreiras = recursao.achatar(setor)

    if escolha == "1":
        posicao, comparacoes = busca.busca_sequencial(barreiras, codigo)
        metodo = "Busca Sequencial"
        lista_usada = barreiras
    elif escolha in ("2", "3"):
        ordenadas, _, _ = ordenacao.selection_sort(barreiras, chave="codigo", crescente=True)
        lista_usada = ordenadas
        if escolha == "2":
            posicao, comparacoes = busca.busca_binaria_iterativa(ordenadas, codigo)
            metodo = "Busca Binária Iterativa"
        else:
            posicao, comparacoes = busca.busca_binaria_recursiva(ordenadas, codigo)
            metodo = "Busca Binária Recursiva"
    else:
        print("Opção inválida.")
        return

    print("\nResultado ({}) - Comparações realizadas: {}".format(metodo, comparacoes))
    if posicao != -1:
        barreira = lista_usada[posicao]
        caminho_hierarquico = recursao.caminho_da_barreira(setor, codigo)
        print("Posição na lista: {}".format(posicao))
        print("Código: {}".format(barreira["codigo"]))
        print("Ambiente: {}".format(barreira["ambiente"]))
        print("Tipo: {}".format(barreira["tipo"]))
        print("Descrição: {}".format(barreira["descricao"]))
        print("Medida / Norma: {} {} (Referência: {} {})".format(
            barreira["medida"], barreira["unidade"], barreira["referencia_norma"], barreira["unidade"]))
        print("Gravidade: {}/5 | Pessoas afetadas/dia: {}".format(
            barreira["gravidade"], barreira["pessoas_dia"]))
        print("Custo estimado: R$ {:.2f}".format(barreira["custo"]))
        print("Intervenção recomendada: {}".format(barreira["intervencao"]))
        print("Caminho na árvore: {}".format(caminho_hierarquico))
    else:
        print("Aviso: Barreira com código '{}' NÃO foi encontrada na base.".format(codigo))


def opcao_matriz_ambiente_tipo(setor):
    print("\n--- 6. MATRIZ AMBIENTE X TIPO DE BARREIRA ---")
    dados = relatorio.montar_matriz_ambiente_tipo(setor)
    texto = relatorio.formatar_matriz_texto(dados)
    print(texto)


def opcao_plano_orcamento(setor):
    print("\n--- 7. PLANO DE INTERVENÇÃO SOB ORÇAMENTO (GULOSO X EXAUSTIVO) ---")
    barreiras = recursao.achatar(setor)
    ordenacao.calcular_indices(barreiras, PESOS)

    valor_padrao = 3000.0
    entrada = input("Informe o teto de orçamento em R$ [Enter para R$ {:.2f}]: ".format(valor_padrao)).strip()
    if not entrada:
        orcamento = valor_padrao
    else:
        try:
            orcamento = float(entrada.replace(",", "."))
        except ValueError:
            print("Valor de orçamento inválido.")
            return

    # Poda prévia de itens que individualmente estouram o teto
    candidatas = recursao.podar_inviaveis(barreiras, orcamento)
    print("\nBarreiras totais: {} | Barreiras viáveis após poda (custo <= R$ {:.2f}): {}".format(
        len(barreiras), orcamento, len(candidatas)))

    if len(candidatas) > 20:
        print("AVISO: O número de candidatas ({}) excede 20 elementos.".format(len(candidatas)))
        print("A abordagem exaustiva poderá demandar mais de 2^20 (1 milhão) de chamadas recursivas.")

    # Execução das estratégias
    bg, cg, itens_g = recursao.pacote_guloso(candidatas, orcamento, PESOS)
    be, ce, itens_e, chamadas = recursao.melhor_pacote_exaustivo(candidatas, orcamento, PESOS)

    print("\n" + "=" * 80)
    print("COMPARATIVO DE ESTRATÉGIAS - ORÇAMENTO MÁXIMO R$ {:.2f}".format(orcamento))
    print("=" * 80)
    print("{:<25} | {:<22} | {:<22}".format("Métrica", "Estratégia Gulosa", "Estratégia Exaustiva"))
    print("-" * 80)
    print("{:<25} | {:<22.3f} | {:<22.3f}".format("Benefício Total", bg, be))
    print("{:<25} | R$ {:<19.2f} | R$ {:<19.2f}".format("Custo Total Executado", cg, ce))
    print("{:<25} | R$ {:<19.2f} | R$ {:<19.2f}".format("Orçamento Restante", orcamento - cg, orcamento - ce))
    print("{:<25} | {:<22} | {:<22}".format("Qtd Barreiras Atendidas", len(itens_g), len(itens_e)))
    print("{:<25} | {:<22} | {:<22}".format("Chamadas Recursivas", "N/A (Linear)", chamadas))
    print("-" * 80)

    print("\nBarreiras escolhidas pela Estratégia Gulosa:")
    print(", ".join(itens_g))

    print("\nBarreiras escolhidas pela Estratégia Exaustiva:")
    print(", ".join(itens_e))

    if abs(be - bg) > 0.001:
        print("\n>>> DIVERGÊNCIA DETECTADA!")
        print("O pacote Exaustivo obteve benefício superior (+{:.3f}) em relação ao Guloso.".format(be - bg))
        print("Explicação: A gulosa esgota o orçamento seguindo estritamente a taxa de prioridade,")
        print("deixando uma folga orçamentária que não acomoda a próxima barreira individualmente.")
        print("A busca exaustiva combina os itens aproveitando melhor o espaço orçamentário restante.")
    else:
        print("\nNeste orçamento específico, ambas as estratégias convergiram para o mesmo benefício ótimo.")


def opcao_relatorio_desempenho(setor):
    print("\n--- 8. RELATÓRIO DE DESEMPENHO DOS ALGORITMOS (OS CINCO ACHADOS) ---")
    barreiras = recursao.achatar(setor)
    ordenacao.calcular_indices(barreiras, PESOS)

    print("\n[Exibindo Achado A1 - Ordenação]")
    print(relatorio.gerar_achado_a1(barreiras))

    print("\n[Exibindo Achado A2 - Busca]")
    print(relatorio.gerar_achado_a2(barreiras))

    print("\n[Exibindo Achado A3 - Hierarquia]")
    print(relatorio.gerar_achado_a3(setor))

    print("\n[Exibindo Achado A4 - Otimização]")
    print(relatorio.gerar_achado_a4(barreiras, PESOS))

    print("\n[Exibindo Achado A5 - Decisão]")
    print(relatorio.gerar_achado_a5(barreiras, PESOS))


def opcao_gravar_relatorio(setor):
    print("\n--- 9. GRAVAR RELATÓRIO EM ARQUIVO ---")
    conteudo = relatorio.gerar_relatorio_completo(setor, PESOS)
    relatorio.gravar_relatorio_arquivo(ARQUIVO_RELATORIO, conteudo)
    tamanho = os.path.getsize(ARQUIVO_RELATORIO)
    print("Sucesso: Relatório completo gerado e salvo em '{}' ({} bytes).".format(
        ARQUIVO_RELATORIO, tamanho))


def executar():
    setor = carregar_setor()
    problemas = coleta.validar_setor(setor)
    if problemas:
        print("\nProblemas de validação no inventário:")
        for problema in problemas:
            print("- " + problema)
    else:
        print("Validação inicial concluída: {} barreiras válidas no setor '{}'.".format(
            recursao.contar_barreiras(setor), setor["nome"]))

    while True:
        print("\n" + "=" * 55)
        print("=== CAMPUS ACESSIVEL - setor: {} ===".format(setor["nome"]))
        print("=" * 55)
        print("1. Importar ficha de campo")
        print("2. Cadastrar / editar / remover barreira")
        print("3. Ver estrutura do setor (resumo hierarquico)")
        print("4. Ranking de prioridade (bubble / selection / insertion)")
        print("5. Localizar barreira por codigo (sequencial / binaria iterativa / binaria recursiva)")
        print("6. Matriz ambiente x tipo de barreira")
        print("7. Plano de intervencao sob orcamento (guloso x exaustivo)")
        print("8. Relatorio de desempenho dos algoritmos")
        print("9. Gravar relatorio em arquivo")
        print("0. Sair")
        print("=" * 55)

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            setor = opcao_importar_ficha(setor)
        elif opcao == "2":
            opcao_cadastrar_editar_remover(setor)
        elif opcao == "3":
            opcao_ver_estrutura(setor)
        elif opcao == "4":
            opcao_ranking_prioridade(setor)
        elif opcao == "5":
            opcao_localizar_barreira(setor)
        elif opcao == "6":
            opcao_matriz_ambiente_tipo(setor)
        elif opcao == "7":
            opcao_plano_orcamento(setor)
        elif opcao == "8":
            opcao_relatorio_desempenho(setor)
        elif opcao == "9":
            opcao_gravar_relatorio(setor)
        elif opcao == "0":
            print("Encerrando o sistema Campus Acessível. Até logo!")
            break
        else:
            print("Opção inválida. Por favor, escolha um número de 0 a 9.")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--gerar-inventario":
        registros, erros = coleta.importar_ficha_campo(ARQUIVO_FICHA)
        if erros:
            for erro in erros:
                print(erro)
            sys.exit(1)
        coleta.gravar_inventario(ARQUIVO_INVENTARIO, coleta.registros_para_setor(registros))
        print("inventario.json criado com {} barreiras.".format(len(registros)))
    elif len(sys.argv) > 1 and sys.argv[1] == "--gerar-relatorio":
        s = carregar_setor()
        opcao_gravar_relatorio(s)
    else:
        executar()
