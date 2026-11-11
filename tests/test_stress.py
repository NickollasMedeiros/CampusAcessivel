import unittest
import coleta
import ordenacao
import busca
import recursao
import relatorio


class TestStressCampusAcessivel(unittest.TestCase):
    def setUp(self):
        self.pesos = {"gravidade": 0.6, "pessoas_dia": 0.4}
        self.barreira_valida = {
            "caminho": "Academia Fusion > Musculacao",
            "codigo": "TEST-01",
            "ambiente": "Musculacao",
            "tipo": "porta_estreita",
            "descricao": "Descricao suficientemente longa para o teste de campo",
            "medida": 75.0,
            "unidade": "cm",
            "referencia_norma": 80.0,
            "gravidade": 4,
            "pessoas_dia": 100,
            "custo": 500.0,
            "intervencao": "Alargar marco da porta",
            "coletado_por": "Tester",
            "data_coleta": "2026-11-11"
        }

    def test_validacao_campos_invalidos_e_limites(self):
        b = self.barreira_valida.copy()
        b["gravidade"] = 0
        probs = coleta.validar_registro(b)
        self.assertTrue(any("gravidade" in p for p in probs))

        b["gravidade"] = 6
        probs = coleta.validar_registro(b)
        self.assertTrue(any("gravidade" in p for p in probs))

        b["gravidade"] = "quatro"
        probs = coleta.validar_registro(b)
        self.assertTrue(any("gravidade" in p for p in probs))

        b = self.barreira_valida.copy()
        b["custo"] = -10.0
        probs = coleta.validar_registro(b)
        self.assertTrue(any("custo" in p for p in probs))

        b["custo"] = 0.0
        probs = coleta.validar_registro(b)
        self.assertTrue(any("custo" in p for p in probs))

        b = self.barreira_valida.copy()
        b["medida"] = -0.5
        probs = coleta.validar_registro(b)
        self.assertTrue(any("medida" in p for p in probs))

        b = self.barreira_valida.copy()
        b["descricao"] = "curta"
        probs = coleta.validar_registro(b)
        self.assertTrue(any("descricao" in p for p in probs))

    def test_desempate_estavel_e_paridade_trocas(self):
        itens = [
            {"codigo": "B", "indice": 10.0, "gravidade": 3, "pessoas_dia": 50, "custo": 300},
            {"codigo": "A", "indice": 10.0, "gravidade": 3, "pessoas_dia": 50, "custo": 300},
            {"codigo": "C", "indice": 10.0, "gravidade": 3, "pessoas_dia": 50, "custo": 300},
        ]
        b_ord, _, b_t = ordenacao.bubble_sort(itens, chave="indice", crescente=False)
        s_ord, s_c, _ = ordenacao.selection_sort(itens, chave="indice", crescente=False)
        i_ord, _, i_t = ordenacao.insertion_sort(itens, chave="indice", crescente=False)

        # Regra de desempate alfabético por código: A, B, C
        self.assertEqual([x["codigo"] for x in b_ord], ["A", "B", "C"])
        self.assertEqual([x["codigo"] for x in s_ord], ["A", "B", "C"])
        self.assertEqual([x["codigo"] for x in i_ord], ["A", "B", "C"])

        # Selection sort sempre n(n-1)/2 comparações: 3*2/2 = 3
        self.assertEqual(s_c, 3)

        # Bubble e Insertion trocas rigorosamente idênticas
        self.assertEqual(b_t, i_t)

    def test_busca_casos_extremos(self):
        lista = []
        p_seq, c_seq = busca.busca_sequencial(lista, "INEXISTENTE")
        self.assertEqual(p_seq, -1)
        self.assertEqual(c_seq, 0)

        p_it, c_it = busca.busca_binaria_iterativa(lista, "INEXISTENTE")
        self.assertEqual(p_it, -1)
        self.assertEqual(c_it, 0)

        p_rec, c_rec = busca.busca_binaria_recursiva(lista, "INEXISTENTE")
        self.assertEqual(p_rec, -1)
        self.assertEqual(c_rec, 0)

        um_item = [{"codigo": "ACA-01"}]
        p, c = busca.busca_binaria_recursiva(um_item, "ACA-01")
        self.assertEqual(p, 0)
        self.assertEqual(c, 1)

        p, c = busca.busca_binaria_recursiva(um_item, "ACA-02")
        self.assertEqual(p, -1)

    def test_mochila_limites_orcamento(self):
        barreiras = [
            {"codigo": "B1", "custo": 100.0, "gravidade": 3, "pessoas_dia": 50},
            {"codigo": "B2", "custo": 200.0, "gravidade": 4, "pessoas_dia": 80},
        ]
        # Orçamento zero
        podadas = recursao.podar_inviaveis(barreiras, 0.0)
        self.assertEqual(len(podadas), 0)
        bg, cg, itens_g = recursao.pacote_guloso(podadas, 0.0, self.pesos)
        be, ce, itens_e, ch = recursao.melhor_pacote_exaustivo(podadas, 0.0, self.pesos)
        self.assertEqual(bg, 0.0)
        self.assertEqual(be, 0.0)
        self.assertEqual(len(itens_g), 0)
        self.assertEqual(len(itens_e), 0)


if __name__ == "__main__":
    unittest.main()
