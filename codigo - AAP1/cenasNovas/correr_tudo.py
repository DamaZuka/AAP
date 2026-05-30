# correr_tudo.py
import sys
import os

# Garante que o Python encontra os módulos no diretório atual
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("=" * 70)
print("   SISTEMA DE AUTOMAÇÃO DE TESTES INTEGRADO - PROJETO 2")
print("=" * 70)

# 1. Executar testes de CSP e Algoritmo Genético para N-Rainhas
try:
    print("\n[1/3] A EXECUTAR COMPARAÇÃO CSP PARA N-RAINHAS...")
    import nqueens_csp
except Exception as e:
    print(f"Erro ao correr nqueens_csp: {e}")

try:
    print("\n[2/3] A EXECUTAR ALGORITMO GENÉTICO PARA N-RAINHAS...")
    import nqueens_genetic
except Exception as e:
    print(f"Erro ao correr nqueens_genetic: {e}")

# 2. Executar teste do Mapa de Portugal
try:
    print("\n[3/3] A EXECUTAR COLORACÃO DO MAPA DE PORTUGAL (CSP)...")
    import mapa_portugal_csp
except Exception as e:
    print(f"Erro ao correr mapa_portugal_csp: {e}")

print("\n" + "=" * 70)
print("   TODOS OS MÓDULOS DE CÓDIGO FORAM EXECUTADOS COM SUCESSO!")
print("=" * 70)