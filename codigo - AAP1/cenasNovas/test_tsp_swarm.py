# test_swarm_tsp.py
import random
from tsp_swarm import TSP_PSO, TSP_ACO


def gerar_instancia_cidades(num_cidades, seed=42):
    """Gera coordenadas X, Y aleatórias para simular os ficheiros de instâncias."""
    random.seed(seed)
    return [(random.uniform(0.0, 100.0), random.uniform(0.0, 100.0)) for _ in range(num_cidades)]


if __name__ == "__main__":
    # Testar com três tamanhos de instâncias diferentes conforme o guião
    instancias = {
        "Pequena (10 Cidades)": gerar_instancia_cidades(10, seed=10),
        "Média (20 Cidades)": gerar_instancia_cidades(20, seed=20),
        "Grande (30 Cidades)": gerar_instancia_cidades(30, seed=30)
    }

    print("=" * 65)
    print("   EXECUTANDO COMPARAÇÃO SWARM: PSO vs ACO NO TSP")
    print("=" * 65)

    for nome, coordenadas in instancias.items():
        print(f"\n>>> A INSTANCIAR TESTES PARA: {nome} <<<")

        # 1. Executar PSO
        pso = TSP_PSO(coordenadas, pop_size=80, max_iter=300, alpha=0.6, beta=0.8)
        pso_rota, pso_custo, pso_tempo = pso.solve()

        print(f"--- Particle Swarm Optimization (PSO) ---")
        print(f"    Melhor Custo (Distância): {pso_custo:.4f}")
        print(f"    Tempo de Execução: {pso_tempo:.4f}s")

        # 2. Executar ACO
        aco = TSP_ACO(coordenadas, num_formigas=30, max_iter=150, alpha=1.0, beta=4.0, evap_rate=0.3)
        aco_rota, aco_custo, aco_tempo = aco.solve()

        print(f"--- Ant Colony Optimization (ACO) ---")
        print(f"    Melhor Custo (Distância): {aco_custo:.4f}")
        print(f"    Tempo de Execução: {aco_tempo:.4f}s")