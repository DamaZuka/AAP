class PuzzleGraph:
    def get_neighbors(self, node):
        return node.get_successors()

    def get_cost(self, node1, node2):
        """
        No puzzle de peças deslizantes, o custo para mover uma peça é sempre constante e igual a 1.
        """
        return 1