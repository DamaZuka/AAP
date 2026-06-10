import matplotlib.pyplot as plt
from tsp_swarm import TSP_PSO, TSP_ACO
from test_tsp_swarm import gerar_instancia_cidades

# Utilizar a instância de maior dimensão para evidenciar diferenças de performance
coordenadas = gerar_instancia_cidades(30, seed=30)

print("A executar as instâncias para o Fine-Tuning do ACO...")
valores_evap = [0.3, 0.4, 0.5, 0.6]
resultados_aco = {}

for evap in valores_evap:
    aco = TSP_ACO(coordenadas, num_formigas=30, max_iter=150, alpha=1.0, beta=4.0, evap_rate=evap)
    # Extração do histórico real do teu algoritmo
    _, _, _, historico = aco.solve()
    resultados_aco[evap] = historico
    print(f"ACO (evap_rate={evap}) processado.")

print("\nA executar as instâncias para o Fine-Tuning do PSO...")
cenarios_pso = {
    "Vizinhança Baixa (α=0.5, β=0.7)": (0.5, 0.7),
    "Centro Otimizado (α=0.6, β=0.8)": (0.6, 0.8),
    "Vizinhança Alta (α=0.7, β=0.9)": (0.7, 0.9)
}
resultados_pso = {}

for nome, (alfa, beta) in cenarios_pso.items():
    pso = TSP_PSO(coordenadas, pop_size=80, max_iter=150, alpha=alfa, beta=beta)
    # Extração do histórico do algoritmo
    _, _, _, historico = pso.solve()
    resultados_pso[nome] = historico
    print(f"PSO ({nome}) processado.")


plt.figure(figsize=(14, 6))

plt.subplot(1, 2, 1)
for evap, hist in resultados_aco.items():
    plt.plot(hist, label=f"evap_rate = {evap}")
plt.title("ACO: Procura do Ponto Ótimo")
plt.xlabel("Iterações")
plt.ylabel("Melhor Custo (Distância)")
plt.grid(True, linestyle="--", alpha=0.5)
plt.legend()

plt.subplot(1, 2, 2)
for nome, hist in resultados_pso.items():
    plt.plot(hist, label=nome)
plt.title("PSO: Refinamento de Pesos")
plt.xlabel("Iterações")
plt.ylabel("Melhor Custo (Distância)")
plt.grid(True, linestyle="--", alpha=0.5)
plt.legend()

plt.tight_layout()
plt.savefig("graficos_fine_tuning.png", dpi=300)
plt.show()

print("\nProcesso concluído. O gráfico 'graficos_fine_tuning.png' foi gerado com sucesso.")