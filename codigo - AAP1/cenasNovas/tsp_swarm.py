# tsp_swarm.py
import random
import math
import time


class TSP_PSO:
    def __init__(self, coordenadas, pop_size=50, max_iter=200, alpha=0.7, beta=0.7):
        self.coordenadas = coordenadas
        self.num_cidades = len(coordenadas)
        self.pop_size = pop_size
        self.max_iter = max_iter
        self.alpha = alpha  # Peso cognitivo (pbest)
        self.beta = beta  # Peso social (gbest)
        self.dist_matrix = self._calcular_matriz_distancias()

    def _calcular_matriz_distancias(self):
        matrix = {}
        for i in range(self.num_cidades):
            for j in range(self.num_cidades):
                c1 = self.coordenadas[i]
                c2 = self.coordenadas[j]
                matrix[(i, j)] = math.sqrt((c1[0] - c2[0]) ** 2 + (c1[1] - c2[1]) ** 2)
        return matrix

    def calcular_custo(self, rota):
        custo = 0
        for i in range(self.num_cidades):
            custo += self.dist_matrix[(rota[i], rota[(i + 1) % self.num_cidades])]
        return custo

    def _obter_sequencia_swaps(self, de_rota, para_rota):
        """Calcula os swaps necessários para transformar uma rota noutra (Velocidade)."""
        swaps = []
        temp_rota = list(de_rota)
        for i in range(self.num_cidades):
            if temp_rota[i] != para_rota[i]:
                alvo_idx = temp_rota.index(para_rota[i])
                swaps.append((i, alvo_idx))
                temp_rota[i], temp_rota[alvo_idx] = temp_rota[alvo_idx], temp_rota[i]
        return swaps

    def solve(self):
        start_time = time.time()

        # Inicializar partículas (rotas aleatórias)
        particulas = [random.sample(range(self.num_cidades), self.num_cidades) for _ in range(self.pop_size)]
        pbest = list(particulas)
        pbest_custos = [self.calcular_custo(p) for p in particulas]

        gbest = min(pbest, key=lambda p: self.calcular_custo(p))
        gbest_custo = self.calcular_custo(gbest)

        for _ in range(self.max_iter):
            for i in range(self.pop_size):
                # Calcular sequências de swap (Velocidade)
                swaps_pbest = self._obter_sequencia_swaps(particulas[i], pbest[i])
                swaps_gbest = self._obter_sequencia_swaps(particulas[i], gbest)

                # Filtrar swaps com base nos coeficientes alpha e beta
                movimentos = []
                for s in swaps_pbest:
                    if random.random() < self.alpha:
                        movimentos.append(s)
                for s in swaps_gbest:
                    if random.random() < self.beta:
                        movimentos.append(s)

                # Aplicar velocidade à partícula (Atualizar Posição)
                for idx1, idx2 in movimentos:
                    particulas[i][idx1], particulas[i][idx2] = particulas[i][idx2], particulas[i][idx1]

                # Atualizar Pbest
                custo_atual = self.calcular_custo(particulas[i])
                if custo_atual < pbest_custos[i]:
                    pbest[i] = list(particulas[i])
                    pbest_custos[i] = custo_atual

                    # Atualizar Gbest
                    if custo_atual < gbest_custo:
                        gbest = list(particulas[i])
                        gbest_custo = custo_atual

        return gbest, gbest_custo, time.time() - start_time


class TSP_ACO:
    def __init__(self, coordenadas, num_formigas=30, max_iter=100, alpha=1.0, beta=3.0, evap_rate=0.4, q=100.0):
        self.coordenadas = coordenadas
        self.num_cidades = len(coordenadas)
        self.num_formigas = num_formigas
        self.max_iter = max_iter
        self.alpha = alpha  # Importância da feromona
        self.beta = beta  # Importância da visibilidade (1/distancia)
        self.evap_rate = evap_rate
        self.q = q  # Constante de depósito
        self.dist_matrix = self._calcular_matriz_distancias()
        self.feromonas = {(i, j): 1.0 for i in range(self.num_cidades) for j in range(self.num_cidades)}

    def _calcular_matriz_distancias(self):
        matrix = {}
        for i in range(self.num_cidades):
            for j in range(self.num_cidades):
                c1 = self.coordenadas[i]
                c2 = self.coordenadas[j]
                matrix[(i, j)] = math.sqrt((c1[0] - c2[0]) ** 2 + (c1[1] - c2[1]) ** 2)
        return matrix

    def calcular_custo(self, rota):
        custo = 0
        for i in range(self.num_cidades):
            custo += self.dist_matrix[(rota[i], rota[(i + 1) % self.num_cidades])]
        return custo

    def _escolher_proxima_cidade(self, cidade_atual, visitadas):
        probabilidades = []
        total = 0.0

        for c in range(self.num_cidades):
            if c not in visitadas:
                tau = self.feromonas[(cidade_atual, c)] ** self.alpha
                eta = (1.0 / max(0.0001, self.dist_matrix[(cidade_atual, c)])) ** self.beta
                prob = tau * eta
                probabilidades.append((c, prob))
                total += prob

        if total == 0.0:
            return random.choice([c for c in range(self.num_cidades) if c not in visitadas])

        probabilidades = [(c, p / total) for c, p in probabilidades]

        # Roleta probabilística
        r = random.random()
        acumulado = 0.0
        for c, p in probabilidades:
            acumulado += p
            if r <= acumulado:
                return c
        return probabilidades[-1][0]

    def solve(self):
        start_time = time.time()

        melhor_rota = None
        melhor_custo = float('inf')

        for iteration in range(self.max_iter):
            todas_rotas = []

            for f in range(self.num_formigas):
                cidade_inicial = random.randint(0, self.num_cidades - 1)
                rota = [cidade_inicial]
                visitadas = {cidade_inicial}

                while len(rota) < self.num_cidades:
                    atual = rota[-1]
                    proxima = self._escolher_proxima_cidade(atual, visitadas)
                    rota.append(proxima)
                    visitadas.add(proxima)

                todas_rotas.append(rota)
                custo_rota = self.calcular_custo(rota)

                if custo_rota < melhor_custo:
                    melhor_custo = custo_rota
                    melhor_rota = list(rota)

            # Evaporação de feromonas
            for chave in self.feromonas:
                self.feromonas[chave] *= (1.0 - self.evap_rate)
                if self.feromonas[chave] < 0.01:
                    self.feromonas[chave] = 0.01

            # Depósito de novas feromonas
            for rota in todas_rotas:
                custo = self.calcular_custo(rota)
                deposito = self.q / max(0.0001, custo)
                for i in range(self.num_cidades):
                    origem = rota[i]
                    destino = rota[(i + 1) % self.num_cidades]
                    self.feromonas[(origem, destino)] += deposito
                    self.feromonas[(destino, origem)] += deposito

        return melhor_rota, melhor_custo, time.time() - start_time