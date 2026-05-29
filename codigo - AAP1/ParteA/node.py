class Node:
    # Estado objetivo definido pelo enunciado para o 8-puzzle (será reescrito no teste do 15-puzzle)
    goal_state = (1, 2, 3, 4, 5, 6, 7, 8, 0)

    # Variável para controlar qual a heurística a utilizar ('manhattan' ou 'misplaced')
    heuristic_type = 'manhattan'

    def __init__(self, board, parent=None, action=None, depth=0):
        self.board = board
        self.parent = parent
        self.action = action
        self.depth = depth

    def is_goal(self):
        """Verifica se o estado atual é o estado objetivo."""
        return self.board == Node.goal_state

    def get_successors(self):
        """Gera todos os estados válidos a partir da posição atual do espaço vazio (0)."""
        successors = []
        empty_idx = self.board.index(0)

        # Calcula a largura dinamicamente (3 para 8-puzzle, 4 para 15-puzzle)
        width = int(len(self.board) ** 0.5)
        row, col = divmod(empty_idx, width)

        moves = [('Cima', -1, 0), ('Baixo', 1, 0), ('Esquerda', 0, -1), ('Direita', 0, 1)]

        for action, dr, dc in moves:
            new_row, new_col = row + dr, col + dc

            # Verifica limites do tabuleiro usando a largura dinâmica
            if 0 <= new_row < width and 0 <= new_col < width:
                new_empty_idx = new_row * width + new_col

                new_board = list(self.board)
                new_board[empty_idx], new_board[new_empty_idx] = new_board[new_empty_idx], new_board[empty_idx]

                child_node = Node(tuple(new_board), self, action, self.depth + 1)
                successors.append(child_node)

        return successors

    @staticmethod
    def get_heuristic(node):
        """Calcula a heurística do nó atual face ao estado objetivo."""
        width = int(len(node.board) ** 0.5)

        if Node.heuristic_type == 'misplaced':
            # Conta peças que não são o espaço vazio (0) e não estão na posição correta
            return sum(1 for i in range(len(node.board)) if node.board[i] != 0 and node.board[i] != Node.goal_state[i])

        elif Node.heuristic_type == 'manhattan':
            dist = 0
            for i in range(len(node.board)):
                val = node.board[i]
                if val != 0:
                    target_idx = Node.goal_state.index(val)
                    curr_row, curr_col = divmod(i, width)
                    target_row, target_col = divmod(target_idx, width)
                    dist += abs(curr_row - target_row) + abs(curr_col - target_col)
            return dist
        return 0

    # Os métodos __eq__ e __hash__ são essenciais para que o Python consiga
    # comparar nós e utilizá-los em listas e dicionários no teu A* e BFS
    def __eq__(self, other):
        return isinstance(other, Node) and self.board == other.board

    def __hash__(self):
        return hash(self.board)