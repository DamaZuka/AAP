# Projeto 1 - Algoritmos de Procura

Este repositório contém o desenvolvimento e a análise do primeiro projeto da unidade curricular de **Algoritmos Avançados de Procura** (AAP).

## Identificação
* **Autora:** Sara Fonseca da Costa Pereira
* **Número de Aluna:** 123562
* **Curso:** Tecnologias Digitais e Inteligência Artificial
* **Instituição:** Escola de Tecnologias Digitais Aplicadas (Iscte-Sintra), Iscte - Instituto Universitário de Lisboa

---

## Descrição do Trabalho
Este projeto tem como foco o estudo e a implementação de diversos paradigmas de procura num espaço de estados bem definido.

### Parte A: Problema 1 - Sliding Puzzle (8-Puzzle e 15-Puzzle)
Implementação e análise comparativa de algoritmos de procura utilizando o jogo do puzzle deslizante.
* **Algoritmos de Procura Não Informada:** Breadth-First Search (BFS) e Depth-First Search (DFS).
* **Algoritmos de Procura Informada:** Greedy Search e A*.
* **Heurísticas Avaliadas:** Número de peças fora do lugar e Distância de Manhattan.

### Parte B: Problema das N-Rainhas
Resolução do problema de colocação de N rainhas não-atacantes num tabuleiro através de algoritmos de procura local.
* **Algoritmos Implementados:** Hill Climbing, Stochastic Hill Climbing, Simulated Annealing, Tabu Search e Stochastic Beam Search.
* **Experiências e Escalabilidade:** Testes de desempenho e sucesso realizados para tabuleiros de dimensões N=8, N=20 e N=50.

---

## Estrutura do Repositório
* `ParteA/`: Diretório contendo os scripts relativos ao Puzzle Deslizante (`main.py`, `algorithms.py`, `node.py`, `puzzle_graph.py`).
* `ParteB/`: Diretório contendo os scripts relativos ao problema das N-Rainhas (`main_nqueens.py`, `nqueens.py`).

---

## Requisitos e Execução
* **Linguagem:** Python 3.12
* **Bibliotecas:** O projeto utiliza exclusivamente bibliotecas nativas do Python (`time`, `csv`, `os`, `heapq`, `random`, `math`). Não é necessária a instalação de dependências externas.

Para reproduzir as experiências, deves executar os seguintes comandos no terminal, a partir do diretório raiz do projeto:
* **Parte A:** `python ParteA/main.py`. Os dados (tempo, estados explorados e comprimento da solução) são registados no ficheiro `resultados_parte_a.csv`.
* **Parte B:** `python ParteB/main_nqueens.py`. As métricas e taxas de sucesso são impressas diretamente na consola.