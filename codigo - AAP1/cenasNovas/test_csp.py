# test_csp.py
from csp_engine import CSP, CSPSolver

# 1. Definir Variáveis e Domínios (Cores: Vermelho, Verde, Azul)
variaveis = ['A', 'B', 'C']
dominios = {
    'A': ['Vermelho', 'Verde'],
    'B': ['Vermelho', 'Verde', 'Azul'],
    'C': ['Verde', 'Azul']
}

# 2. Instanciar o CSP
meu_csp = CSP(variaveis, dominios)

# 3. Definir as Restrições (Vizinhos não podem ter a mesma cor)
def restricao_adjacencia(var, assignment):
    # Se os vizinhos estiverem atribuídos, as cores têm de ser diferentes
    if 'A' in assignment and 'B' in assignment and assignment['A'] == assignment['B']:
        return False
    if 'B' in assignment and 'C' in assignment and assignment['B'] == assignment['C']:
        return False
    return True

# Aplicar a restrição às variáveis
meu_csp.add_constraint('A', restricao_adjacencia)
meu_csp.add_constraint('B', restricao_adjacencia)
meu_csp.add_constraint('C', restricao_adjacencia)

# 4. Resolver
solver = CSPSolver(meu_csp)
solucao = solver.solve(use_mrv=True, use_lcv=True)

print("Estado do teste do Motor CSP:")
print(f"Solução encontrada: {solucao}")
print(f"Nós expandidos: {solver.nodes_expanded}")