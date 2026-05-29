# nqueens_csp.py
import time
from csp_engine import CSP, CSPSolver


def criar_restricao_nrainhas():
    """
    Cria a função de restrição para o problema das N-Rainhas.
    Nesta modelação, o índice da variável é a coluna e o valor atribuído é a linha.
    Assim, evitam-se conflitos de colunas logo à partida.
    """

    def restricao(var_atual, assignment):
        linha_atual = assignment[var_atual]
        coluna_atual = var_atual

        # Verificar contra todas as outras rainhas já posicionadas
        for outra_coluna, outra_linha in assignment.items():
            if outra_coluna == coluna_atual:
                continue

            # 1. Mesma linha
            if outra_linha == linha_atual:
                return False

            # 2. Mesmas diagonais: se a distância entre linhas for igual à distância entre colunas
            if abs(outra_linha - linha_atual) == abs(outra_coluna - coluna_atual):
                return False

        return True

    return restricao


def resolver_n_rainhas(n, use_mrv=True, use_lcv=True):
    """Configura o CSP para N rainhas e chama o solver."""
    # Variáveis: identificadas pelas colunas (0 até N-1)
    variables = list(range(n))

    # Domínios: linhas possíveis para cada coluna (0 até N-1)
    domains = {col: list(range(n)) for col in variables}

    # Instanciar o CSP
    csp = CSP(variables, domains)

    # Aplicar a função de restrição a todas as variáveis
    funcao_restricao = criar_restricao_nrainhas()
    for var in variables:
        csp.add_constraint(var, funcao_restricao)

    # Resolver e medir o tempo
    solver = CSPSolver(csp)

    start_time = time.time()
    solucao = solver.solve(use_mrv=use_mrv, use_lcv=use_lcv)
    end_time = time.time()

    tempo_execucao = end_time - start_time

    return solucao, solver.nodes_expanded, tempo_execucao


# --- EXECUÇÃO DOS TESTES EXIGIDOS NO ENUNCIADO ---
if __name__ == "__main__":
    # Tamanhos de N obrigatórios no guião do projeto
    tamanhos_n = [8, 16, 32, 64]

    print("=" * 60)
    print("   EXECUTANDO COMPARAÇÃO CSP: N-RAINHAS (Com MRV e LCV)")
    print("=" * 60)

    for n in tamanhos_n:
        print(f"\nA iniciar testes para N = {n}...")
        sol, nos, t = resolver_n_rainhas(n, use_mrv=True, use_lcv=True)

        if sol:
            print(f"-> Sucesso! Solução encontrada para N={n}.")
            print(f"   Tempo de Execução: {t:.4f} segundos")
            print(f"   Nós Expandidos: {nos}")
            if n == 8:
                print(f"   Configuração das Linhas (por Coluna): {list(sol.values())}")
        else:
            print(f"-> Falha: Não foi encontrada solução para N={n} dentro dos limites.")