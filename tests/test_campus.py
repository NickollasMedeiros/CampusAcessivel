import os
import tempfile
import unittest

import coleta
import ordenacao
import recursao


PESOS = {"gravidade": 0.6, "pessoas_dia": 0.4}


def barreira(codigo, gravidade, pessoas_dia, custo, tipo="porta_estreita"):
    return {
        "caminho": "Academia > Teste",
        "codigo": codigo,
        "ambiente": "Teste",
        "tipo": tipo,
        "descricao": "Descricao suficientemente longa para validar",
        "medida": 10.0,
        "unidade": "cm",
        "referencia_norma": 80.0,
        "gravidade": gravidade,
        "pessoas_dia": pessoas_dia,
        "custo": custo,
        "intervencao": "Intervencao de teste",
        "coletado_por": "Grupo",
        "data_coleta": "2026-10-15",
    }


class TestColeta(unittest.TestCase):
    def test_importa_ficha_atual_com_15_registros(self):
        registros, erros = coleta.importar_ficha_campo("ficha_de_campo.txt")
        self.assertEqual(erros, [])
        self.assertEqual(len(registros), 15)
        self.assertTrue(all(registro["custo"] > 0 for registro in registros))

    def test_rejeita_custo_zero_e_gravidade_invalida(self):
        registro = barreira("TEST-01", 6, 100, 0)
        problemas = coleta.validar_registro(registro)
        self.assertIn("gravidade deve estar entre 1 e 5", problemas)
        self.assertIn("custo deve ser maior que zero", problemas)

    def test_detecta_codigo_repetido_no_setor(self):
        primeiro = barreira("TEST-01", 3, 100, 100)
        segundo = barreira("TEST-01", 4, 100, 200)
        setor = {"nome": "Teste", "barreiras": [primeiro], "subsetores": [
            {"nome": "Sub", "barreiras": [segundo], "subsetores": []}
        ]}
        problemas = coleta.validar_setor(setor)
        self.assertTrue(any("codigo repetido" in problema for problema in problemas))

    def test_persistencia_json_preserva_setor(self):
        setor = coleta.registros_para_setor([barreira("TEST-01", 3, 100, 100)])
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as arquivo:
            caminho = arquivo.name
        try:
            coleta.gravar_inventario(caminho, setor)
            carregado = coleta.ler_inventario(caminho)
            self.assertEqual(carregado["nome"], "Academia Fusion")
            self.assertEqual(carregado["subsetores"][0]["barreiras"][0]["codigo"], "TEST-01")
        finally:
            os.remove(caminho)


class TestRecursao(unittest.TestCase):
    def setUp(self):
        self.setor = {
            "nome": "Raiz",
            "barreiras": [barreira("A", 3, 100, 100, "porta_estreita")],
            "subsetores": [{
                "nome": "Filho",
                "barreiras": [barreira("B", 4, 200, 200, "rampa_inclinada")],
                "subsetores": [{
                    "nome": "Neto",
                    "barreiras": [barreira("C", 5, 300, 300, "porta_estreita")],
                    "subsetores": [],
                }],
            }],
        }

    def test_totais_e_profundidade(self):
        self.assertEqual(recursao.contar_barreiras(self.setor), 3)
        self.assertEqual(recursao.custo_total(self.setor), 600.0)
        self.assertEqual(recursao.contar_por_tipo(self.setor, "porta_estreita"), 2)
        self.assertEqual(recursao.profundidade(self.setor), 3)

    def test_achatar_e_caminho(self):
        lista = recursao.achatar(self.setor)
        self.assertEqual([item["codigo"] for item in lista], ["A", "B", "C"])
        self.assertEqual(recursao.caminho_da_barreira(self.setor, "C"), "Raiz > Filho > Neto")
        self.assertIsNone(recursao.caminho_da_barreira(self.setor, "NAO-EXISTE"))

    def test_pacote_exaustivo_encontra_melhor_beneficio(self):
        itens = [
            barreira("A", 5, 100, 60),
            barreira("B", 4, 100, 40),
            barreira("C", 1, 100, 30),
        ]
        beneficio, custo, codigos, chamadas = recursao.melhor_pacote_exaustivo(
            itens, 70, PESOS
        )
        self.assertEqual(codigos, ["B", "C"])
        self.assertEqual(custo, 70.0)
        self.assertEqual(beneficio, 3.8)
        self.assertGreater(chamadas, 0)


class TestOrdenacao(unittest.TestCase):
    def setUp(self):
        self.itens = [
            barreira("C", 3, 100, 100),
            barreira("A", 5, 100, 100),
            barreira("B", 4, 100, 100),
        ]
        ordenacao.calcular_indices(self.itens, PESOS)

    def test_tres_ordenacoes_produzem_mesmo_ranking(self):
        esperados = ["A", "B", "C"]
        for algoritmo in (ordenacao.bubble_sort, ordenacao.selection_sort,
                          ordenacao.insertion_sort):
            ordenada, comparacoes, trocas = algoritmo(self.itens)
            self.assertEqual([item["codigo"] for item in ordenada], esperados)
            self.assertGreater(comparacoes, 0)
            self.assertGreaterEqual(trocas, 0)

    def test_ordenacao_por_codigo_crescente(self):
        ordenada, _, _ = ordenacao.selection_sort(self.itens, chave="codigo", crescente=True)
        self.assertEqual([item["codigo"] for item in ordenada], ["A", "B", "C"])

    def test_ordenacao_nao_altera_lista_original(self):
        original = [item["codigo"] for item in self.itens]
        ordenacao.bubble_sort(self.itens)
        self.assertEqual([item["codigo"] for item in self.itens], original)

    def test_desempate_por_codigo(self):
        ordenada, _, _ = ordenacao.insertion_sort(self.itens)
        self.assertEqual(ordenada[0]["codigo"], "A")
        self.assertTrue(ordenacao.confere_com_o_python(ordenada, "indice", False))


class TestInventarioReal(unittest.TestCase):
    def test_inventario_json_atual(self):
        setor = coleta.ler_inventario("inventario.json")
        problemas = coleta.validar_setor(setor)
        self.assertEqual(problemas, [])
        self.assertEqual(recursao.contar_barreiras(setor), 15)
        self.assertGreater(recursao.profundidade(setor), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)