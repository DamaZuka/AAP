import random
import math


class NQueensState:
    def __init__(self, n, board=None):
        self.n = n
        if board is None:
            # Gera uma configuração aleatória: [linha_rainha_col0, linha_rainha_col1, ...]
            self.board = [random.randint(0, n - 1) for _ in range(n)]
        else:
            self.board = list(board)

    def get_conflicts(self):
        """Calcula o número de pares de rainhas que se atacam mutuamente."""
        conflicts = 0
        for i in range(self.n):
            for j in range(i + 1, self.n):
                # Verifica se partilham a mesma linha ou a mesma diagonal
                if self.board[i] == self.board[j] or abs(self.board[i] - self.board[j]) == abs(i - j):
                    conflicts += 1
        return conflicts

    def get_neighbors(self):
        """Gera todos os estados vizinhos movendo uma rainha ao longo da sua respetiva coluna."""
        neighbors = []
        for col in range(self.n):
            for row in range(self.n):
                if self.board[col] != row:
                    new_board = list(self.board)
                    new_board[col] = row
                    neighbors.append(NQueensState(self.n, new_board))
        return neighbors


def hill_climbing(initial_state, max_iterations=1000):
    """Executa o algoritmo Hill Climbing clássico."""
    current = initial_state
    iterations = 0

    while iterations < max_iterations:
        if current.get_conflicts() == 0:
            break

        neighbors = current.get_neighbors()
        if not neighbors:
            break

        best_neighbor = min(neighbors, key=lambda state: state.get_conflicts())

        if best_neighbor.get_conflicts() >= current.get_conflicts():
            break  # Atingiu um ótimo local

        current = best_neighbor
        iterations += 1

    return current, iterations


def simulated_annealing(initial_state, initial_temp=100.0, cooling_rate=0.95):
    """Executa o algoritmo Simulated Annealing."""
    current = initial_state
    temp = initial_temp
    iterations = 0

    while temp > 0.1:
        if current.get_conflicts() == 0:
            break

        neighbors = current.get_neighbors()
        if not neighbors:
            break

        next_state = random.choice(neighbors)
        delta_e = current.get_conflicts() - next_state.get_conflicts()

        # Aceita se for melhor, ou aceita com probabilidade termodinâmica se for pior
        if delta_e > 0 or random.random() < math.exp(delta_e / temp):
            current = next_state

        temp *= cooling_rate
        iterations += 1

    return current, iterations


def tabu_search(initial_state, tabu_size=10, max_iterations=500):
    """Executa o algoritmo Tabu Search com uma lista de memória."""
    current = initial_state
    best_overall = current
    tabu_list = []
    iterations = 0

    while iterations < max_iterations:
        if current.get_conflicts() == 0:
            break

        neighbors = current.get_neighbors()
        if not neighbors:
            break

        valid_neighbors = []
        for n in neighbors:
            # O critério de aspiração: aceita um vizinho tabu se ele for o melhor estado global até agora
            if tuple(n.board) not in tabu_list or n.get_conflicts() < best_overall.get_conflicts():
                valid_neighbors.append(n)

        if not valid_neighbors:
            break

        best_neighbor = min(valid_neighbors, key=lambda state: state.get_conflicts())
        current = best_neighbor

        if current.get_conflicts() < best_overall.get_conflicts():
            best_overall = current

        # Atualiza a lista tabu
        tabu_list.append(tuple(current.board))
        if len(tabu_list) > tabu_size:
            tabu_list.pop(0)

        iterations += 1

    return best_overall, iterations


def stochastic_beam_search(initial_state, beam_width=3, max_iterations=500):
    """Executa o algoritmo Stochastic Beam Search mantendo k estados simultâneos."""
    n = initial_state.n
    # Inicializa k estados (o estado inicial + k-1 estados aleatórios)
    states = [initial_state] + [NQueensState(n) for _ in range(beam_width - 1)]
    iterations = 0

    while iterations < max_iterations:
        # Verifica se algum dos estados atuais é a solução
        best_state = min(states, key=lambda s: s.get_conflicts())
        if best_state.get_conflicts() == 0:
            return best_state, iterations

        all_neighbors = []
        for state in states:
            all_neighbors.extend(state.get_neighbors())

        if not all_neighbors:
            break

        # Ordena todos os sucessores gerados
        sorted_neighbors = sorted(all_neighbors, key=lambda s: s.get_conflicts())

        # Componente estocástica: em vez de escolher os k estritamente melhores,
        # escolhe aleatoriamente k estados de entre os 2*k melhores
        pool_size = min(len(sorted_neighbors), beam_width * 2)
        pool = sorted_neighbors[:pool_size]
        states = random.sample(pool, min(beam_width, len(pool)))

        iterations += 1

    return min(states, key=lambda s: s.get_conflicts()), iterations


def stochastic_hill_climbing(initial_state, max_iterations=1000, num_samples=100):
    """
    Executa o algoritmo Stochastic Hill Climbing.
    Avalia apenas uma amostra aleatória da vizinhança em cada iteração,
    mitigando a explosão combinatória em tabuleiros de grandes dimensões (ex: N=50).
    """
    current = initial_state
    iterations = 0
    n = current.n

    while iterations < max_iterations:
        if current.get_conflicts() == 0:
            break

        # Geração de uma amostra estocástica de vizinhos
        neighbors = []
        for _ in range(num_samples):
            col = random.randint(0, n - 1)
            row = random.randint(0, n - 1)

            # Assegura que a rainha é movida para uma nova linha
            if current.board[col] != row:
                new_board = list(current.board)
                new_board[col] = row
                neighbors.append(NQueensState(n, new_board))

        if not neighbors:
            break

        # Seleciona o melhor vizinho dentro da amostra gerada
        best_neighbor = min(neighbors, key=lambda state: state.get_conflicts())

        # Critério de paragem: se o melhor da amostra não melhora o estado atual
        if best_neighbor.get_conflicts() >= current.get_conflicts():
            break

        current = best_neighbor
        iterations += 1

    return current, iterations