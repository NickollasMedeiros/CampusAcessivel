# Campus Acessível - Academia Fusion

Sistema de inventário e priorização de intervenções de acessibilidade da Academia Fusion, desenvolvido para a disciplina **Construção de Algoritmos e Programação (2026/2)** do UNASP - Engenharia de Computação.

**Grupo 11:**
- Nickollas Teixeira Medeiros
- Felipe Allan Nascimento Cruz
- João Gabriel

---

## 1. Estrutura do Projeto

Os seis módulos obrigatórios do projeto estão localizados diretamente na raiz:

- `main.py`: Menu interativo com 10 opções (0 a 9) e fluxo principal da aplicação.
- `coleta.py`: Validação de registros, montagem da árvore hierárquica, importação da ficha de campo e persistência em JSON.
- `recursao.py`: Percursos recursivos da árvore (contagem, custo total, profundidade, achatamento, caminho) e resolução do problema da mochila (estratégia gulosa e exaustiva com poda de inviáveis).
- `ordenacao.py`: Algoritmos Bubble Sort, Selection Sort e Insertion Sort com contadores de comparações e trocas, cálculo do índice de prioridade e conferência com `sorted()`.
- `busca.py`: Busca Sequencial, Busca Binária Iterativa e Busca Binária Recursiva com casos base explicitados.
- `relatorio.py`: Matriz ambiente x tipo de barreira, formatação de tabelas e processamento dos cinco achados analíticos (A1 a A5).

Arquivos complementares:
- `inventario.json`: Persistência oficial da árvore hierárquica do setor (15 barreiras, 5 ambientes, 3 níveis).
- `ficha_de_campo.txt`: Dados tabulados da coleta de campo com 14 campos por linha separados por ponto e vírgula.
- `relatorio.txt`: Relatório analítico completo gerado automaticamente pelo programa.
- `caderno_de_bordo.txt`: Histórico das sessões de trabalho e as 3 seções obrigatórias (Divisão de Responsabilidades, Registro de Uso de IA e Defeito Encontrado).
- `fotos/`: 15 registros fotográficos identificados pelo código da barreira (`ACA-REC-01` a `ACA-TRE-15`).
- `tests/test_campus.py`: Suíte de 21 testes unitários automatizados.
- `docs/`: Cotação de preços, relatórios parciais e materiais de apoio.

---

## 2. Como Executar o Sistema

No terminal PowerShell ou CMD, a partir da pasta raiz:

```powershell
python main.py
```

### Menu de Opções Disponíveis:
```text
1. Importar ficha de campo
2. Cadastrar / editar / remover barreira
3. Ver estrutura do setor (resumo hierarquico)
4. Ranking de prioridade (bubble / selection / insertion)
5. Localizar barreira por codigo (sequencial / binaria iterativa / binaria recursiva)
6. Matriz ambiente x tipo de barreira
7. Plano de intervencao sob orcamento (guloso x exaustivo)
8. Relatorio de desempenho dos algoritmos
9. Gravar relatorio em arquivo
0. Sair
```

### Atalhos via Linha de Comando:
- Gerar ou recarregar `inventario.json` a partir de `ficha_de_campo.txt`:
  ```powershell
  python main.py --gerar-inventario
  ```
- Gerar o arquivo `relatorio.txt` diretamente:
  ```powershell
  python main.py --gerar-relatorio
  ```

---

## 3. Como Executar os Testes Automatizados

Para rodar todos os 21 testes unitários:

```powershell
python -m unittest tests/test_campus.py -v
```

---

## 4. Validação de Sintaxe

Para verificar a compilação de todos os módulos sem erros:

```powershell
python -m py_compile main.py coleta.py recursao.py ordenacao.py busca.py relatorio.py
```

---

## 5. Checklist da Entrega (Seção 15)

- [x] `main.py`, `coleta.py`, `recursao.py`, `ordenacao.py`, `busca.py`, `relatorio.py`
- [x] `inventario.json` com no mínimo 15 barreiras, 3 ambientes e 2 níveis
- [x] `ficha_de_campo.txt` preenchida e validada
- [x] `fotos/` com uma foto por barreira nomeada pelo código
- [x] `relatorio.txt` gerado diretamente pelo próprio programa
- [x] `caderno_de_bordo.txt` com as três seções obrigatórias
- [x] O programa roda estritamente com `python main.py` usando apenas a biblioteca padrão
- [x] Todas as funções recursivas possuem casos base identificados em comentários
- [x] Todo número citado no relatório é reproduzível na execução do sistema
