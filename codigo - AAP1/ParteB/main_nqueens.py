import time
import csv
import os
from nqueens import NQueensState, hill_climbing, simulated_annealing, tabu_search, stochastic_beam_search, \
    stochastic_hill_climbing


def correr_experiencia(algoritmo, nome_algoritmo, n, runs=10, csv_filename="resultados_parte_b.csv"):
    sucessos = 0
    tempos = []
    iteracoes = []
    conflitos = []

    for execucao in range(runs):
        estado_inicial = NQueensState(n)

        start_time = time.time()
        estado_final, iters = algoritmo(estado_inicial)
        end_time = time.time()

        tempo_decorrido = end_time - start_time
        tempos.append(tempo_decorrido)
        iteracoes.append(iters)
        conflitos.append(estado_final.get_conflicts())

        if estado_final.get_conflicts() == 0:
            sucessos += 1

    # Cálculo das métricas finais
    taxa_sucesso = (sucessos / runs) * 100
    tempo_medio = sum(tempos) / runs
    media_iteracoes = sum(iteracoes) / runs
    conflitos_medios = sum(conflitos) / runs

    # Impressão na consola
    print(f"--- {nome_algoritmo} ---")
    print(f"Taxa de sucesso: {taxa_sucesso:.1f}%")
    print(f"Tempo médio: {tempo_medio:.4f}s")
    print(f"Média iterações: {media_iteracoes:.1f}")
    print(f"Qualidade (conflitos médios): {conflitos_medios:.2f}\n")

    # Gravação no ficheiro CSV
    file_exists = os.path.isfile(csv_filename)
    with open(csv_filename, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # Escrever o cabeçalho apenas se o ficheiro for novo
        if not file_exists:
            writer.writerow(
                ["Algoritmo", "Dimensao_N", "Taxa_Sucesso(%)", "Tempo_Medio(s)", "Media_Iteracoes", "Conflitos_Medios"])

        # Escrever a linha com os resultados da experiência
        writer.writerow([
            nome_algoritmo,
            n,
            round(taxa_sucesso, 1),
            round(tempo_medio, 4),
            round(media_iteracoes, 1),
            round(conflitos_medios, 2)
        ])


if __name__ == "__main__":

    valores_n = [8, 20, 50]
    execucoes = 10

    print("=" * 70)
    print(" PARTE 1: EXPERIÊNCIAS PARA VÁRIOS VALORES DE N")
    print("=" * 70)

    for N in valores_n:
        print(f"\n>>> A INICIAR TESTES DE BASE PARA N = {N} <<<")

        # Definição de limites dinâmicos consoante a complexidade
        # Mantido a 1 iteração para N>=50 devido a restrições de tempo de execução
        limite_iters = 3 if N >= 50 else (500 if N >= 20 else 1000)

        # O Simulated Annealing requer atenção redobrada.
        taxa_arrefecimento = 0.85 if N >= 50 else (0.95 if N >= 20 else 0.995)
        temp_inicial = 100 if N >= 50 else 500

        hc_limitado = lambda state: hill_climbing(state, max_iterations=limite_iters)
        correr_experiencia(hc_limitado, f"Hill Climbing Clássico (N={N}, max_iters={limite_iters})", N, runs=execucoes)

        # Inclusão do Stochastic Hill Climbing como bónus para mitigar a explosão combinatória
        if N >= 50:
            hc_estocastico = lambda state: stochastic_hill_climbing(state, max_iterations=200, num_samples=100)
            correr_experiencia(hc_estocastico, f"Stochastic Hill Climbing (N={N}, max_iters=200, samples=100)", N,
                               runs=execucoes)

        sa_limitado = lambda state: simulated_annealing(state, initial_temp=temp_inicial,
                                                        cooling_rate=taxa_arrefecimento)
        correr_experiencia(sa_limitado, f"Simulated Annealing (N={N}, cool_rate={taxa_arrefecimento})", N,
                           runs=execucoes)

        ts_limitado = lambda state: tabu_search(state, tabu_size=10, max_iterations=limite_iters)
        correr_experiencia(ts_limitado, f"Tabu Search (N={N}, max_iters={limite_iters})", N, runs=execucoes)

        # Beam Search com largura reduzida em N=50 para mitigar sobrecarga de memória e tempo
        beam_w = 2 if N >= 50 else 3
        sbs_limitado = lambda state: stochastic_beam_search(state, beam_width=beam_w, max_iterations=limite_iters)
        correr_experiencia(sbs_limitado, f"Stochastic Beam Search (N={N}, beam_w={beam_w})", N, runs=execucoes)

    print("\n" + "=" * 70)
    print(" PARTE 2: ANÁLISE DE IMPACTO DOS PARÂMETROS")
    print("=" * 70)

    N_param = 20

    print("\n>>> IMPACTO DA TEMPERATURA (Simulated Annealing) - N=20 <<<")
    configs_sa = [
        {"temp": 100, "rate": 0.90},
        {"temp": 500, "rate": 0.95},
        {"temp": 1000, "rate": 0.99}
    ]
    for cfg in configs_sa:
        alg_sa = lambda state: simulated_annealing(state, initial_temp=cfg['temp'], cooling_rate=cfg['rate'])
        correr_experiencia(alg_sa, f"SA (Temp={cfg['temp']}, Rate={cfg['rate']})", N_param, runs=execucoes)

    print("\n>>> IMPACTO DO TAMANHO DA LISTA TABU (Tabu Search) - N=20 <<<")
    configs_ts = [5, 10, 20]
    for size in configs_ts:
        alg_ts = lambda state: tabu_search(state, tabu_size=size, max_iterations=500)
        correr_experiencia(alg_ts, f"Tabu Search (Tabu Size={size})", N_param, runs=execucoes)

    print("\n>>> IMPACTO DA LARGURA DO FEIXE (Stochastic Beam Search) - N=20 <<<")
    configs_sbs = [2, 3, 5]
    for width in configs_sbs:
        alg_sbs = lambda state: stochastic_beam_search(state, beam_width=width, max_iterations=500)
        correr_experiencia(alg_sbs, f"Stochastic Beam Search (Beam Width={width})", N_param, runs=execucoes)