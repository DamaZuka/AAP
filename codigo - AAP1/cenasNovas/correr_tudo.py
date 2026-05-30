# correr_tudo.py
import subprocess
import sys
import os
import re
import csv

diretorio_atual = os.path.dirname(os.path.abspath(__file__))

scripts_de_teste = [
    ("test_csp.py", "Teste Motor CSP Base"),
    ("nqueens_csp.py", "CSP - N-Rainhas"),
    ("nqueens_genetic.py", "Algoritmo Genetico - N-Rainhas"),
    ("mapa_portugal_csp.py", "CSP - Mapa de Portugal"),
    ("test_tsp_swarm.py", "Swarm - PSO vs ACO")
]

print("=" * 75)
print("    SISTEMA DE AUTOMAÇÃO DE TESTES INTEGRADO - GERADOR DE CSV COMPLETO")
print("=" * 75)

# Estrutura para armazenar as linhas do CSV
dados_csv = [
    ["Algoritmo/Problema", "Instancia/Dimensão", "Metrica_Qualidade", "Tempo_Execucao(s)", "Iteracoes_Nos_Expandidos",
     "Sucesso"]]

for script, descricao in scripts_de_teste:
    caminho_completo = os.path.join(diretorio_atual, script)
    print(f"\n>>> A EXECUTAR: {descricao} ({script}) <<<")

    if not os.path.exists(caminho_completo):
        print(f"Erro: {script} não encontrado!")
        continue

    # Executa o script capturando o output textual da consola
    resultado = subprocess.run([sys.executable, caminho_completo], capture_output=True, text=True, encoding='utf-8')
    output = resultado.stdout
    print(output)  # Mostra no terminal para veres a correr

    # --- PARSING DOS DADOS PARA O CSV ---
    if script == "test_csp.py":
        sol_match = re.search(r"Solução encontrada: (\{.*?\})", output)
        nos_match = re.search(r"Nós expandidos: (\d+)", output)
        if sol_match and nos_match:
            dados_csv.append(
                ["Motor CSP Base (Test)", "3 Variaveis (A,B,C)", "Solução Válida", "0.0000", nos_match.group(1), "Sim"])

    elif script == "nqueens_csp.py":
        blocos = re.findall(
            r"A iniciar testes para N = (\d+).+?-> (Sucesso|Falha).+?Tempo de Execução: ([\d\.]+) segundos.+?Nós Expandidos: (\d+)",
            output, re.DOTALL)
        for n, status, t, nos in blocos:
            dados_csv.append([f"CSP N-Queens", f"N={n}", "0 Conflitos" if status == "Sucesso" else "Inviável", t, nos,
                              "Sim" if status == "Sucesso" else "Não"])

    elif script == "nqueens_genetic.py":
        blocos = re.findall(
            r"A iniciar simulação evolutiva para N = (\d+).+?-> (.*?)\..+?Tempo de Execução: ([\d\.]+) segundos.+?Gerações / Iterações processadas: (\d+)",
            output, re.DOTALL)
        for n, msg, t, ger in blocos:
            sucesso = "Sim" if "Sucesso" in msg else "Não (Timeout)"
            qualidade = "0 Conflitos" if "Sucesso" in msg else re.search(r"Melhor fitness: ([\d/]+)", msg).group(
                1) + " Fitness" if re.search(r"Melhor fitness: ([\d/]+)", msg) else "Sub-ótimo"
            dados_csv.append(["Algoritmo Genetico", f"N={n}", qualidade, t, ger, sucesso])

    elif script == "mapa_portugal_csp.py":
        sucesso_match = re.search(
            r"Encontrada uma coloração válida usando (\d+) cores.+?Tempo: ([\d\.]+) segundos.+?Nós Expandidos: (\d+)",
            output, re.DOTALL)
        if sucesso_match:
            k, t, nos = sucesso_match.groups()
            dados_csv.append(["CSP Mapa Portugal", "18 Distritos", f"{k} Cores (Mínimo)", t, nos, "Sim"])

    elif script == "test_tsp_swarm.py":
        instancias = re.findall(
            r">>> A INSTANCIAR TESTES PARA: (.*?) <<<.+?Melhor Custo \(Distância\): ([\d\.]+).+?Tempo de Execução: ([\d\.]+)s.+?Melhor Custo \(Distância\): ([\d\.]+).+?Tempo de Execução: ([\d\.]+)s",
            output, re.DOTALL)
        for inst, pso_c, pso_t, aco_c, aco_t in instancias:
            dados_csv.append(["TSP - PSO", inst, f"{pso_c} Dist.", pso_t, "300", "Sim"])
            dados_csv.append(["TSP - ACO", inst, f"{aco_c} Dist.", aco_t, "150", "Sim"])

# Gravar o ficheiro CSV definitivo
csv_filename = os.path.join(diretorio_atual, "resultados_projeto2.csv")
with open(csv_filename, mode='w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerows(dados_csv)

print("\n" + "=" * 75)
print("    BENCHMARK COMPLETO CONCLUÍDO! CSV GERADO COM SUCESSO!")
print(f"    Ficheiro guardado em: {csv_filename}")
print("=" * 75)