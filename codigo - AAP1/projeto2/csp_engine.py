# csp_engine.py

class CSP:
    def __init__(self, variables, domains):
        self.variables = variables
        self.domains = {var: list(dom) for var, dom in domains.items()}
        self.constraints = {var: [] for var in variables}

    def add_constraint(self, variable, constraint_function):
        self.constraints[variable].append(constraint_function)

    def is_consistent(self, variable, assignment):
        for constraint in self.constraints[variable]:
            if not constraint(variable, assignment):
                return False
        return True


class CSPSolver:
    def __init__(self, csp):
        self.csp = csp
        self.nodes_expanded = 0

    def solve(self, use_mrv=True, use_lcv=True):
        self.nodes_expanded = 0
        return self._backtracking({}, use_mrv, use_lcv)

    def _get_unassigned_variable(self, assignment, use_mrv):
        unassigned = [v for v in self.csp.variables if v not in assignment]
        if not use_mrv:
            return unassigned[0]
        return min(unassigned, key=lambda var: len(self.csp.domains[var]))

    def _order_domain_values(self, variable, assignment, use_lcv):
        if not use_lcv:
            return self.csp.domains[variable]

        def count_conflicts(value):
            conflicts = 0
            test_assignment = assignment.copy()
            test_assignment[variable] = value
            for neighbor in self.csp.variables:
                if neighbor not in test_assignment:
                    for n_value in self.csp.domains[neighbor]:
                        test_assignment[neighbor] = n_value
                        if not self.csp.is_consistent(neighbor, test_assignment):
                            conflicts += 1
                        del test_assignment[neighbor]
            return conflicts

        return sorted(self.csp.domains[variable], key=count_conflicts)

    def _forward_checking(self, variable, value, assignment):
        """
        Remove os valores inconsistentes dos domínios das variáveis vizinhas.
        Retorna os domínios alterados para podermos restaurar se houver backtrack.
        """
        removidos = {}
        for vizinho in self.csp.variables:
            if vizinho not in assignment:
                removidos[vizinho] = []
                valores_historicos = list(self.csp.domains[vizinho])
                for v_vizinho in valores_historicos:
                    # Testa consistência temporária
                    test_assignment = assignment.copy()
                    test_assignment[vizinho] = v_vizinho
                    if not self.csp.is_consistent(vizinho, test_assignment):
                        self.csp.domains[vizinho].remove(v_vizinho)
                        removidos[vizinho].append(v_vizinho)

                # Se o domínio de um vizinho ficou vazio, esta ramificação aborta já!
                if not self.csp.domains[vizinho]:
                    return None
        return removidos

    def _backtracking(self, assignment, use_mrv, use_lcv):
        if len(assignment) == len(self.csp.variables):
            return assignment

        self.nodes_expanded += 1
        var = self._get_unassigned_variable(assignment, use_mrv)

        for value in self._order_domain_values(var, assignment, use_lcv):
            if self.csp.is_consistent(var, {**assignment, var: value}):
                assignment[var] = value

                # Guarda os domínios atuais antes de podar
                dominios_antigos = {v: list(d) for v, d in self.csp.domains.items()}

                # Executa a filtragem antecipada (Forward Checking)
                inferencia = self._forward_checking(var, value, assignment)

                if inferencia is not None:
                    result = self._backtracking(assignment, use_mrv, use_lcv)
                    if result is not None:
                        return result

                # Se falhou, restaura os domínios antigos (Backtrack)
                self.csp.domains = dominios_antigos
                del assignment[var]

        return None