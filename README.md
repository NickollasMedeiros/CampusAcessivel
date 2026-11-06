# Campus Acessivel

Sistema de inventario e priorizacao de intervencoes de acessibilidade da Academia Fusion.

## Estrutura

- `main.py`, `coleta.py`, `recursao.py` e `ordenacao.py`: modulos principais exigidos na entrega.
- `inventario.json`: inventario persistido em formato de arvore.
- `ficha_de_campo.txt`: dados de campo usados para gerar o inventario.
- `fotos/`: uma foto por barreira, identificada pelo codigo.
- `caderno_de_bordo.txt`: registro do processo do grupo.
- `tests/`: testes automatizados.
- `docs/`: relatorios, cotacao e documento de referencia.

## Executar o sistema

No terminal, a partir desta pasta:

```powershell
py -3 main.py
```

Opcoes atuais:

- `1`: exibe o resumo hierarquico.
- `2`: exibe o ranking de prioridade.
- `0`: encerra o programa.

## Executar os testes

```powershell
py -3 -m unittest discover -s tests -p "test_*.py" -v
```

## Validar sintaxe

```powershell
py -3 -m py_compile coleta.py recursao.py ordenacao.py main.py
```

## Entrega ao professor

Os seis arquivos obrigatorios devem permanecer na raiz: `main.py`, `coleta.py`,
`recursao.py`, `ordenacao.py`, `busca.py` e `relatorio.py`. Os dois ultimos ainda
serao integrados na entrega final.
