"""
Módulo de Testes Dinâmicos da Interface CLI (main.py) e Persistência
Executa simulações interativas automatizadas para as 10 opções do menu,
validando comportamento, mensagens de erro, robustez e integridade do inventario.json.
"""

import json
import os
import shutil
import subprocess
import sys
import unittest

DIR_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARQ_INVENTARIO = os.path.join(DIR_BASE, "inventario.json")
ARQ_BACKUP = os.path.join(DIR_BASE, "inventario_backup_qa.json")
ARQ_RELATORIO = os.path.join(DIR_BASE, "relatorio.txt")


def executar_main_interativo(entradas):
    """
    Executa main.py passando uma lista de comandos/respostas via stdin.
    Garante que o último comando seja '0' para encerramento limpo se não fornecido.
    """
    if not entradas or entradas[-1] != "0":
        entradas.append("0")
    
    texto_input = "\n".join(entradas) + "\n"
    processo = subprocess.run(
        [sys.executable, "main.py"],
        cwd=DIR_BASE,
        input=texto_input,
        text=True,
        capture_output=True,
        encoding="utf-8",
        errors="replace"
    )
    return processo.returncode, processo.stdout, processo.stderr


class TestMenuDinamicoEPersistencia(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Fazer backup do inventario.json original para garantir restauração perfeita
        if os.path.exists(ARQ_INVENTARIO):
            shutil.copyfile(ARQ_INVENTARIO, ARQ_BACKUP)

    @classmethod
    def tearDownClass(cls):
        # Restaurar inventario.json original
        if os.path.exists(ARQ_BACKUP):
            shutil.copyfile(ARQ_BACKUP, ARQ_INVENTARIO)
            os.remove(ARQ_BACKUP)

    def setUp(self):
        # Garantir que cada teste comece com a base íntegra do backup
        if os.path.exists(ARQ_BACKUP):
            shutil.copyfile(ARQ_BACKUP, ARQ_INVENTARIO)

    # =========================================================================
    # OPÇÃO 0: SAIR E ENTRADAS INVÁLIDAS NO MENU PRINCIPAL
    # =========================================================================

    def test_menu_opcao_0_sair_e_entradas_invalidas(self):
        entradas = [
            "99",      # Inválida
            "abc",     # Inválida texto
            "",        # Vazia
            "-1",      # Negativa
            "0"        # Sair
        ]
        ret, out, err = executar_main_interativo(entradas)
        self.assertEqual(ret, 0, f"Processo encerrou com erro: {err}")
        self.assertIn("Opção inválida. Por favor, escolha um número de 0 a 9.", out)
        self.assertIn("Encerrando o sistema Campus Acessível. Até logo!", out)

    # =========================================================================
    # OPÇÃO 3: VER ESTRUTURA DO SETOR (RESUMO HIERÁRQUICO)
    # =========================================================================

    def test_menu_opcao_3_ver_estrutura(self):
        entradas = ["3", "0"]
        ret, out, err = executar_main_interativo(entradas)
        self.assertEqual(ret, 0)
        self.assertIn("--- 3. ESTRUTURA DO SETOR (RESUMO HIERÁRQUICO) ---", out)
        self.assertIn("Academia Fusion - 15 barreiras", out)
        self.assertIn("Total de barreiras: 15", out)
        self.assertIn("Custo total estimado: R$ 76020.00", out)
        self.assertIn("Profundidade real da árvore:", out)

    # =========================================================================
    # OPÇÃO 4: RANKING DE PRIORIDADE (3 ALGORITMOS + ENTRADA ANÔMALA)
    # =========================================================================

    def test_menu_opcao_4_ranking_prioridade_completo(self):
        # 1: Bubble Sort
        ret1, out1, _ = executar_main_interativo(["4", "1", "0"])
        self.assertEqual(ret1, 0)
        self.assertIn("RANKING DE PRIORIDADE - BUBBLE SORT", out1)
        self.assertIn("APROVADO (Idêntico)", out1)
        self.assertIn("MÉTRICAS DO ALGORITMO: Comparações =", out1)

        # 2: Selection Sort
        ret2, out2, _ = executar_main_interativo(["4", "2", "0"])
        self.assertEqual(ret2, 0)
        self.assertIn("RANKING DE PRIORIDADE - SELECTION SORT", out2)
        self.assertIn("APROVADO (Idêntico)", out2)

        # 3: Insertion Sort
        ret3, out3, _ = executar_main_interativo(["4", "3", "0"])
        self.assertEqual(ret3, 0)
        self.assertIn("RANKING DE PRIORIDADE - INSERTION SORT", out3)
        self.assertIn("APROVADO (Idêntico)", out3)

        # Entrada inválida no sub-menu da opção 4
        ret_inv, out_inv, _ = executar_main_interativo(["4", "99", "0"])
        self.assertEqual(ret_inv, 0)
        self.assertIn("Opção inválida.", out_inv)

    # =========================================================================
    # OPÇÃO 5: LOCALIZAR BARREIRA (3 MÉTODOS + CASOS EXTREMOS)
    # =========================================================================

    def test_menu_opcao_5_localizar_barreira(self):
        # 1. Busca Sequencial com código existente
        ret1, out1, _ = executar_main_interativo(["5", "ACA-REC-01", "1", "0"])
        self.assertEqual(ret1, 0)
        self.assertIn("Resultado (Busca Sequencial)", out1)
        self.assertIn("Código: ACA-REC-01", out1)
        self.assertIn("Catraca rotativa sem passagem", out1)

        # 2. Busca Binária Iterativa com código existente
        ret2, out2, _ = executar_main_interativo(["5", "aca-san-14", "2", "0"])  # minúsculo testando strip().upper()
        self.assertEqual(ret2, 0)
        self.assertIn("Resultado (Busca Binária Iterativa)", out2)
        self.assertIn("Código: ACA-SAN-14", out2)

        # 3. Busca Binária Recursiva com código existente
        ret3, out3, _ = executar_main_interativo(["5", "ACA-ESC-06", "3", "0"])
        self.assertEqual(ret3, 0)
        self.assertIn("Resultado (Busca Binária Recursiva)", out3)
        self.assertIn("Código: ACA-ESC-06", out3)

        # 4. Código inexistente
        ret_inex, out_inex, _ = executar_main_interativo(["5", "ACA-FANTASMA-99", "1", "0"])
        self.assertEqual(ret_inex, 0)
        self.assertIn("NÃO foi encontrada na base.", out_inex)

        # 5. Código vazio
        ret_vazio, out_vazio, _ = executar_main_interativo(["5", "", "0"])
        self.assertEqual(ret_vazio, 0)
        self.assertIn("Código não informado.", out_vazio)

        # 6. Opção de algoritmo inválida
        ret_alg_inv, out_alg_inv, _ = executar_main_interativo(["5", "ACA-REC-01", "xyz", "0"])
        self.assertEqual(ret_alg_inv, 0)
        self.assertIn("Opção inválida.", out_alg_inv)

    # =========================================================================
    # OPÇÃO 6: MATRIZ AMBIENTE X TIPO DE BARREIRA
    # =========================================================================

    def test_menu_opcao_6_matriz_ambiente_tipo(self):
        entradas = ["6", "0"]
        ret, out, err = executar_main_interativo(entradas)
        self.assertEqual(ret, 0)
        self.assertIn("--- 6. MATRIZ AMBIENTE X TIPO DE BARREIRA ---", out)
        self.assertIn("=== MATRIZ AMBIENTE X TIPO DE BARREIRA ===", out)
        self.assertIn("TOTAL POR TIPO", out)
        self.assertIn("15", out)

    # =========================================================================
    # OPÇÃO 7: PLANO DE INTERVENÇÃO SOB ORÇAMENTO (GULOSO X EXAUSTIVO)
    # =========================================================================

    def test_menu_opcao_7_plano_orcamento(self):
        # 1. Orçamento padrão R$ 3000 (Enter direto) -> Detecta divergência
        ret1, out1, _ = executar_main_interativo(["7", "", "0"])
        self.assertEqual(ret1, 0)
        self.assertIn("COMPARATIVO DE ESTRATÉGIAS - ORÇAMENTO MÁXIMO R$ 3000.00", out1)
        self.assertIn("DIVERGÊNCIA DETECTADA!", out1)
        self.assertIn("Chamadas Recursivas", out1)

        # 2. Orçamento personalizado R$ 5000
        ret2, out2, _ = executar_main_interativo(["7", "5000,00", "0"])
        self.assertEqual(ret2, 0)
        self.assertIn("COMPARATIVO DE ESTRATÉGIAS - ORÇAMENTO MÁXIMO R$ 5000.00", out2)

        # 3. Entrada anômala (texto no orçamento)
        ret3, out3, _ = executar_main_interativo(["7", "mil_reais", "0"])
        self.assertEqual(ret3, 0)
        self.assertIn("Valor de orçamento inválido.", out3)

    # =========================================================================
    # OPÇÃO 8: RELATÓRIO DE DESEMPENHO (OS 5 ACHADOS)
    # =========================================================================

    def test_menu_opcao_8_relatorio_desempenho(self):
        entradas = ["8", "0"]
        ret, out, err = executar_main_interativo(entradas)
        self.assertEqual(ret, 0)
        self.assertIn("--- 8. RELATÓRIO DE DESEMPENHO DOS ALGORITMOS (OS CINCO ACHADOS) ---", out)
        self.assertIn("[Exibindo Achado A1 - Ordenação]", out)
        self.assertIn("[Exibindo Achado A2 - Busca]", out)
        self.assertIn("[Exibindo Achado A3 - Hierarquia]", out)
        self.assertIn("[Exibindo Achado A4 - Otimização]", out)
        self.assertIn("[Exibindo Achado A5 - Decisão]", out)

    # =========================================================================
    # OPÇÃO 9: GRAVAR RELATÓRIO EM ARQUIVO
    # =========================================================================

    def test_menu_opcao_9_gravar_relatorio(self):
        if os.path.exists(ARQ_RELATORIO):
            os.remove(ARQ_RELATORIO)

        entradas = ["9", "0"]
        ret, out, err = executar_main_interativo(entradas)
        self.assertEqual(ret, 0)
        self.assertIn("Sucesso: Relatório completo gerado e salvo em 'relatorio.txt'", out)
        self.assertTrue(os.path.exists(ARQ_RELATORIO))
        self.assertGreater(os.path.getsize(ARQ_RELATORIO), 5000)

    # =========================================================================
    # OPÇÃO 1: IMPORTAR FICHA DE CAMPO E PERSISTÊNCIA
    # =========================================================================

    def test_menu_opcao_1_importar_ficha(self):
        # 1. Caminho inexistente
        ret_err, out_err, _ = executar_main_interativo(["1", "caminho_inexistente_123.txt", "0"])
        self.assertEqual(ret_err, 0)
        self.assertIn("Erro: Arquivo 'caminho_inexistente_123.txt' não encontrado.", out_err)

        # 2. Importação válida com Enter padrão
        ret_ok, out_ok, _ = executar_main_interativo(["1", "", "0"])
        self.assertEqual(ret_ok, 0)
        self.assertIn("Sucesso: 15 barreiras importadas e salvas em 'inventario.json'.", out_ok)

        # Conferir integridade física do inventario.json
        with open(ARQ_INVENTARIO, "r", encoding="utf-8") as f:
            dados = json.load(f)
        self.assertEqual(dados["nome"], "Academia Fusion")

    # =========================================================================
    # OPÇÃO 2: CADASTRAR, EDITAR, REMOVER E PERSISTÊNCIA EM inventario.json
    # =========================================================================

    def test_menu_opcao_2_crud_e_persistencia_json(self):
        # Sub-teste 2.1: Cadastrar nova barreira
        entradas_cad = [
            "2",  # Menu CRUD
            "1",  # 1. Cadastrar
            "Academia > Área de Treino > Musculação",  # caminho
            "ACA-TRE-99",                             # código
            "Musculação",                             # ambiente
            "circulacao_estreita",                    # tipo
            "Passagem de teste para validacao de QA dinamico", # descrição (>= 15 chars)
            "70,5",                                   # medida
            "cm",                                     # unidade
            "90,0",                                   # referência norma
            "4",                                      # gravidade
            "150",                                    # pessoas/dia
            "750,00",                                 # custo
            "Readequação de espaço",                  # intervenção
            "QA Inspector",                           # coletor
            "2026-11-11",                             # data
            "0",  # Voltar do sub-menu
            "0"   # Sair do main
        ]
        ret_cad, out_cad, _ = executar_main_interativo(entradas_cad)
        self.assertEqual(ret_cad, 0)
        self.assertIn("Sucesso: Barreira cadastrada com sucesso.", out_cad)

        # Verificar persistência imediata em inventario.json
        with open(ARQ_INVENTARIO, "r", encoding="utf-8") as f:
            inv = json.load(f)
        todos_codigos = []
        def coletar(no):
            for b in no.get("barreiras", []):
                todos_codigos.append(b["codigo"])
            for sub in no.get("subsetores", []):
                coletar(sub)
        coletar(inv)
        self.assertIn("ACA-TRE-99", todos_codigos)
        self.assertEqual(len(todos_codigos), 16)

        # Sub-teste 2.2: Editar a barreira recém cadastrada
        entradas_edit = [
            "2",  # Menu CRUD
            "2",  # 2. Editar
            "ACA-TRE-99", # código da barreira
            "Descricao devidamente editada com mais de quinze caracteres", # nova descrição
            "1250.50",    # novo custo
            "5",          # nova gravidade
            "180",        # novo alcance
            "0",  # Voltar do sub-menu
            "0"   # Sair
        ]
        ret_edit, out_edit, _ = executar_main_interativo(entradas_edit)
        self.assertEqual(ret_edit, 0)
        self.assertIn("Sucesso: Barreira atualizada com sucesso.", out_edit)

        # Verificar persistência da alteração em inventario.json
        with open(ARQ_INVENTARIO, "r", encoding="utf-8") as f:
            inv_edit = json.load(f)
        def achar(no, cod):
            for b in no.get("barreiras", []):
                if b["codigo"] == cod:
                    return b
            for sub in no.get("subsetores", []):
                r = achar(sub, cod)
                if r:
                    return r
            return None
        b_editada = achar(inv_edit, "ACA-TRE-99")
        self.assertIsNotNone(b_editada)
        self.assertEqual(b_editada["custo"], 1250.50)
        self.assertEqual(b_editada["gravidade"], 5)
        self.assertEqual(b_editada["pessoas_dia"], 180)

        # Sub-teste 2.3: Remoção com cancelamento ('n')
        entradas_canc = [
            "2",
            "3",          # Remover
            "ACA-TRE-99",
            "n",          # Não confirmar
            "0",
            "0"
        ]
        ret_canc, out_canc, _ = executar_main_interativo(entradas_canc)
        self.assertEqual(ret_canc, 0)
        self.assertIn("Operação cancelada.", out_canc)

        # Confirmar que continua em inventario.json
        with open(ARQ_INVENTARIO, "r", encoding="utf-8") as f:
            inv_pos_canc = json.load(f)
        self.assertIsNotNone(achar(inv_pos_canc, "ACA-TRE-99"))

        # Sub-teste 2.4: Remoção com confirmação ('s')
        entradas_rem = [
            "2",
            "3",          # Remover
            "ACA-TRE-99",
            "s",          # Confirmar
            "0",
            "0"
        ]
        ret_rem, out_rem, _ = executar_main_interativo(entradas_rem)
        self.assertEqual(ret_rem, 0)
        self.assertIn("Sucesso: Barreira removida com sucesso.", out_rem)

        # Verificar remoção persistida em inventario.json
        with open(ARQ_INVENTARIO, "r", encoding="utf-8") as f:
            inv_pos_rem = json.load(f)
        self.assertIsNone(achar(inv_pos_rem, "ACA-TRE-99"))
        todos_codigos_final = []
        def coletar_final(no):
            for b in no.get("barreiras", []):
                todos_codigos_final.append(b["codigo"])
            for sub in no.get("subsetores", []):
                coletar_final(sub)
        coletar_final(inv_pos_rem)
        self.assertEqual(len(todos_codigos_final), 15)


if __name__ == "__main__":
    unittest.main(verbosity=2)
