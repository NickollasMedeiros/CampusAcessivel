import os
import sys

import coleta
import ordenacao
import recursao


PESOS = {"gravidade": 0.6, "pessoas_dia": 0.4}
ARQUIVO_FICHA = "ficha_de_campo.txt"
ARQUIVO_INVENTARIO = "inventario.json"


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


def mostrar_ranking(barreiras):
    ordenacao.calcular_indices(barreiras, PESOS)
    ranking, comparacoes, trocas = ordenacao.insertion_sort(barreiras)
    print("\nRANKING DE PRIORIDADE - INSERTION SORT")
    print("Pesos: gravidade=0.6 | alcance (pessoas/dia)=0.4")
    for posicao, barreira in enumerate(ranking, 1):
        print("{:02d}. {} | indice {:.3f} | custo R$ {:.2f}".format(
            posicao, barreira["codigo"], barreira["indice"], barreira["custo"]))
    print("Comparacoes: {} | Trocas: {}".format(comparacoes, trocas))


def executar():
    setor = carregar_setor()
    problemas = coleta.validar_setor(setor)
    if problemas:
        print("\nProblemas de validacao:")
        for problema in problemas:
            print("- " + problema)
    else:
        print("Validacao concluida: {} barreiras validas.".format(
            recursao.contar_barreiras(setor)))

    while True:
        print("\n=== CAMPUS ACESSIVEL - Academia Fusion ===")
        print("1. Ver estrutura do setor")
        print("2. Mostrar ranking de prioridade")
        print("0. Sair")
        opcao = input("Escolha: ").strip()
        if opcao == "1":
            recursao.resumo_hierarquico(setor)
        elif opcao == "2":
            mostrar_ranking(recursao.achatar(setor))
        elif opcao == "0":
            print("Programa encerrado.")
            break
        else:
            print("Opcao invalida. Escolha 1, 2 ou 0.")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--gerar-inventario":
        registros, erros = coleta.importar_ficha_campo(ARQUIVO_FICHA)
        if erros:
            for erro in erros:
                print(erro)
            sys.exit(1)
        coleta.gravar_inventario(ARQUIVO_INVENTARIO, coleta.registros_para_setor(registros))
        print("inventario.json criado com {} barreiras.".format(len(registros)))
    else:
        executar()