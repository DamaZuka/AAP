from node import Node
import heapq
import time


class Algorithms:
    def __init__(self, graph):
        self.found_path = []
        self.visit_order = []
        self.graph = graph
        self.designations = ['Profundidade Primeiro', 'Largura Primeiro', 'Greedy BFS', 'A*']

    def dfs(self, start_node, end_node, max_nodes=50000, timeout=60, start_time=None):
        if start_time is None:
            start_time = time.time()

        # Condições de paragem por limite de recursos
        if time.time() - start_time > timeout or len(self.visit_order) >= max_nodes:
            return self.visit_order, []

        if end_node not in self.found_path and start_node not in self.visit_order:
            self.visit_order.append(start_node)
            self.found_path.append(start_node)
            vizinhos = self.graph.get_neighbors(start_node)
            for v in vizinhos:
                if v == end_node:
                    self.visit_order.append(v)
                    self.found_path.append(v)
                else:
                    self.dfs(v, end_node, max_nodes, timeout, start_time)

            if start_node in self.visit_order and end_node not in self.found_path:
                if self.found_path:
                    self.found_path.pop()

        return self.visit_order, self.found_path

    def bfs(self, start_node, end_node, max_nodes=50000, timeout=60):
        caminho = {}
        caminho[start_node] = None
        espera = [start_node]
        start_time = time.time()

        while espera:
            # Condições de paragem por limite de recursos
            if time.time() - start_time > timeout or len(self.visit_order) >= max_nodes:
                return self.visit_order, []

            g = espera.pop(0)
            if end_node not in self.visit_order:
                self.visit_order.append(g)
                vizinhos = self.graph.get_neighbors(g)
                for v in vizinhos:
                    if v not in caminho:
                        espera.append(v)
                        caminho[v] = g
            else:
                break

        if end_node not in caminho and end_node != start_node:
            return self.visit_order, []

        target = end_node
        while target is not None:
            self.found_path.append(target)
            target = caminho.get(target)

        self.found_path.reverse()
        return self.visit_order, self.found_path

    def greedy_bfs(self, start_node, end_node, max_nodes=50000, timeout=60):
        espera = []
        visitado = [start_node]
        caminho = {start_node: None}
        start_time = time.time()

        while end_node not in visitado:
            # Condições de paragem por limite de recursos
            if time.time() - start_time > timeout or len(visitado) >= max_nodes:
                return self.visit_order, []

            if not espera and len(visitado) > 0 and visitado[-1] != start_node:
                break

            current_node = visitado[-1]
            vizinhos = self.graph.get_neighbors(current_node)

            for v in vizinhos:
                if v not in caminho:
                    espera.append(v)
                    caminho[v] = current_node

            if not espera:
                break

            melhor_vizinho = min(espera, key=lambda node: Node.get_heuristic(node))

            visitado.append(melhor_vizinho)
            espera.remove(melhor_vizinho)
            self.visit_order = visitado

        if end_node not in visitado:
            return self.visit_order, []

        target = end_node
        path = []
        while target is not None:
            path.append(target)
            target = caminho.get(target)

        path.reverse()
        self.found_path = path
        return self.visit_order, self.found_path

    def a_star(self, start_node, end_node, max_nodes=50000, timeout=60):
        self.found_path = []
        self.visit_order = []
        start_time = time.time()

        count = 0
        espera = [(Node.get_heuristic(start_node), count, start_node)]

        caminho = {}
        g_score = {start_node: 0}

        espera_hash = {start_node}
        visitados = set()

        while espera:
            # Condições de paragem por limite de recursos
            if time.time() - start_time > timeout or len(self.visit_order) >= max_nodes:
                return self.visit_order, []

            current_f, _, current_node = heapq.heappop(espera)

            if current_node in visitados:
                continue

            self.visit_order.append(current_node)

            if current_node == end_node:
                target = current_node
                while target in caminho:
                    self.found_path.append(target)
                    target = caminho[target]
                self.found_path.append(start_node)
                self.found_path.reverse()
                return self.visit_order, self.found_path

            visitados.add(current_node)
            if current_node in espera_hash:
                espera_hash.remove(current_node)

            for v in self.graph.get_neighbors(current_node):
                if v in visitados:
                    continue

                tentative_g = g_score[current_node] + self.graph.get_cost(current_node, v)

                if tentative_g < g_score.get(v, float('inf')):
                    caminho[v] = current_node
                    g_score[v] = tentative_g
                    f = tentative_g + Node.get_heuristic(v)

                    count += 1
                    heapq.heappush(espera, (f, count, v))
                    espera_hash.add(v)

        return self.visit_order, self.found_path

    def perform_search(self, search_type, start_node, end_node, max_nodes=50000, timeout=60):
        self.found_path = []
        self.visit_order = []

        if "Profundidade" in search_type:
            return self.dfs(start_node, end_node, max_nodes=max_nodes, timeout=timeout)
        elif "Largura" in search_type:
            return self.bfs(start_node, end_node, max_nodes=max_nodes, timeout=timeout)
        elif "Greedy" in search_type:
            return self.greedy_bfs(start_node, end_node, max_nodes=max_nodes, timeout=timeout)
        elif "A*" in search_type:
            return self.a_star(start_node, end_node, max_nodes=max_nodes, timeout=timeout)
        else:
            raise ValueError(f"Algoritmo '{search_type}' não reconhecido.")