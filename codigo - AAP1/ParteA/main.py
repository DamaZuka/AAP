import time
import csv
import os
from node import Node
from puzzle_graph import PuzzleGraph
from AAP1.ParteA.algorithms import Algorithms


def log_to_csv(data, filename="resultados_parte_a.csv"):
    """
    Função para guardar os resultados num ficheiro CSV.
    """
    file_exists = os.path.isfile(filename)
    with open(filename, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # Escrever cabeçalho se o ficheiro for novo
        if not file_exists:
            writer.writerow(
                ["Algoritmo", "Heuristica", "Dificuldade", "Tempo(s)", "Estados_Explorados", "Comprimento_Solucao"])
        writer.writerow(data)


def run_experiment(nome_estado, initial_board, search_type, heuristic=None):
    # Definição de limites com base na complexidade do problema
    # O 15-Puzzle requer uma margem substancialmente maior de exploração
    limite_nos = 10000 if "15P" in nome_estado else 5000
    limite_tempo = 60  # Limite de 60 segundos por execução

    # Formatação condicional para exibir a heurística, se aplicável
    heur_str = heuristic if heuristic else "N/A"
    print(f"\n>>> A testar: {search_type} | Heurística: {heur_str} | Estado: {nome_estado}")

    start_node = Node(initial_board)
    end_node = Node(Node.goal_state)

    # Atribuição da heurística caso se trate de uma procura informada
    if heuristic:
        Node.heuristic_type = heuristic

    graph = PuzzleGraph()
    algo = Algorithms(graph)

    start_time = time.time()

    try:
        # Passagem dos limites diretamente para o metodo de pesquisa
        visit_order, path = algo.perform_search(
            search_type,
            start_node,
            end_node,
            max_nodes=limite_nos,
            timeout=limite_tempo
        )

        execution_time = time.time() - start_time

        if not path:
            print("Resultado: Limite excedido ou sem solução (inviável).")
            resultado_log = [search_type, heur_str, nome_estado, None, None, None]
        else:
            solucao_len = len(path) - 1
            print(
                f"Tempo: {execution_time:.4f}s | Estados explorados: {len(visit_order)} | Comprimento da Solução: {solucao_len}")
            resultado_log = [search_type, heur_str, nome_estado, round(execution_time, 4), len(visit_order),
                             solucao_len]

        # Guardar os dados no CSV
        log_to_csv(resultado_log)

    except Exception as e:
        print(f"Erro na execução: {e}")


if __name__ == "__main__":
    # 8-PUZZLE
    Node.goal_state = (1, 2, 3, 4, 5, 6, 7, 8, 0)

    # Dicionário com os estados
    estados_8p = {
        "8P_Facil": (1, 2, 3, 4, 0, 6, 7, 5, 8),
        "8P_Medio": (1, 0, 2, 4, 5, 3, 7, 8, 6),
        "8P_Dificil": (8, 6, 7, 2, 5, 4, 3, 0, 1)
    }

    # Separação das tipologias de algoritmos para facilitar a injeção das heurísticas
    algoritmos_nao_informados = ["Largura Primeiro", "Profundidade Primeiro"]
    algoritmos_informados = ["Greedy BFS", "A*"]

    heuristicas = ["manhattan", "pecas_fora"]

    print(">>> A TESTAR 8-PUZZLE <<<")

    for nome_estado, tabuleiro in estados_8p.items():
        print(f"\n{'=' * 50}\n--- NÍVEL DE DIFICULDADE: {nome_estado.upper()} ---\n{'=' * 50}")

        # Testar algoritmos de procura cega (não informada)
        for alg in algoritmos_nao_informados:
            run_experiment(nome_estado, tabuleiro, alg)

        # Testar algoritmos de procura heurística (informada)
        for alg in algoritmos_informados:
            for heur in heuristicas:
                run_experiment(nome_estado, tabuleiro, alg, heur)

    # 15-PUZZLE
    Node.goal_state = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0)
    estados_15p = {
        "15P_Facil": (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 0, 14, 15),
        "15P_Medio": (1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 11, 12, 13, 10, 14, 15),
        "15P_Dificil": (1, 6, 2, 4, 5, 10, 3, 8, 9, 13, 7, 11, 14, 15, 0, 12)
    }

    print("\n>>> A TESTAR 15-PUZZLE <<<")
    # Para 15-Puzzle, o foco incide na procura informada (A*)
    for nome, tabuleiro in estados_15p.items():
        for heur in heuristicas:
            run_experiment(nome, tabuleiro, "A*", heur)