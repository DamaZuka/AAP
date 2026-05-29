# genetic_algorithm.py
import random
import time


class NQueensGeneticCompleto:
    def __init__(self, n, pop_size=150, mutation_rate=0.08, max_generations=2000):
        self.n = n
        # Garante população par para a dinâmica de nascimento de gémeos funcionar sem quebrar o limite
        self.pop_size = pop_size if pop_size % 2 == 0 else pop_size + 1
        self.mutation_rate = mutation_rate
        self.max_generations = max_generations
        self.max_fitness = (n * (n - 1)) // 2

    def fitness(self, cromossoma):
        """Calcula a aptidão do indivíduo (pares de rainhas que NÃO se atacam)."""
        ataques = 0
        for i in range(self.n):
            for j in range(i + 1, self.n):
                if cromossoma[i] == cromossoma[j]:
                    ataques += 1
                elif abs(cromossoma[i] - cromossoma[j]) == abs(i - j):
                    ataques += 1
        return self.max_fitness - ataques

    def criar_individuo(self):
        """Gera um cromossoma inicial aleatório (DNA original)."""
        return [random.randint(0, self.n - 1) for _ in range(self.n)]

    def selecao_progenitores(self, populacao, fitnesses):
        """
        A tua Seleção Corrigida: Filtra por indicador de aptidão relativa > 0.3
        e escolhe os pais usando Roleta Proporcional para garantir pressão seletiva.
        """
        pop_com_fit_relativo = []
        for ind, fit in zip(populacao, fitnesses):
            fit_relativo = fit / self.max_fitness
            pop_com_fit_relativo.append((ind, fit, fit_relativo))

        # Filtro biológico estrito (> 0.3)
        pool_reprodutivo = [ind for ind in pop_com_fit_relativo if ind[2] > 0.3]

        # Salvaguarda caso a geração inicial seja muito fraca
        if not pool_reprodutivo:
            pool_reprodutivo = sorted(pop_com_fit_relativo, key=lambda x: x[1], reverse=True)[
                :max(2, self.pop_size // 10)]

        individuos_aprovados = [item[0] for item in pool_reprodutivo]
        fitnesses_aprovados = [item[1] for item in pool_reprodutivo]

        # Seleção por Roleta dentro dos aprovados
        return random.choices(individuos_aprovados, weights=fitnesses_aprovados, k=1)[0]

    def meiose_e_crossing_over(self, p1, p2):
        """
        Meiose celular com recombinação homóloga.
        Alterna aleatoriamente entre Crossing-Over de Ponto Único ou Multi-Ponto.
        """
        if self.n < 6 or random.random() < 0.5:
            # Single-Point Crossover
            ponto = random.randint(1, self.n - 2)
            gameta_A = p1[:ponto] + p2[ponto:]
            gameta_B = p2[:ponto] + p1[ponto:]
        else:
            # Multi-Point Crossover (Dois pontos de corte)
            ponto1 = random.randint(1, self.n // 2)
            ponto2 = random.randint(ponto1 + 1, self.n - 2)

            gameta_A = p1[:ponto1] + p2[ponto1:ponto2] + p1[ponto2:]
            gameta_B = p2[:ponto1] + p1[ponto1:ponto2] + p2[ponto2:]

        return gameta_A, gameta_B

    def mutacao_e_inversao(self, cromossoma):
        """
        Erros de replicação genética:
        Aplica Mutação de Ponto Simples ou Inversão Cromossómica Completa.
        """
        if random.random() < self.mutation_rate:
            if random.random() < 0.6 or self.n < 4:
                # Mutação de Ponto: Altera o alelo de um gene aleatório
                coluna = random.randint(0, self.n - 1)
                cromossoma[coluna] = random.randint(0, self.n - 1)
            else:
                # Inversão Genética: Inverte um bloco inteiro do cromossoma
                ponto1 = random.randint(0, self.n - 3)
                ponto2 = random.randint(ponto1 + 2, self.n - 1)
                segmento = cromossoma[ponto1:ponto2]
                cromossoma = cromossoma[:ponto1] + segmento[::-1] + cromossoma[ponto2:]
        return cromossoma

    def fecundacao_e_desenvolvimento_embriao(self, gameta_pai, gameta_mae):
        """
        Mecânica do Zigoto e Parto:
        Simula o nascimento de indivíduos normais, Gémeos Maternos/Idênticos
        (Monozigóticos) ou Gémeos Fraternos (Dizigóticos).
        """
        # Formação e mutação dos primeiros rascunhos de zigotos
        zigoto_1 = self.mutacao_e_inversao(gameta_pai)
        zigoto_2 = self.mutacao_e_inversao(gameta_mae)

        probabilidade_parto = random.random()

        if probabilidade_parto < 0.10:
            # 10% de hipóteses de Gémeos Maternos / Idênticos (Monozigóticos)
            # O mesmo zigoto fecundado divide-se perfeitamente em dois embriões iguais
            embriao_clonado = list(zigoto_1)
            return [list(zigoto_1), embriao_clonado]

        elif probabilidade_parto < 0.25:
            # Mais 15% de hipóteses (entre 0.10 e 0.25) de Gémeos Fraternos (Dizigóticos)
            # Dois gâmetas diferentes são fecundados ao mesmo tempo
            return [list(zigoto_1), list(zigoto_2)]

        else:
            # 75% de hipóteses de Nascimentos Individuais Normais
            # Retorna os dois de qualquer forma para manter o fluxo de preenchimento par estável
            return [list(zigoto_1), list(zigoto_2)]

    def aplicar_elitismo(self, populacao, fitnesses, n_elites=2):
        """Clonagem artificial das mentes mais brilhantes para a era seguinte."""
        ordenados = [ind for ind, _ in sorted(zip(populacao, fitnesses), key=lambda x: x[1], reverse=True)]
        return ordenados[:n_elites]

    def executar_evolucao(self):
        """Orquestra o ciclo de vida evolucionário completo."""
        populacao = [self.criar_individuo() for _ in range(self.pop_size)]

        start_time = time.time()

        for geracao in range(1, self.max_generations + 1):
            fitnesses = [self.fitness(ind) for ind in populacao]

            # Condição de vitória absoluta (Zero conflitos no tabuleiro)
            if self.max_fitness in fitnesses:
                end_time = time.time()
                idx = fitnesses.index(self.max_fitness)
                return populacao[idx], geracao, end_time - start_time, True

            # Sobrevivência garantida via Elitismo
            nova_geracao = self.aplicar_elitismo(populacao, fitnesses, n_elites=2)

            # Ciclo reprodutivo até atingir a capacidade de carga do ecossistema (pop_size)
            while len(nova_geracao) < self.pop_size:
                pai = self.selecao_progenitores(populacao, fitnesses)
                mae = self.selecao_progenitores(populacao, fitnesses)

                # Execução da meiose e cruzamento cromossómico
                gameta_pai, gameta_mae = self.meiose_e_crossing_over(pai, mae)

                # Fecundação dos gâmetas e análise de gémeos
                nascimentos = self.fecundacao_e_desenvolvimento_embriao(gameta_pai, gameta_mae)

                for individuo in nascimentos:
                    if len(nova_geracao) < self.pop_size:
                        nova_geracao.append(individuo)

            populacao = nova_geracao

        end_time = time.time()
        melhor_idx = fitnesses.index(max(fitnesses))
        return populacao[melhor_idx], self.max_generations, end_time - start_time, False


if __name__ == "__main__":
    tamanhos_n = [8, 16, 32, 64]

    print("=" * 60)
    print("   EXECUTANDO AG COMPLETO: LIMITES COMPUTACIONAIS AMPLIADOS")
    print("=" * 60)

    for n in tamanhos_n:
        print(f"\nA iniciar simulação evolutiva para N = {n}...")

        # Ampliação dos limites máximos de gerações/iterações
        if n <= 16:
            max_g = 6700  # Limite ampliado para dar margem de convergência
        else:
            max_g = 1700  # Limite ampliado para tabuleiros maiores

        # Instancia o teu algoritmo genético com os novos parâmetros
        ag = NQueensGeneticCompleto(n, pop_size=120, max_generations=max_g)
        melhor, geracoes, tempo, sucesso = ag.executar_evolucao()
        fit_final = ag.fitness(melhor)

        if sucesso:
            print(f"-> Sucesso Absoluto! Solução perfeita obtida na geração {geracoes}.")
        else:
            print(
                f"-> Terminado por limite de recursos ({geracoes} ger.). Melhor fitness: {fit_final}/{ag.max_fitness}")

        print(f"   Tempo de Execução: {tempo:.4f} segundos")
        print(f"   Gerações / Iterações processadas: {geracoes}")