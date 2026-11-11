"""
Script utilitário para gerar versões formatadas em HTML e PDF dos entregáveis:
1. relatorio.pdf (Relatório Técnico com os 5 Achados A1-A5)
2. ficha_de_campo.pdf (Ficha de campo preenchida e pronta para impressão/assinatura)
3. caderno_de_bordo.pdf (Caderno de bordo fechado para a Entrega E4)
4. ficha_revisao_por_pares.pdf (Ficha oficial de avaliação por pares)

Utiliza o navegador Google Chrome ou Microsoft Edge em modo headless para gerar
PDFs de alta definição sem necessitar de nenhuma biblioteca externa pip.
"""

import os
import subprocess
import sys

DIRETORIO_RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, DIRETORIO_RAIZ)

import coleta
import recursao
import ordenacao
import busca
import relatorio


def localizar_navegador():
    caminhos = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    ]
    for c in caminhos:
        if os.path.exists(c):
            return c
    return None


def converter_html_para_pdf(caminho_html, caminho_pdf):
    navegador = localizar_navegador()
    if not navegador:
        print("Navegador não encontrado para conversão direta de PDF. Abra o HTML e salve como PDF.")
        return False
    comando = [
        navegador,
        "--headless",
        "--disable-gpu",
        "--run-all-compositor-stages-before-draw",
        f"--print-to-pdf={caminho_pdf}",
        caminho_html
    ]
    res = subprocess.run(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return res.returncode == 0 and os.path.exists(caminho_pdf)


def gerar_relatorio_html(setor, pesos, caminho_saida):
    conteudo_txt = relatorio.gerar_relatorio_completo(setor, pesos)
    
    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>Relatório Técnico - Campus Acessível</title>
<style>
  @page {{
    size: A4;
    margin: 18mm;
  }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    line-height: 1.45;
    color: #24292f;
    margin: 0;
    padding: 15px;
    background: #fff;
  }}
  h1 {{ font-size: 20px; margin-bottom: 4px; color: #0969da; border-bottom: 2px solid #0969da; padding-bottom: 6px; }}
  pre {{
    background-color: #f6f8fa;
    border: 1px solid #d0d7de;
    border-radius: 6px;
    padding: 12px;
    font-family: "Cascadia Code", "Consolas", monospace;
    font-size: 10px;
    line-height: 1.35;
    white-space: pre-wrap;
    word-break: break-word;
  }}
  .meta {{
    font-size: 11px;
    color: #57606a;
    margin-bottom: 16px;
  }}
</style>
</head>
<body>
<h1>Campus Acessível - Relatório Técnico dos Cinco Achados</h1>
<div class="meta">
  <strong>UNASP - Engenharia de Computação (2026/2)</strong><br>
  <strong>Disciplina:</strong> Construção de Algoritmos e Programação | <strong>Professor:</strong> Eduardo Mendes Oliveira<br>
  <strong>Grupo 11:</strong> Nickollas Teixeira Medeiros, Felipe Allan Nascimento Cruz, João Gabriel<br>
  <strong>Setor:</strong> Academia Fusion
</div>

<pre>{conteudo_txt}</pre>

</body>
</html>"""
    with open(caminho_saida, "w", encoding="utf-8") as f:
        f.write(html)


def gerar_ficha_campo_html(caminho_ficha, caminho_saida):
    registros, _ = coleta.importar_ficha_campo(caminho_ficha)
    linhas_tabela = []
    for r in registros:
        linhas_tabela.append(f"""
        <tr>
          <td><strong>{r['codigo']}</strong></td>
          <td>{r['ambiente']}</td>
          <td>{r['tipo']}</td>
          <td>{r['descricao']}</td>
          <td>{r['medida']} {r['unidade']}</td>
          <td>{r['referencia_norma']} {r['unidade']}</td>
          <td>{r['gravidade']}</td>
          <td>{r['pessoas_dia']}</td>
          <td>R$ {r['custo']:.2f}</td>
          <td>{r['intervencao']}</td>
          <td>{r['coletado_por']}</td>
        </tr>
        """)
    
    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>Ficha de Campo - Campus Acessível</title>
<style>
  @page {{
    size: A4 landscape;
    margin: 12mm;
  }}
  body {{
    font-family: Arial, sans-serif;
    font-size: 10px;
    margin: 0;
    padding: 10px;
  }}
  h1 {{ font-size: 16px; margin: 0 0 4px 0; color: #003366; }}
  .sub {{ font-size: 11px; color: #555; margin-bottom: 12px; }}
  table {{
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 20px;
  }}
  th, td {{
    border: 1px solid #ccc;
    padding: 5px 6px;
    text-align: left;
    vertical-align: middle;
  }}
  th {{
    background-color: #f0f4f8;
    color: #333;
    font-weight: bold;
    font-size: 9.5px;
  }}
  tr:nth-child(even) {{ background-color: #fafafa; }}
  .assinaturas {{
    margin-top: 30px;
    display: flex;
    justify-content: space-between;
    text-align: center;
    font-size: 11px;
  }}
  .campo-ass {{
    border-top: 1px solid #000;
    width: 28%;
    padding-top: 4px;
  }}
</style>
</head>
<body>
<h1>Campus Acessível - Ficha de Campo Oficial (Inventário de Barreiras)</h1>
<div class="sub">Setor: <strong>Academia Fusion</strong> | Grupo 11 - Engenharia de Computação | Data: Outubro/Novembro 2026</div>

<table>
  <thead>
    <tr>
      <th>Código</th>
      <th>Ambiente</th>
      <th>Tipo</th>
      <th>Descrição</th>
      <th>Medida</th>
      <th>Norma</th>
      <th>Grav.</th>
      <th>Alcance</th>
      <th>Custo</th>
      <th>Intervenção</th>
      <th>Coletor</th>
    </tr>
  </thead>
  <tbody>
    {''.join(linhas_tabela)}
  </tbody>
</table>

<div class="assinaturas">
  <div class="campo-ass">Nickollas Teixeira Medeiros</div>
  <div class="campo-ass">Felipe Allan Nascimento Cruz</div>
  <div class="campo-ass">João Gabriel</div>
</div>

</body>
</html>"""
    with open(caminho_saida, "w", encoding="utf-8") as f:
        f.write(html)


def gerar_caderno_html(caminho_caderno, caminho_saida):
    with open(caminho_caderno, "r", encoding="utf-8") as f:
        texto = f.read()

    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>Caderno de Bordo - Grupo 11</title>
<style>
  @page {{
    size: A4;
    margin: 18mm;
  }}
  body {{
    font-family: Arial, sans-serif;
    font-size: 11px;
    line-height: 1.5;
    padding: 15px;
  }}
  h1 {{ font-size: 16px; color: #111; border-bottom: 2px solid #333; padding-bottom: 4px; }}
  pre {{
    font-family: Arial, sans-serif;
    font-size: 11px;
    white-space: pre-wrap;
    line-height: 1.5;
  }}
</style>
</head>
<body>
<pre>{texto}</pre>
</body>
</html>"""
    with open(caminho_saida, "w", encoding="utf-8") as f:
        f.write(html)


def gerar_revisao_pares_html(caminho_saida):
    html = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>Ficha de Revisão por Pares - Campus Acessível</title>
<style>
  @page {
    size: A4;
    margin: 15mm;
  }
  body {
    font-family: Arial, sans-serif;
    font-size: 11px;
    line-height: 1.4;
    padding: 10px;
    color: #222;
  }
  h1 { font-size: 16px; margin: 0 0 6px 0; color: #003366; text-align: center; }
  h2 { font-size: 13px; margin: 12px 0 6px 0; color: #333; border-bottom: 1px solid #ccc; padding-bottom: 3px; }
  .box-identificacao {
    border: 1px solid #999;
    padding: 8px;
    margin-bottom: 12px;
    background: #fdfdfd;
  }
  table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 12px;
  }
  th, td {
    border: 1px solid #888;
    padding: 5px 6px;
    text-align: left;
    font-size: 10.5px;
  }
  th { background-color: #eee; font-weight: bold; }
  .check { text-align: center; width: 45px; }
  .comentario {
    border: 1px solid #999;
    height: 60px;
    margin-bottom: 12px;
    padding: 6px;
  }
  .assinaturas {
    margin-top: 25px;
    display: flex;
    justify-content: space-between;
    text-align: center;
  }
  .linha-ass {
    border-top: 1px solid #000;
    width: 45%;
    padding-top: 4px;
    font-size: 10.5px;
  }
</style>
</head>
<body>
<h1>UNASP - Construção de Algoritmos e Programação (2026/2)</h1>
<h2 style="text-align: center; border: none; margin-top: 0;">Ficha de Revisão por Pares — Checkpoint 2 (E4)</h2>

<div class="box-identificacao">
  <strong>Grupo Avaliado:</strong> Grupo 11 — Academia Fusion<br>
  <strong>Integrantes Avaliados:</strong> Nickollas Teixeira Medeiros, Felipe Allan Nascimento Cruz, João Gabriel<br>
  <strong>Grupo Revisor:</strong> Grupo Nº: ______ &nbsp;&nbsp;|&nbsp;&nbsp; Setor Avaliado: ___________________________<br>
  <strong>Integrantes Revisores:</strong> __________________________________________________________________
</div>

<h2>Itens de Avaliação Técnica</h2>
<table>
  <thead>
    <tr>
      <th>Critério Avaliado</th>
      <th>Descrição da Conformidade</th>
      <th class="check">Atende?</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>1. Escopo Técnico (Seção 5)</strong></td>
      <td>Uso exclusivo da biblioteca padrão do Python, sem OOP, sem banco de dados, sem bibliotecas externas.</td>
      <td class="check">[ &nbsp; ] Sim<br>[ &nbsp; ] Não</td>
    </tr>
    <tr>
      <td><strong>2. Módulos Obrigatórios (Seção 7)</strong></td>
      <td>Presença na raiz de: main.py, coleta.py, recursao.py, ordenacao.py, busca.py, relatorio.py.</td>
      <td class="check">[ &nbsp; ] Sim<br>[ &nbsp; ] Não</td>
    </tr>
    <tr>
      <td><strong>3. Execução no Terminal</strong></td>
      <td>O programa executa diretamente com python main.py exibindo menu numerado completo (0 a 9).</td>
      <td class="check">[ &nbsp; ] Sim<br>[ &nbsp; ] Não</td>
    </tr>
    <tr>
      <td><strong>4. Recursão e Casos Base (Seção 7.2)</strong></td>
      <td>Percurso da árvore por recursão e todas as funções recursivas com caso base identificado em comentário.</td>
      <td class="check">[ &nbsp; ] Sim<br>[ &nbsp; ] Não</td>
    </tr>
    <tr>
      <td><strong>5. Ordenação e Busca Próprias</strong></td>
      <td>Implementação própria de Bubble, Selection, Insertion, Sequencial, Binária Iterativa e Recursiva com contadores.</td>
      <td class="check">[ &nbsp; ] Sim<br>[ &nbsp; ] Não</td>
    </tr>
    <tr>
      <td><strong>6. Divergência Guloso x Exaustivo</strong></td>
      <td>Comprovação em pelo menos um orçamento em que a estratégia gulosa perde para a exaustiva.</td>
      <td class="check">[ &nbsp; ] Sim<br>[ &nbsp; ] Não</td>
    </tr>
    <tr>
      <td><strong>7. Inventário e Fotos</strong></td>
      <td>No mínimo 15 barreiras em inventario.json e fotos correspondentes na pasta fotos/.</td>
      <td class="check">[ &nbsp; ] Sim<br>[ &nbsp; ] Não</td>
    </tr>
  </tbody>
</table>

<h2>Parecer do Grupo Revisor</h2>
<div class="comentario">
  Observações e recomendações sobre o trabalho revisado:
</div>

<div class="assinaturas">
  <div class="linha-ass">Representante do Grupo Avaliado (Grupo 11)</div>
  <div class="linha-ass">Representante do Grupo Revisor</div>
</div>

</body>
</html>"""
    with open(caminho_saida, "w", encoding="utf-8") as f:
        f.write(html)


def main():
    setor = coleta.ler_inventario(os.path.join(DIRETORIO_RAIZ, "inventario.json"))
    pesos = {"gravidade": 0.6, "pessoas_dia": 0.4}

    docs_dir = os.path.join(DIRETORIO_RAIZ, "docs")
    
    html_relatorio = os.path.join(docs_dir, "relatorio.html")
    pdf_relatorio = os.path.join(DIRETORIO_RAIZ, "relatorio.pdf")
    
    html_ficha = os.path.join(docs_dir, "ficha_de_campo.html")
    pdf_ficha = os.path.join(DIRETORIO_RAIZ, "ficha_de_campo.pdf")

    html_caderno = os.path.join(docs_dir, "caderno_de_bordo.html")
    pdf_caderno = os.path.join(DIRETORIO_RAIZ, "caderno_de_bordo.pdf")

    html_pares = os.path.join(docs_dir, "ficha_revisao_por_pares.html")
    pdf_pares = os.path.join(DIRETORIO_RAIZ, "ficha_revisao_por_pares.pdf")

    print("Gerando HTMLs em docs/...")
    gerar_relatorio_html(setor, pesos, html_relatorio)
    gerar_ficha_campo_html(os.path.join(DIRETORIO_RAIZ, "ficha_de_campo.txt"), html_ficha)
    gerar_caderno_html(os.path.join(DIRETORIO_RAIZ, "caderno_de_bordo.txt"), html_caderno)
    gerar_revisao_pares_html(html_pares)
    print("HTMLs gerados com sucesso.")

    print("Renderizando PDFs via navegador headless...")
    converter_html_para_pdf(html_relatorio, pdf_relatorio)
    converter_html_para_pdf(html_ficha, pdf_ficha)
    converter_html_para_pdf(html_caderno, pdf_caderno)
    converter_html_para_pdf(html_pares, pdf_pares)
    print("PDFs gerados:")
    for p in [pdf_relatorio, pdf_ficha, pdf_caderno, pdf_pares]:
        if os.path.exists(p):
            print(f"- {p} ({os.path.getsize(p)} bytes)")


if __name__ == "__main__":
    main()
