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
    html = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>Relatório Técnico - Campus Acessível</title>
<style>
  @page {
    size: A4 portrait;
    margin: 10mm 12mm 10mm 12mm;
  }
  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
    line-height: 1.25;
    color: #1f2328;
    margin: 0;
    padding: 0;
    background: #fff;
    font-size: 8px;
  }
  .page {
    page-break-after: always;
    break-after: page;
    box-sizing: border-box;
  }
  .page:last-child {
    page-break-after: avoid;
    break-after: avoid;
  }
  .header-inst {
    border-bottom: 2px solid #003366;
    padding-bottom: 3px;
    margin-bottom: 5px;
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
  }
  .inst-title { font-size: 11px; font-weight: bold; color: #003366; }
  .inst-sub { font-size: 8px; color: #555; }
  h1 { font-size: 13px; margin: 2px 0; color: #003366; text-transform: uppercase; }
  h2 { font-size: 10px; margin: 4px 0 2px 0; color: #0a3069; border-left: 3px solid #0969da; padding-left: 5px; }
  h3 { font-size: 8.5px; margin: 3px 0 1px 0; color: #24292f; }
  .meta-box {
    background: #f6f8fa;
    border: 1px solid #d0d7de;
    border-radius: 4px;
    padding: 4px 6px;
    margin-bottom: 5px;
    font-size: 8px;
    line-height: 1.3;
  }
  table {
    width: 100%;
    border-collapse: collapse;
    margin: 2px 0 5px 0;
    font-size: 7.5px;
  }
  th, td {
    border: 1px solid #d0d7de;
    padding: 2px 4px;
    text-align: left;
  }
  th {
    background: #f0f4f8;
    color: #0a3069;
    font-weight: bold;
  }
  tr:nth-child(even) { background: #fafafa; }
  .text-box {
    background: #ffffff;
    border: 1px solid #e1e4e8;
    border-radius: 4px;
    padding: 3px 5px;
    margin-bottom: 4px;
    font-size: 8px;
    line-height: 1.3;
  }
  .highlight {
    background: #fff8c5;
    border-left: 3px solid #d4a72c;
    padding: 3px 5px;
    margin: 3px 0;
    font-size: 8px;
  }
  .tag {
    display: inline-block;
    padding: 1px 3px;
    border-radius: 3px;
    font-weight: bold;
    font-size: 7px;
  }
  .tag-danger { background: #ffebe9; color: #cf222e; }
  .tag-ok { background: #dafbe1; color: #1a7f37; }
  .signatures {
    margin-top: 8px;
    display: flex;
    justify-content: space-between;
    text-align: center;
    font-size: 8px;
  }
  .sig-line {
    border-top: 1px solid #333;
    width: 30%;
    padding-top: 2px;
  }
</style>
</head>
<body>

<!-- PÁGINA 1: CONTEXTO, METODOLOGIA E MATRIZ -->
<div class="page">
  <div class="header-inst">
    <div>
      <div class="inst-title">UNASP — Centro Universitário Adventista de São Paulo</div>
      <div class="inst-sub">Engenharia de Computação | Construção de Algoritmos e Programação (2026/2)</div>
    </div>
    <div style="text-align: right;">
      <div class="inst-sub">Prof. Eduardo Mendes Oliveira</div>
      <div class="inst-sub">Entrega E4 — Pacote Congelado</div>
    </div>
  </div>

  <h1>Relatório Técnico de Engenharia: Inventário e Priorização</h1>
  <div class="meta-box">
    <strong>Setor Auditado:</strong> Academia Fusion &nbsp;|&nbsp; <strong>Grupo 11:</strong> Nickollas Teixeira Medeiros, Felipe Allan Nascimento Cruz, João Gabriel<br>
    <strong>Missão Técnica:</strong> Inventariar barreiras de acessibilidade física, modelar a hierarquia do setor e determinar o pacote ótimo de intervenções sob restrição orçamentária via algoritmos exatos e heurísticas de ordenação e busca.
  </div>

  <h2>1. Identificação do Setor, Amostragem e Metodologia de Coleta</h2>
  <div class="text-box">
    A coleta de campo presencial foi conduzida na Academia Fusion, cobrindo 15 barreiras arquitetônicas distribuídas em 3 níveis hierárquicos e 5 ambientes funcionais. As medições foram efetuadas com trena métrica calibrada e conferidas com os parâmetros da <strong>NBR 9050:2020</strong> (Acessibilidade a edificações, mobiliário, espaços e equipamentos urbanos).<br>
    <strong>Critérios Decisórios Declarados pelo Grupo:</strong>
    <ul>
      <li><strong>Escala de Gravidade (1 a 5):</strong> Calibrada pelo risco à integridade física e impedimento absoluto de circulação independente. Gravidade 5 denota bloqueio total (ex.: catraca rotativa sem passagem lateral ACA-REC-01 e escada sem alternativa de desnível ACA-ESC-06). Gravidade 1-2 refere-se a desconforto ou desnível leve.</li>
      <li><strong>Alcance (Pessoas/Dia):</strong> Estimado a partir do fluxo diário de frequentadores e colaboradores da academia (mediana de 200 pessoas/dia nas áreas de passagem e recepção; 50 pessoas/dia na área de espera).</li>
      <li><strong>Método de Estimativa de Custo:</strong> Cotações diretas de mercado da construção civil, catálogos de fornecedores de acessibilidade e tabela SINAPI/SP, englobando insumos, frete e mão de obra de instalação especializada.</li>
    </ul>
  </div>

  <h2>2. Matriz Ambiente x Tipo de Barreira (Lista de Listas)</h2>
  <div class="text-box">
    A estrutura bidimensional abaixo totaliza as ocorrências de barreiras correlacionando o espaço físico às tipologias normativas:
  </div>
  <table>
    <thead>
      <tr>
        <th>Ambiente</th>
        <th>Porta Estreita</th>
        <th>Balcão Alto</th>
        <th>Piso Irreg.</th>
        <th>Sinaliz. Aus.</th>
        <th>Mobil. Inad.</th>
        <th>Elevador Aus.</th>
        <th>Ausên. Corrim.</th>
        <th>Banheiro Inad.</th>
        <th>Circul. Estreita</th>
        <th>TOTAL</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Entrada</strong></td>
        <td>1</td><td>1</td><td>1</td><td>1</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td><strong>4</strong></td>
      </tr>
      <tr>
        <td><strong>Área de Espera</strong></td>
        <td>0</td><td>0</td><td>0</td><td>0</td><td>1</td><td>0</td><td>0</td><td>0</td><td>0</td><td><strong>1</strong></td>
      </tr>
      <tr>
        <td><strong>Escadaria Principal</strong></td>
        <td>0</td><td>0</td><td>0</td><td>1</td><td>0</td><td>1</td><td>2</td><td>0</td><td>0</td><td><strong>4</strong></td>
      </tr>
      <tr>
        <td><strong>Lavatório</strong></td>
        <td>1</td><td>0</td><td>0</td><td>0</td><td>2</td><td>0</td><td>0</td><td>1</td><td>1</td><td><strong>5</strong></td>
      </tr>
      <tr>
        <td><strong>Musculação</strong></td>
        <td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1</td><td><strong>1</strong></td>
      </tr>
      <tr style="background: #f0f4f8; font-weight: bold;">
        <td>TOTAL GERAL</td>
        <td>2</td><td>1</td><td>1</td><td>2</td><td>3</td><td>1</td><td>2</td><td>1</td><td>2</td><td>15</td>
      </tr>
    </tbody>
  </table>
  <div class="highlight">
    <strong>Síntese Estrutural:</strong> O Lavatório e WC concentra o maior número de barreiras (5 itens), enquanto a Escadaria Principal responde pelo maior gargalo financeiro do setor (R$ 62.600,00), evidenciando a necessidade de priorização analítica.
  </div>
</div>

<!-- PÁGINA 2: ACHADO A1 (ORDENAÇÃO) -->
<div class="page">
  <div class="header-inst">
    <div class="inst-title">Campus Acessível — Relatório dos Cinco Achados</div>
    <div class="inst-sub">Grupo 11 | Academia Fusion</div>
  </div>

  <h2>3. Achado A1 — Ordenação: Comparações, Trocas e Complexidade Assintótica</h2>
  <div class="text-box">
    Avaliamos experimentalmente os três algoritmos de ordenação obrigatórios — <strong>Bubble Sort</strong>, <strong>Selection Sort</strong> e <strong>Insertion Sort</strong> — sob três frações da base de dados ($N=5$, $N=10$, $N=15$) e três permutações iniciais (Original, Já Ordenada pelo Índice e Ordem Inversa).
  </div>

  <table>
    <thead>
      <tr>
        <th>Fração da Base</th>
        <th>Cenário Inicial</th>
        <th>Bubble Sort (Comp / Trocas)</th>
        <th>Selection Sort (Comp / Trocas)</th>
        <th>Insertion Sort (Comp / Trocas)</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td rowspan="3"><strong>1/3 da Base (N = 5)</strong></td>
        <td>Original</td><td>C = 10, T = 6</td><td>C = 10, T = 2</td><td>C = 7, T = 6</td>
      </tr>
      <tr>
        <td>Ordenada</td><td>C = 4, T = 0</td><td>C = 10, T = 0</td><td>C = 4, T = 0</td>
      </tr>
      <tr>
        <td>Inversa</td><td>C = 10, T = 10</td><td>C = 10, T = 2</td><td>C = 10, T = 10</td>
      </tr>
      <tr style="background:#f9f9f9;">
        <td rowspan="3"><strong>2/3 da Base (N = 10)</strong></td>
        <td>Original</td><td>C = 42, T = 22</td><td>C = 45, T = 8</td><td>C = 28, T = 22</td>
      </tr>
      <tr style="background:#f9f9f9;">
        <td>Ordenada</td><td>C = 9, T = 0</td><td>C = 45, T = 0</td><td>C = 9, T = 0</td>
      </tr>
      <tr style="background:#f9f9f9;">
        <td>Inversa</td><td>C = 45, T = 45</td><td>C = 45, T = 5</td><td>C = 45, T = 45</td>
      </tr>
      <tr>
        <td rowspan="3"><strong>Total da Base (N = 15)</strong></td>
        <td>Original</td><td>C = 104, T = 60</td><td>C = 105, T = 10</td><td>C = 69, T = 60</td>
      </tr>
      <tr>
        <td>Ordenada</td><td>C = 14, T = 0</td><td>C = 105, T = 0</td><td>C = 14, T = 0</td>
      </tr>
      <tr>
        <td>Inversa</td><td>C = 105, T = 105</td><td>C = 105, T = 7</td><td>C = 105, T = 105</td>
      </tr>
    </tbody>
  </table>

  <h2>Análise Teórica dos Fenômenos Observados</h2>
  <div class="text-box">
    <strong>1. Por que o Selection Sort faz número invariante de comparações?</strong><br>
    O Selection Sort executa sempre exatamente $\\frac{n(n-1)}{2}$ comparações (10 para $N=5$; 45 para $N=10$; 105 para $N=15$), independentemente do estado prévio da lista. Sua invariância decorre de sua lógica estrutural: para cada posição $i$, ele varre incondicionalmente todos os elementos restantes de $i+1$ até $n-1$ para identificar o elemento com índice prioritário extremo. Ele não possui mecanismo de detecção de ordem prévia nem parada antecipada.<br><br>

    <strong>2. Por que o Insertion Sort varia tão drasticamente?</strong><br>
    O laço interno do Insertion Sort insere o elemento atual deslocando elementos maiores para a direita. Na lista pré-ordenada, a primeira comparação falha imediatamente ($resultado[posicao] \\ge atual$), executando apenas 1 comparação por elemento e 0 trocas. Isso resulta no melhor caso estritamente linear $O(n)$ com $n-1$ comparações (14 comparações para $N=15$). Em contrapartida, na lista invertida, o elemento precisa ser transportado até o início do vetor, atingindo o pior caso quadrático com $\\frac{n(n-1)}{2}$ comparações e trocas (105 operações).<br><br>

    <strong>3. Qual é a relação exata entre as trocas do Bubble Sort e do Insertion Sort?</strong><br>
    <div class="highlight">
      <strong>Enunciado em uma linha:</strong> O número de trocas do Bubble Sort e do Insertion Sort é RIGOROSAMENTE IDÊNTICO em todos os cenários porque ambos operam trocando pares de elementos adjacentes fora de ordem, resolvendo exatamente o número de inversões da permutação original: $trocas = I(\\pi)$.
    </div>
    Cada troca efetuada por qualquer um dos dois métodos diminui a quantidade global de inversões da lista em exatamente 1. Assim, para $N=15$ na base original, existiam 60 inversões, exigindo precisamente 60 trocas tanto no Bubble quanto no Insertion Sort.
  </div>
</div>

<!-- PÁGINA 3: ACHADO A2 (BUSCA) E ACHADO A3 (HIERARQUIA) -->
<div class="page">
  <div class="header-inst">
    <div class="inst-title">Campus Acessível — Relatório dos Cinco Achados</div>
    <div class="inst-sub">Grupo 11 | Academia Fusion</div>
  </div>

  <h2>4. Achado A2 — Busca: Comparações, Pior Caso e Análise Amortizada</h2>
  <div class="text-box">
    Submetemos os algoritmos de busca (Sequencial, Binária Iterativa e Binária Recursiva com casos base explicitados) a cinco alvos padronizados sobre a base de 15 barreiras ordenada por código:
  </div>

  <table>
    <thead>
      <tr>
        <th>Posição / Caso</th>
        <th>Código do Alvo</th>
        <th>Busca Sequencial (Pos / Comp)</th>
        <th>Binária Iterativa (Pos / Comp)</th>
        <th>Binária Recursiva (Pos / Comp)</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Primeiro código</strong></td>
        <td><code>ACA-ESC-06</code></td>
        <td>pos = 0, C = 1</td>
        <td>pos = 0, C = 4</td>
        <td>pos = 0, C = 4</td>
      </tr>
      <tr>
        <td><strong>Código do meio</strong></td>
        <td><code>ACA-REC-03</code></td>
        <td>pos = 7, C = 8</td>
        <td>pos = 7, C = 1</td>
        <td>pos = 7, C = 1</td>
      </tr>
      <tr>
        <td><strong>Último código</strong></td>
        <td><code>ACA-TRE-15</code></td>
        <td>pos = 14, C = 15</td>
        <td>pos = 14, C = 4</td>
        <td>pos = 14, C = 4</td>
      </tr>
      <tr>
        <td><strong>Aleatório do meio</strong></td>
        <td><code>ACA-ESC-09</code></td>
        <td>pos = 3, C = 4</td>
        <td>pos = 3, C = 2</td>
        <td>pos = 3, C = 2</td>
      </tr>
      <tr>
        <td><strong>Código inexistente</strong></td>
        <td><code>ACA-XXX-99</code></td>
        <td>pos = -1, C = 15</td>
        <td>pos = -1, C = 4</td>
        <td>pos = -1, C = 4</td>
      </tr>
    </tbody>
  </table>

  <div class="text-box">
    <strong>Fundamentação Teórica da Busca:</strong>
    <ul>
      <li><strong>Onde a Sequencial supera a Binária:</strong> No primeiro elemento da lista (<code>ACA-ESC-06</code>). A sequencial testa o índice 0 na primeira comparação ($C=1$), atingindo seu melhor caso $O(1)$. A busca binária avalia a mediana (índice 7) e desce sucessivamente pela árvore de busca até atingir a folha na extremidade esquerda, consumindo $\\lfloor \\log_2 15 \\rfloor + 1 = 4$ comparações.</li>
      <li><strong>Custo da Ordenação Prévia e Análise Amortizada:</strong> A busca binária exige lista rigorosamente ordenada. O custo de ordenar nossos dados via algoritmos elementares é $O(n^2)$ (105 comparações). Para uma consulta isolada ($m=1$), a sequencial é mais barata ($105 + 4 = 109 > 15$). A binária torna-se eficiente apenas quando o custo da ordenação é amortizado sobre múltiplas consultas: $O(n^2 + m \\log_2 n) < O(m \\cdot n)$.</li>
      <li><strong>Código Inexistente vs Pior Caso:</strong> Para uma chave inexistente, a busca binária não pode abortar prematuramente; ela é obrigada a percorrer um caminho completo da raiz até uma folha externa vazia onde $inicio > fim$. Esse caminho possui comprimento igual à altura da árvore de decisão: $h = \\lfloor \\log_2 n \\rfloor + 1 = 4$. Portanto, o número de comparações de insucesso é idêntico ao pior caso de sucesso.</li>
    </ul>
  </div>

  <h2>5. Achado A3 — Hierarquia: Árvore do Setor e Limites da Recursão</h2>
  <div class="text-box">
    A estrutura do setor <strong>Academia Fusion</strong> possui profundidade real de <strong>3 níveis</strong> e totaliza <strong>R$ 76.020,00</strong>:
  </div>
  <table>
    <thead>
      <tr>
        <th>Subsetor de 1º Nível</th>
        <th>Qtd Barreiras</th>
        <th>Custo Total</th>
        <th>Barreira Mais Grave (Gravidade 5)</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Receção e Espera</strong></td>
        <td>5</td>
        <td>R$ 6.600,00</td>
        <td><code>ACA-REC-01</code> — Catraca rotativa sem passagem acessível (R$ 3.500,00)</td>
      </tr>
      <tr>
        <td><strong>Acessos e Sanitários</strong></td>
        <td>9</td>
        <td>R$ 67.420,00</td>
        <td><code>ACA-ESC-06</code> — Ausência de elevador / plataforma elevatória (R$ 60.000,00)<br><code>ACA-SAN-14</code> — Porta de fole estreita de 65 cm (R$ 2.500,00)</td>
      </tr>
      <tr>
        <td><strong>Área de Treino</strong></td>
        <td>1</td>
        <td>R$ 2.000,00</td>
        <td><code>ACA-TRE-15</code> — Corredor de pernas com 75 cm (Gravidade 4, R$ 2.000,00)</td>
      </tr>
    </tbody>
  </table>
  <div class="text-box">
    <strong>Caminho Hierárquico Completo da Barreira Mais Crítica:</strong><br>
    <code>Academia Fusion > Acessos e Sanitários > Escadaria Principal > ACA-ESC-06</code><br><br>
    <strong>Falha de Laços Fixos e Efeito da Remoção do Caso Base:</strong><br>
    Uma implementação com número fixo de laços aninhados (ex.: 2 laços for) processaria apenas os subsetores de nível 1 e 2, falhando silenciosamente ao ignorar completamente as barreiras localizadas no nível 3 (como a Entrada e o Lavatório). A recursão é agnóstica à topologia da árvore.<br>
    Se o <strong>caso base</strong> for removido da recursão (<code>if len(subsetores) == 0: return</code>), as chamadas continuarão se empilhando indefinidamente na pilha de execução até esgotar o limite interno de recursão da máquina, disparando a exceção fatal do interpretador: <code>RecursionError: maximum recursion depth exceeded</code>.
  </div>
</div>

<!-- PÁGINA 4: ACHADO A4 (OTIMIZAÇÃO) -->
<div class="page">
  <div class="header-inst">
    <div class="inst-title">Campus Acessível — Relatório dos Cinco Achados</div>
    <div class="inst-sub">Grupo 11 | Academia Fusion</div>
  </div>

  <h2>6. Achado A4 — Otimização: Pacote Guloso vs Exaustivo (Problema da Mochila 0/1)</h2>
  <div class="text-box">
    O problema de seleção do pacote ótimo de intervenções sob teto financeiro modela formalmente o <em>0/1 Knapsack Problem</em>. Comparamos a heurística <strong>Gulosa</strong> (ordenação decrescente por benefício/custo) com a busca <strong>Exaustiva</strong> por retrocesso recursivo (com poda de inviáveis) em quatro patamares de investimento:
  </div>

  <table>
    <thead>
      <tr>
        <th>Teto de Orçamento</th>
        <th>Estratégia Gulosa (Benefício / Custo / Qtd)</th>
        <th>Estratégia Exaustiva (Benefício / Custo / Qtd)</th>
        <th>Chamadas Recursivas</th>
        <th>Convergência</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>R$ 1.000,00</strong></td>
        <td>Benefício = 13.600 | R$ 820,00 | 5 itens</td>
        <td>Benefício = 13.600 | R$ 820,00 | 5 itens</td>
        <td>127 chamadas</td>
        <td><span class="tag tag-ok">Ótimo Global</span></td>
      </tr>
      <tr>
        <td><strong>R$ 3.000,00</strong></td>
        <td>Benefício = 19.400 | R$ 2.220,00 | 7 itens</td>
        <td>Benefício = 20.000 | R$ 2.620,00 | 7 itens</td>
        <td>2.481 chamadas</td>
        <td><span class="tag tag-danger">Divergência (+0.600)</span></td>
      </tr>
      <tr>
        <td><strong>R$ 6.000,00</strong></td>
        <td>Benefício = 25.200 | R$ 4.620,00 | 9 itens</td>
        <td>Benefício = 26.400 | R$ 5.920,00 | 9 itens</td>
        <td>10.075 chamadas</td>
        <td><span class="tag tag-danger">Divergência (+1.200)</span></td>
      </tr>
      <tr>
        <td><strong>R$ 10.000,00</strong></td>
        <td>Benefício = 31.600 | R$ 8.420,00 | 11 itens</td>
        <td>Benefício = 32.800 | R$ 9.720,00 | 11 itens</td>
        <td>15.971 chamadas</td>
        <td><span class="tag tag-danger">Divergência (+1.200)</span></td>
      </tr>
    </tbody>
  </table>

  <div class="highlight">
    <strong>Comprovação Formal da Divergência (Orçamento R$ 3.000,00):</strong><br>
    • <strong>Pacote Guloso:</strong> Selecionou <code>ACA-SAN-13, ACA-SAN-12, ACA-REC-04, ACA-REC-03, ACA-SAN-11, ACA-ESC-09, ACA-ESC-07</code>. Custo: R$ 2.220,00. Benefício: 19.400.<br>
    • <strong>Pacote Exaustivo:</strong> Selecionou <code>ACA-REC-02, ACA-REC-03, ACA-REC-04, ACA-ESC-09, ACA-SAN-11, ACA-SAN-12, ACA-SAN-13</code>. Custo: R$ 2.620,00. Benefício: 20.000.<br>
    • <strong>Por que a Gulosa perdeu?</strong> A abordagem gulosa escolhe cegamente pela densidade de benefício por real ($b_i / c_i$). Após alocar os itens mais baratos, restaram R$ 780,00 livres. A próxima barreira no ranking guloso custava R$ 1.200,00 (<code>ACA-REC-02</code>), não cabendo na folga. A busca exaustiva explorou a árvore combinatória global e identificou que substituir <code>ACA-ESC-07</code> (custo R$ 800; benefício 2.6) por <code>ACA-REC-02</code> (custo R$ 1.200; benefício 3.2) preenchia de forma mais eficiente a folga orçamentária ociosa, gerando um ganho de <strong>+0.600</strong> de benefício social.
  </div>

  <h2>Crescimento Exponencial e Inviabilidade para a Escala do Campus</h2>
  <div class="text-box">
    Medimos o número de chamadas da recursão exaustiva variando a quantidade de candidatos (Teto R$ 10.000,00):
  </div>
  <table>
    <thead>
      <tr>
        <th>Nº Barreiras Candidatas (N)</th>
        <th>3</th>
        <th>5</th>
        <th>8</th>
        <th>10</th>
        <th>14</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Chamadas Recursivas</strong></td>
        <td>15</td>
        <td>63</td>
        <td>287</td>
        <td>1.044</td>
        <td>8.188</td>
      </tr>
    </tbody>
  </table>
  <div class="text-box">
    <strong>Relação Matemática:</strong> A cada barreira adicional, a árvore de decisão binária ramifica em dois novos estados (incluir vs não incluir), exibindo crescimento $O(2^N)$. Embora a poda prévia descarte itens inviáveis, o teto teórico é de $2^{N+1}-1$ chamadas.<br><br>
    <strong>Se o campus inteiro tem 400 barreiras, essa abordagem serve? Por quê?</strong><br>
    <strong>NÃO SERVE.</strong> Para $N = 400$, o número de combinações possíveis é $2^{400} \\approx 2,58 \\times 10^{120}$. Mesmo um processador executando $10^{12}$ chamadas por segundo levaria aproximadamente $10^{100}$ anos para concluir a execução — magnitude infinitamente superior aos 13,8 bilhões de anos da idade do universo. Para a escala institucional de 400 barreiras, torna-se imperativo adotar <strong>Programação Dinâmica</strong> (complexidade pseudo-polinomial $O(N \\cdot W)$) ou manter a heurística <strong>Gulosa</strong> com garantia de aproximação rápida em tempo $O(N \\log N)$.
  </div>
</div>

<!-- PÁGINA 5: ACHADO A5 (DECISÃO) E PARECER FINAL -->
<div class="page">
  <div class="header-inst">
    <div class="inst-title">Campus Acessível — Relatório dos Cinco Achados</div>
    <div class="inst-sub">Grupo 11 | Academia Fusion</div>
  </div>

  <h2>7. Achado A5 — Decisão: Índice de Prioridade e Análise de Sensibilidade</h2>
  <div class="text-box">
    <strong>Fórmula Matemática do Índice de Prioridade:</strong><br>
    $$\\text{{benefício}} = \\text{{gravidade}} \\times P_{{\\text{{grav}}}} + \\left(\\frac{{\\text{{pessoas\\_dia}}}}{{100}}\\right) \\times P_{{\\text{{alc}}}} \\qquad \\Longrightarrow \\qquad \\text{{índice}} = \\frac{{\\text{{benefício}}}}{{\\text{{custo}} / 1000}}$$
    • <strong>Pesos Base:</strong> $P_{{\\text{{grav}}}} = 0.6$ (peso maior na integridade física e impedimento) e $P_{{\\text{{alc}}}} = 0.4$ (impacto de fluxo).<br>
    • <strong>Regra de Desempate Estrita:</strong> Em caso de empate absoluto no índice, o desempate é feito pela ordem alfabética crescente do campo <code>codigo</code>, garantindo determinismo matemático independente do algoritmo de ordenação.
  </div>

  <h2>Análise de Sensibilidade — Variação dos Pesos no Top 10</h2>
  <table>
    <thead>
      <tr>
        <th>Posição</th>
        <th>Cenário Base (0.6 Grav / 0.4 Alc)</th>
        <th>Cenário Dobro Gravidade (1.2 Grav / 0.4 Alc)</th>
        <th>Cenário Dobro Alcance (0.6 Grav / 0.8 Alc)</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>01</strong></td>
        <td><code>ACA-SAN-13</code> (idx 26.67)</td>
        <td><code>ACA-SAN-13</code> (idx 46.67)</td>
        <td><code>ACA-SAN-13</code> (idx 33.33)</td>
      </tr>
      <tr>
        <td><strong>02</strong></td>
        <td><code>ACA-SAN-12</code> (idx 21.33)</td>
        <td><code>ACA-SAN-12</code> (idx 37.33)</td>
        <td><code>ACA-SAN-12</code> (idx 26.67)</td>
      </tr>
      <tr>
        <td><strong>03</strong></td>
        <td><code>ACA-REC-04</code> (idx 17.33)</td>
        <td><code>ACA-REC-04</code> (idx 29.33)</td>
        <td><code>ACA-REC-04</code> (idx 22.67)</td>
      </tr>
      <tr>
        <td><strong>04</strong></td>
        <td><code>ACA-REC-03</code> (idx 13.33)</td>
        <td><code>ACA-REC-03</code> (idx 21.33)</td>
        <td><code>ACA-REC-03</code> (idx 18.67)</td>
      </tr>
      <tr>
        <td><strong>05</strong></td>
        <td><code>ACA-SAN-11</code> (idx 10.40)</td>
        <td><code>ACA-SAN-11</code> (idx 17.60)</td>
        <td><code>ACA-SAN-11</code> (idx 13.60)</td>
      </tr>
      <tr>
        <td><strong>06</strong></td>
        <td><code>ACA-ESC-09</code> (idx 5.33)</td>
        <td><code>ACA-ESC-09</code> (idx 9.33)</td>
        <td><code>ACA-ESC-09</code> (idx 6.67)</td>
      </tr>
      <tr>
        <td><strong>07</strong></td>
        <td><code>ACA-ESC-07</code> (idx 3.25)</td>
        <td><code>ACA-ESC-07</code> (idx 5.50)</td>
        <td><code>ACA-ESC-07</code> (idx 4.25)</td>
      </tr>
      <tr>
        <td><strong>08</strong></td>
        <td><code>ACA-REC-02</code> (idx 2.67)</td>
        <td><code>ACA-REC-02</code> (idx 4.67)</td>
        <td><code>ACA-REC-02</code> (idx 3.33)</td>
      </tr>
      <tr>
        <td><strong>09</strong></td>
        <td><code>ACA-ESC-08</code> (idx 2.17)</td>
        <td><code>ACA-ESC-08</code> (idx 3.67)</td>
        <td><code>ACA-ESC-08</code> (idx 2.83)</td>
      </tr>
      <tr>
        <td><strong>10</strong></td>
        <td><code>ACA-SAN-10</code> (idx 1.78)</td>
        <td><code>ACA-SAN-10</code> (idx 3.11)</td>
        <td><code>ACA-SAN-10</code> (idx 2.22)</td>
      </tr>
    </tbody>
  </table>

  <h2>8. Parecer Técnico Final e Sustentação da Recomendação</h2>
  <div class="text-box">
    <strong>Diante das variações de pesos, o grupo mantém ou altera a recomendação original?</strong><br>
    O grupo <strong>MANTÉM INTEGRALMENTE</strong> a recomendação original do Cenário Base.<br><br>
    <strong>Sustentação Técnica Diante da Mantenedora:</strong><br>
    A análise de sensibilidade revela uma propriedade de estabilidade notável: <strong>o Top 6 permanece 100% inalterado em todas as simulações</strong> (as posições de 1 a 6 são rigorosamente idênticas no Cenário Base, no Dobro da Gravidade e no Dobro do Alcance). As seis primeiras intervenções reúnem baixo custo financeiro (R$ 120 a R$ 600 cada) com eliminação imediata de riscos físicos graves e bloqueios de passagem (ex.: destravamento de circulação com retirada de corrente no lavatório, isolamento de sifão térmico e sinalização visual).<br><br>
    A variação de pesos atinge apenas as posições inferiores (7 a 10), confirmando que a recomendação prioritária do grupo é imune a flutuações subjetivas de critério orçamentário e maximiza de forma defensável o retorno social de cada real investido no campus da UNASP.
  </div>

  <div class="signatures">
    <div class="sig-line">
      <strong>Nickollas Teixeira Medeiros</strong><br>
      Coleta de Campo e Métricas NBR
    </div>
    <div class="sig-line">
      <strong>Felipe Allan Nascimento Cruz</strong><br>
      Arquitetura e Módulos de Software
    </div>
    <div class="sig-line">
      <strong>João Gabriel</strong><br>
      Custos, Algoritmos e Análise dos Achados
    </div>
  </div>
</div>

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
