import random
import time


class NQueensGeneticCompleto:
    def __init__(self, n, pop_size=150, mutation_rate=0.15, max_generations=2000):
        self.n = n
        # Garante população par para a dinâmica de nascimento de gémeos funcionar sem quebrar o limite
        self.pop_size = pop_size if pop_size % 2 == 0 else pop_size + 1
        self.mutation_rate = mutation_rate
        self.max_generations = max_generations
        # O máximo de fitness teórico continua a ser o número de pares de rainhas
        self.max_fitness = (n * (n - 1)) // 2

    def fitness(self, cromossoma):
        """Calcula a aptidão. Como usamos permutações, apenas contamos ataques nas diagonais!"""
        ataques = 0
        for i in range(self.n):
            for j in range(i + 1, self.n):
                # Ataque na diagonal: se a diferença das linhas for igual à diferença das colunas
                if abs(cromossoma[i] - cromossoma[j]) == abs(i - j):
                    ataques += 1
        return self.max_fitness - ataques

    def criar_individuo(self):
        """Gera um cromossoma baseado numa permutação (0 ataques em linhas/colunas de base)."""
        individuo = list(range(self.n))
        random.shuffle(individuo)
        return individuo

    def selecao_progenitores(self, populacao, fitnesses):
        """
        Seleção por Roleta Proporcional pura sobre toda a população,
        garantindo pressão seletiva sem extinguir a diversidade precocemente.
        """
        # Salvaguarda para o caso de todos terem fitness zero (muito raro, mas possível em N gigantes)
        if sum(fitnesses) == 0:
            return random.choice(populacao)
        return random.choices(populacao, weights=fitnesses, k=1)[0]

    def meiose_e_crossing_over(self, p1, p2):
        """
        Meiose com cruzamento por mapeamento parcial simplificado
        para tentar preservar a propriedade de permutação nos filhos.
        """
        if self.n < 4:
            return list(p1), list(p2)

        ponto = random.randint(1, self.n - 2)

        # Filho A ganha a primeira parte do Pai 1
        filho_A = p1[:ponto]
        # Preenche o resto com os genes do Pai 2 que ainda não estão lá, mantendo a permutação
        filho_A += [gene for gene in p2 if gene not in filho_A]

        # Filho B ganha a primeira parte do Pai 2
        filho_B = p2[:ponto]
        # Preenche o resto com os genes do Pai 1
        filho_B += [gene for gene in p1 if gene not in filho_B]

        return filho_A, filho_B

    def mutacao_e_inversao(self, cromossoma):
        """
        Erros de replicação genética adaptados para permutações:
        Aplica Mutação por Swap (Troca) ou Inversão de um segmento.
        """
        if random.random() < self.mutation_rate:
            if random.random() < 0.7 or self.n < 4:
                # Mutação por Swap: troca a posição de duas rainhas (mantém a permutação válida)
                i, j = random.sample(range(self.n), 2)
                cromossoma[i], cromossoma[j] = cromossoma[j], cromossoma[i]
            else:
                # Inversão Genética de um bloco (também preserva os valores únicos)
                ponto1 = random.randint(0, self.n - 3)
                ponto2 = random.randint(ponto1 + 2, self.n - 1)
                segmento = cromossoma[ponto1:ponto2]
                cromossoma = cromossoma[:ponto1] + segmento[::-1] + cromossoma[ponto2:]
        return cromossoma

    def fecundacao_e_desenvolvimento_embriao(self, gameta_pai, gameta_mae):
        """
        Mecânica do Zigoto e Parto (Mantida a tua assinatura biológica!).
        """
        zigoto_1 = self.mutacao_e_inversao(list(gameta_pai))
        zigoto_2 = self.mutacao_e_inversao(list(gameta_mae))

        probabilidade_parto = random.random()

        if probabilidade_parto < 0.05:
            # 5% de hipóteses de Gémeos Idênticos (Clonagem de um zigoto estável)
            return [list(zigoto_1), list(zigoto_1)]
        elif probabilidade_parto < 0.20:
            # 15% de hipóteses de Gémeos Fraternos
            return [list(zigoto_1), list(zigoto_2)]
        else:
            # 80% Nascimentos normais
            return [list(zigoto_1), list(zigoto_2)]

    def aplicar_elitismo(self, populacao, fitnesses, n_elites=4):
        """Preserva os melhores cromossomas para a geração seguinte."""
        ordenados = [ind for ind, _ in sorted(zip(populacao, fitnesses), key=lambda x: x[1], reverse=True)]
        return [list(el) for el in ordenados[:n_elites]]

    def executar_evolucao(self):
        """Orquestra o ciclo de vida evolucionário completo."""
        populacao = [self.criar_individuo() for _ in range(self.pop_size)]
        start_time = time.time()

        for geracao in range(1, self.max_generations + 1):
            fitnesses = [self.fitness(ind) for ind in populacao]

            # Condição de vitória absoluta (Zero conflitos nas diagonais)
            if self.max_fitness in fitnesses:
                end_time = time.time()
                idx = fitnesses.index(self.max_fitness)
                return populacao[idx], geracao, end_time - start_time, True

            # Elitismo: os 4 melhores passam sempre
            nova_geracao = self.aplicar_elitismo(populacao, fitnesses, n_elites=4)

            # Repovoamento
            while len(nova_geracao) < self.pop_size:
                pai = self.selecao_progenitores(populacao, fitnesses)
                mae = self.selecao_progenitores(populacao, fitnesses)

                gameta_pai, gameta_mae = self.meiose_e_crossing_over(pai, mae)
                nascimentos = self.fecundacao_e_desenvolvimento_embriao(gameta_pai, gameta_mae)

                for individuo in nascimentos:
                    if len(nova_geracao) < self.pop_size:
                        nova_geracao.append(individuo)

            populacao = nova_geracao

        end_time = time.time()
        fitnesses = [self.fitness(ind) for ind in populacao]
        melhor_idx = fitnesses.index(max(fitnesses))
        return populacao[melhor_idx], self.max_generations, end_time - start_time, False


