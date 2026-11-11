"""
Módulo de Testes de Estresse e Validação CRUD - Campus Acessível
Focado em entradas anômalas, casos limites e robustez do módulo coleta.py
"""

import json
import os
import tempfile
import unittest

import coleta
import recursao


def barreira_base(codigo="STRESS-01", **kwargs):
    padrao = {
        "caminho": "Academia Fusion > Setor Alfa > Sala 1",
        "codigo": codigo,
        "ambiente": "Sala 1",
        "tipo": "porta_estreita",
        "descricao": "Largura da folha de porta inferior a 80 centimetros",
        "medida": 68.5,
        "unidade": "cm",
        "referencia_norma": 80.0,
        "gravidade": 4,
        "pessoas_dia": 120,
        "custo": 850.0,
        "intervencao": "Substituição do caixilho e folha",
        "coletado_por": "QA Bot",
        "data_coleta": "2026-11-11"
    }
    padrao.update(kwargs)
    return padrao


class TestStressColeta(unittest.TestCase):

    # =========================================================================
    # 1. VALIDAÇÃO DE REGISTROS (validar_registro) COM ENTRADAS ANÔMALAS
    # =========================================================================

    def test_registro_vazio_ou_campos_ausentes(self):
        problemas = coleta.validar_registro({})
        self.assertGreaterEqual(len(problemas), 14)
        for campo in coleta.CAMPOS:
            self.assertTrue(any(campo in p for p in problemas), f"Deveria reportar ausência de '{campo}'")

    def test_registro_campos_espacos_em_branco(self):
        registro = {campo: "   " for campo in coleta.CAMPOS}
        problemas = coleta.validar_registro(registro)
        self.assertGreaterEqual(len(problemas), 14)
        for campo in coleta.CAMPOS:
            self.assertTrue(any(f"campo ausente: {campo}" in p for p in problemas))

    def test_gravidade_limites_e_tipos_anomalos(self):
        # Limites válidos (1 e 5)
        self.assertEqual(coleta.validar_registro(barreira_base(gravidade=1)), [])
        self.assertEqual(coleta.validar_registro(barreira_base(gravidade=5)), [])

        # Inválidos: fora do intervalo
        for g_inv in [0, -1, -99, 6, 10, 1000]:
            p = coleta.validar_registro(barreira_base(gravidade=g_inv))
            self.assertTrue(any("gravidade deve estar entre 1 e 5" in msg for msg in p), f"Falha para gravidade={g_inv}")

        # Inválidos: tipos não numéricos
        for g_str in ["cinco", "alta", None, [3], {"g": 4}]:
            p = coleta.validar_registro(barreira_base(gravidade=g_str))
            self.assertTrue(any("gravidade" in msg for msg in p), f"Falha para tipo anômalo {g_str}")

    def test_custo_limites_e_tipos_anomalos(self):
        # Custo válido
        self.assertEqual(coleta.validar_registro(barreira_base(custo=0.01)), [])
        self.assertEqual(coleta.validar_registro(barreira_base(custo=1000000.0)), [])

        # Custo <= 0
        for c_inv in [0, 0.0, -0.01, -500.0, -1e6]:
            p = coleta.validar_registro(barreira_base(custo=c_inv))
            self.assertTrue(any("custo deve ser maior que zero" in msg for msg in p), f"Falha para custo={c_inv}")

        # Custo não numérico
        for c_str in ["de_graca", "cem reais", None, []]:
            p = coleta.validar_registro(barreira_base(custo=c_str))
            self.assertTrue(any("custo invalido" in msg or "custo deve ser maior que zero" in msg for msg in p))

    def test_medida_limites_e_tipos_anomalos(self):
        # Medida zero é válida (ex: ausência de rampa/elevador/sinalização)
        self.assertEqual(coleta.validar_registro(barreira_base(medida=0)), [])
        self.assertEqual(coleta.validar_registro(barreira_base(medida=0.0)), [])
        self.assertEqual(coleta.validar_registro(barreira_base(medida=999.9)), [])

        # Medida negativa é inválida
        for m_inv in [-0.01, -1.0, -50.0]:
            p = coleta.validar_registro(barreira_base(medida=m_inv))
            self.assertTrue(any("medida nao pode ser negativa" in msg for msg in p))

        # Medida com tipo inválido
        for m_str in ["quinhentos", None, {}]:
            p = coleta.validar_registro(barreira_base(medida=m_str))
            self.assertTrue(any("medida invalida" in msg for msg in p))

    def test_descricao_comprimento_fronteira(self):
        # 14 caracteres (deve falhar)
        desc_14 = "12345678901234"
        self.assertEqual(len(desc_14), 14)
        p14 = coleta.validar_registro(barreira_base(descricao=desc_14))
        self.assertTrue(any("descricao curta demais" in msg for msg in p14))

        # 15 caracteres (limite exato - deve passar)
        desc_15 = "123456789012345"
        self.assertEqual(len(desc_15), 15)
        p15 = coleta.validar_registro(barreira_base(descricao=desc_15))
        self.assertFalse(any("descricao curta demais" in msg for msg in p15))

        # 5.000 caracteres (estresse de tamanho)
        desc_longa = "Descricao de teste extensa. " * 200
        p_longa = coleta.validar_registro(barreira_base(descricao=desc_longa))
        self.assertEqual(p_longa, [])

    def test_caracteres_especiais_e_injecoes(self):
        # Injeção e caracteres especiais devem ser tratados como texto seguro sem quebrar
        payloads = [
            "<script>alert('XSS')</script>",
            "' OR '1'='1'; DROP TABLE barreiras; --",
            "Barreira com acentuação: Ação, Acesso & Corrimão (90°)",
            "Emoji no texto: ⚠️ Cuidado piso molhado ♿",
            "Tabs \t e quebras \n no texto",
        ]
        for payload in payloads:
            b = barreira_base(descricao=payload.ljust(20, "x"))
            probs = coleta.validar_registro(b)
            # Não deve dar crash; validação deve aceitar string de tamanho suficiente
            self.assertEqual(probs, [], f"Falhou com payload: {payload}")

    def test_codigo_repetido_na_validacao(self):
        codigos_usados = ["COD-01", "COD-02", "COD-03"]
        b_dup = barreira_base(codigo="COD-02")
        probs = coleta.validar_registro(b_dup, codigos_usados)
        self.assertIn("codigo repetido: COD-02", probs)

        b_novo = barreira_base(codigo="COD-04")
        probs_novo = coleta.validar_registro(b_novo, codigos_usados)
        self.assertNotIn("codigo repetido: COD-04", probs_novo)

    # =========================================================================
    # 2. VALIDAÇÃO DE ÁRVORE / SETOR (validar_setor)
    # =========================================================================

    def test_validar_setor_arvore_profunda(self):
        # Cria árvore com 10 níveis de profundidade
        raiz = {"nome": "Nivel 0", "barreiras": [], "subsetores": []}
        atual = raiz
        for i in range(1, 11):
            filho = {"nome": f"Nivel {i}", "barreiras": [barreira_base(codigo=f"PROF-{i}")], "subsetores": []}
            atual["subsetores"].append(filho)
            atual = filho

        probs = coleta.validar_setor(raiz)
        self.assertEqual(probs, [])
        self.assertEqual(recursao.profundidade(raiz), 11)
        self.assertEqual(recursao.contar_barreiras(raiz), 10)

    def test_validar_setor_detecta_duplicata_em_ramos_diferentes(self):
        raiz = {
            "nome": "Campus",
            "barreiras": [],
            "subsetores": [
                {
                    "nome": "Bloco A",
                    "barreiras": [barreira_base(codigo="CLONE-01")],
                    "subsetores": []
                },
                {
                    "nome": "Bloco B",
                    "barreiras": [barreira_base(codigo="CLONE-01")],
                    "subsetores": []
                }
            ]
        }
        probs = coleta.validar_setor(raiz)
        self.assertTrue(any("codigo repetido: CLONE-01" in p for p in probs))

    # =========================================================================
    # 3. CRUD COMPLETO E CASOS DE FRONTEIRA
    # =========================================================================

    def test_crud_fluxo_completo_e_rejeicoes(self):
        setor = {"nome": "Setor Raiz", "barreiras": [], "subsetores": []}

        # 1. Cadastrar barreira válida com auto-criação de subníveis
        b1 = barreira_base(codigo="CAD-01", caminho="Setor Raiz > Ala Norte > Sala 10")
        sucesso, msg = coleta.cadastrar_barreira(setor, b1)
        self.assertTrue(sucesso)
        self.assertEqual(coleta.localizar_barreira(setor, "CAD-01")["codigo"], "CAD-01")

        # 2. Rejeitar cadastro com código repetido
        b1_dup = barreira_base(codigo="CAD-01", caminho="Setor Raiz > Ala Sul")
        sucesso_dup, msg_dup = coleta.cadastrar_barreira(setor, b1_dup)
        self.assertFalse(sucesso_dup)
        self.assertTrue(any("codigo repetido" in p for p in msg_dup))

        # 3. Rejeitar cadastro com dados inválidos
        b_inv = barreira_base(codigo="CAD-INV", gravidade=9, custo=-10)
        sucesso_inv, msg_inv = coleta.cadastrar_barreira(setor, b_inv)
        self.assertFalse(sucesso_inv)
        self.assertTrue(len(msg_inv) >= 2)

        # 4. Cadastrar uma segunda barreira
        b2 = barreira_base(codigo="CAD-02", caminho="Setor Raiz > Ala Norte > Sala 20", custo=350.0)
        sucesso_b2, _ = coleta.cadastrar_barreira(setor, b2)
        self.assertTrue(sucesso_b2)
        self.assertEqual(recursao.contar_barreiras(setor), 2)

        # 5. Edição bem sucedida de múltiplos campos
        sucesso_ed, msg_ed = coleta.editar_barreira(
            setor, "CAD-01", {"custo": 999.0, "descricao": "Nova descricao detalhada devidamente validada"}
        )
        self.assertTrue(sucesso_ed)
        self.assertEqual(coleta.localizar_barreira(setor, "CAD-01")["custo"], 999.0)

        # 6. Edição rejeitada: código inexistente
        sucesso_ed_inex, msg_ed_inex = coleta.editar_barreira(setor, "NAO-EXISTE", {"custo": 100.0})
        self.assertFalse(sucesso_ed_inex)
        self.assertTrue(any("não encontrada" in m for m in msg_ed_inex))

        # 7. Edição rejeitada: dados inválidos (não deve corromper o registro original)
        sucesso_ed_inv, msg_ed_inv = coleta.editar_barreira(setor, "CAD-01", {"custo": -50.0})
        self.assertFalse(sucesso_ed_inv)
        self.assertEqual(coleta.localizar_barreira(setor, "CAD-01")["custo"], 999.0)

        # 8. Edição rejeitada: alteração de código colidindo com outro código existente
        sucesso_ed_col, msg_ed_col = coleta.editar_barreira(setor, "CAD-01", {"codigo": "CAD-02"})
        self.assertFalse(sucesso_ed_col)
        self.assertTrue(any("codigo repetido: CAD-02" in m for m in msg_ed_col))

        # 9. Remoção de código inexistente
        sucesso_rem_inex, msg_rem_inex = coleta.remover_barreira(setor, "INEXISTENTE-99")
        self.assertFalse(sucesso_rem_inex)

        # 10. Remoção bem sucedida de CAD-01
        sucesso_rem_1, _ = coleta.remover_barreira(setor, "CAD-01")
        self.assertTrue(sucesso_rem_1)
        self.assertIsNone(coleta.localizar_barreira(setor, "CAD-01"))
        self.assertEqual(recursao.contar_barreiras(setor), 1)

        # 11. Remoção bem sucedida de CAD-02
        sucesso_rem_2, _ = coleta.remover_barreira(setor, "CAD-02")
        self.assertTrue(sucesso_rem_2)
        self.assertEqual(recursao.contar_barreiras(setor), 0)

    # =========================================================================
    # 4. IMPORTAÇÃO E PERSISTÊNCIA (importar_ficha_campo, gravar/ler_inventario)
    # =========================================================================

    def test_importar_ficha_arquivo_inexistente(self):
        with self.assertRaises(FileNotFoundError):
            coleta.importar_ficha_campo("arquivo_fantasma_xyz.txt")

    def test_importar_ficha_arquivo_vazio(self):
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False) as f:
            f.write("")
            caminho = f.name
        try:
            registros, erros = coleta.importar_ficha_campo(caminho)
            self.assertEqual(registros, [])
            self.assertEqual(erros, [])
        finally:
            os.remove(caminho)

    def test_importar_ficha_linhas_anomalas(self):
        linhas = [
            "caminho;codigo;ambiente;tipo;descricao;medida;unidade;referencia_norma;gravidade;pessoas_dia;custo;intervencao;coletado_por;data_coleta\n",
            # Linha válida
            "Academia > Entrada;VALID-01;Entrada;tipo_a;Descricao suficientemente longa para o teste;10;cm;20;3;100;500.00;Intervencao;Tester;2026-10-15\n",
            # Linha com menos de 14 campos
            "Incompleta;com;poucos;campos\n",
            # Linha com valor não numérico em campo numérico
            "Academia > Entrada;ERRO-02;Entrada;tipo_a;Descricao suficientemente longa;dez;cm;20;3;100;500;Intervencao;Tester;2026-10-15\n",
            # Linha com gravidade inválida (> 5)
            "Academia > Entrada;ERRO-03;Entrada;tipo_a;Descricao suficientemente longa;10;cm;20;9;100;500;Intervencao;Tester;2026-10-15\n",
            # Linha com custo zero
            "Academia > Entrada;ERRO-04;Entrada;tipo_a;Descricao suficientemente longa;10;cm;20;4;100;0.00;Intervencao;Tester;2026-10-15\n",
            # Linha com descrição curta
            "Academia > Entrada;ERRO-05;Entrada;tipo_a;Curta;10;cm;20;4;100;50.00;Intervencao;Tester;2026-10-15\n",
        ]
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False) as f:
            f.writelines(linhas)
            caminho = f.name
        try:
            registros, erros = coleta.importar_ficha_campo(caminho)
            self.assertEqual(len(registros), 1)
            self.assertEqual(registros[0]["codigo"], "VALID-01")
            self.assertEqual(len(erros), 5)
            self.assertTrue(any("esperados 14 campos" in e for e in erros))
            self.assertTrue(any("valor numerico invalido" in e for e in erros))
            self.assertTrue(any("gravidade deve estar entre 1 e 5" in e for e in erros))
            self.assertTrue(any("custo deve ser maior que zero" in e for e in erros))
            self.assertTrue(any("descricao curta demais" in e for e in erros))
        finally:
            os.remove(caminho)

    def test_persistencia_json_estresse_roundtrip(self):
        setor_orig = {
            "nome": "Setor Acentuado - Ação & Reação ♿",
            "barreiras": [barreira_base(codigo="UTF-01", descricao="Descrição com caracteres acentuados: café, maçã, corrimão")],
            "subsetores": [
                {
                    "nome": "Subsetor Profundo",
                    "barreiras": [barreira_base(codigo="UTF-02", custo=12345.67)],
                    "subsetores": []
                }
            ]
        }
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False, suffix=".json") as f:
            caminho = f.name
        try:
            coleta.gravar_inventario(caminho, setor_orig)
            carregado = coleta.ler_inventario(caminho)
            self.assertEqual(carregado["nome"], setor_orig["nome"])
            self.assertEqual(carregado["barreiras"][0]["descricao"], setor_orig["barreiras"][0]["descricao"])
            self.assertEqual(carregado["subsetores"][0]["barreiras"][0]["custo"], 12345.67)
            # Validar estrutura JSON recarregada
            self.assertEqual(coleta.validar_setor(carregado), [])
        finally:
            os.remove(caminho)


if __name__ == "__main__":
    unittest.main(verbosity=2)
