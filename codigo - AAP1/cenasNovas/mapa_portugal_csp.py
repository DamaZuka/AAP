# portugal_map_csp.py
import time
from csp_engine import CSP, CSPSolver


def obter_adjacencias_portugal():
    """Retorna o dicionário de distritos vizinhos de Portugal Continental."""
    return {
        'Viana do Castelo': ['Braga', 'Vila Real'],
        'Braga': ['Viana do Castelo', 'Vila Real', 'Porto'],
        'Porto': ['Braga', 'Vila Real', 'Viseu', 'Aveiro'],
        'Vila Real': ['Viana do Castelo', 'Braga', 'Porto', 'Viseu', 'Bragança'],
        'Bragança': ['Vila Real', 'Viseu', 'Guarda'],
        'Viseu': ['Porto', 'Vila Real', 'Bragança', 'Guarda', 'Coimbra', 'Aveiro'],
        'Aveiro': ['Porto', 'Viseu', 'Coimbra'],
        'Coimbra': ['Aveiro', 'Viseu', 'Guarda', 'Castelo Branco', 'Leiria'],
        'Guarda': ['Bragança', 'Viseu', 'Coimbra', 'Castelo Branco'],
        'Castelo Branco': ['Guarda', 'Coimbra', 'Leiria', 'Santarém', 'Portalegre'],
        'Leiria': ['Coimbra', 'Castelo Branco', 'Santarém', 'Lisboa'],
        'Santarém': ['Leiria', 'Castelo Branco', 'Portalegre', 'Évora', 'Setúbal', 'Lisboa'],
        'Lisboa': ['Leiria', 'Santarém', 'Setúbal'],
        'Portalegre': ['Castelo Branco', 'Santarém', 'Évora'],
        'Évora': ['Portalegre', 'Santarém', 'Setúbal', 'Beja'],
        'Setúbal': ['Lisboa', 'Santarém', 'Évora', 'Beja'],
        'Beja': ['Setúbal', 'Évora', 'Faro'],
        'Faro': ['Beja']
    }


def criar_restricao_coloracao(adjacencias):
    """Cria a regra: distritos vizinhos não podem ter a mesma cor."""

    def restricao(var_atual, assignment):
        cor_atual = assignment[var_atual]
        vizinhos = adjacencias.get(var_atual, [])

        for vizinho in vizinhos:
            if vizinho in assignment and assignment[vizinho] == cor_atual:
                return False
        return True

    return restricao


def resolver_mapa_portugal(num_cores):
    distritos_adj = obter_adjacencias_portugal()
    variables = list(distritos_adj.keys())

    # Lista de cores disponíveis (K cores)
    lista_cores = [f"Cor_{i + 1}" for i in range(num_cores)]
    domains = {distrito: lista_cores.copy() for distrito in variables}

    # Inicializa CSP
    csp = CSP(variables, domains)
    funcao_restricao = criar_restricao_coloracao(distritos_adj)

    for var in variables:
        csp.add_constraint(var, funcao_restricao)

    solver = CSPSolver(csp)

    start_time = time.time()
    solucao = solver.solve(use_mrv=True, use_lcv=True)
    end_time = time.time()

    return solucao, solver.nodes_expanded, end_time - start_time


if __name__ == "__main__":
    print("=" * 60)
    print("   EXECUTANDO OPÇÃO D: COLORACÃO DO MAPA DE PORTUGAL")
    print("=" * 60)

    # Testar a partir de 3 cores para encontrar o número cromático mínimo
    for k in [3, 4]:
        print(f"\nA tentar colorir com K = {k} cores...")
        sol, nos, tempo = resolver_mapa_portugal(k)

        if sol:
            print(f"-> Sucesso! Encontrada uma coloração válida usando {k} cores.")
            print(f"   Tempo: {tempo:.4f} segundos")
            print(f"   Nós Expandidos: {nos}")
            print("\nDistribuição das cores pelos Distritos:")
            for distrito, cor in sorted(sol.items()):
                print(f"   - {distrito}: {cor}")
            break
        else:
            print(f"-> Falha: Não é possível colorir o mapa continental com apenas {k} cores.")