if __name__ == "__main__":
    tamanhos_n = [8, 16, 32, 64]
    num_execucoes = 10  # Número de runs independentes para validade estatística

    print("=" * 60)
    print("   EXECUTANDO AG OPTIMIZADO POR PERMUTAÇÃO (10 RUNS/N)")
    print("=" * 60)

    for n in tamanhos_n:
        print(f"\nA iniciar simulação evolutiva para N = {n}...")

        # Definição de limites de gerações equilibrados
        if n <= 16:
            max_g = 2000
        else:
            max_g = 3000

        sucessos = 0
        tempos = []
        geracoes_lista = []
        melhor_fitness_global = 0
        max_fit_teorico = (n * (n - 1)) // 2

        # Correr o algoritmo múltiplas vezes
        for i in range(num_execucoes):
            ag = NQueensGeneticCompleto(n, pop_size=160, mutation_rate=0.2, max_generations=max_g)
            melhor, geracoes, tempo, sucesso = ag.executar_evolucao()
            fit_final = ag.fitness(melhor)

            if sucesso:
                sucessos += 1

            if fit_final > melhor_fitness_global:
                melhor_fitness_global = fit_final

            tempos.append(tempo)
            geracoes_lista.append(geracoes)

        # Calcular as métricas médias
        taxa_sucesso = (sucessos / num_execucoes) * 100
        tempo_medio = sum(tempos) / num_execucoes
        geracoes_medias = sum(geracoes_lista) / num_execucoes

        # Imprimir resultados compatíveis com o extrator do CSV
        if taxa_sucesso > 0:
            print(f"-> Sucesso com {taxa_sucesso:.1f}% de taxa de convergencia.")
        else:
            print(
                f"-> Terminado por limite ({taxa_sucesso:.1f}% sucesso). Melhor fitness global: {melhor_fitness_global}/{max_fit_teorico}")

        print(f"   Tempo de Execução: {tempo_medio:.4f} segundos")
        print(f"   Gerações / Iterações processadas: {geracoes_medias:.1f}")