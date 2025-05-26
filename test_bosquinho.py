#!/usr/bin/env python3
"""
Teste do assistente Bosquinho - M/M/1
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.mm1_calculator import MM1Calculator
from agents.bosquinho_agent import BosquinhoAgent
from agents.nodes import extract_parameters

def test_mm1_calculator():
    """Testa a classe MM1Calculator"""
    print("🧪 Testando MM1Calculator...")

    calculator = MM1Calculator()

    # Teste 1: Utilização do sistema
    print("\n📊 Teste 1: Utilização do sistema (λ=2, μ=3)")
    result = calculator.calculate_rho(2, 3)
    print(f"Resultado: {result}")

    # Teste 2: Número médio no sistema
    print("\n👥 Teste 2: Número médio no sistema (λ=1, μ=2)")
    result = calculator.calculate_L(1, 2)
    print(f"Resultado: {result}")

    # Teste 3: Sistema instável
    print("\n⚠️ Teste 3: Sistema instável (λ=3, μ=2)")
    result = calculator.calculate_L(3, 2)
    print(f"Resultado: {result}")

    # Teste 4: Probabilidade de n clientes
    print("\n🎯 Teste 4: Probabilidade de 2 clientes (λ=1, μ=2)")
    result = calculator.calculate_Pn(1, 2, 2)
    print(f"Resultado: {result}")

    print("\n✅ Testes do MM1Calculator concluídos!")

def test_bosquinho_agent():
    """Testa o agente Bosquinho"""
    print("\n🔄 Testando Agente Bosquinho...")

    # Cria o agente
    agent = BosquinhoAgent()

    # Teste com pergunta sobre utilização
    print("\n📝 Teste: 'Calcule a utilização com λ=2 e μ=3'")

    messages = [
        {"role": "user", "content": "Calcule a utilização com λ=2 e μ=3"}
    ]

    try:
        result = agent.process_message(messages)
        print("✅ Agente executado com sucesso!")
        print(f"Mensagens finais: {len(result['messages'])}")
        if result["messages"]:
            last_msg = result["messages"][-1]
            if hasattr(last_msg, 'content'):
                content = str(last_msg.content)[:100]
            else:
                content = last_msg.get('content', 'Sem conteúdo')[:100]
            print(f"Última resposta: {content}...")
    except Exception as e:
        print(f"❌ Erro no agente: {e}")

    print("\n✅ Teste do Agente Bosquinho concluído!")


def test_examples():
    """Testa os exemplos do aeroporto"""
    print("\n✈️ Testando Exemplos do Aeroporto...")

    agent = BosquinhoAgent()

    # Teste exemplo do aeroporto 1
    print("\n📝 Teste: 'Resolva o exemplo do aeroporto 1'")

    messages = [
        {"role": "user", "content": "Resolva o exemplo do aeroporto 1"}
    ]

    try:
        result = agent.process_message(messages)
        print("✅ Exemplo do aeroporto 1 resolvido!")
        if result["messages"]:
            last_msg = result["messages"][-1]
            if hasattr(last_msg, 'content'):
                content = str(last_msg.content)[:200]
            else:
                content = last_msg.get('content', 'Sem conteúdo')[:200]
            print(f"Resposta: {content}...")
    except Exception as e:
        print(f"❌ Erro no exemplo: {e}")

    print("\n✅ Teste de exemplos concluído!")

def test_parameter_extraction():
    """Testa a extração de parâmetros"""
    print("\n🔍 Testando extração de parâmetros...")

    test_cases = [
        "Calcule ρ com λ=2 e μ=3",
        "Taxa de utilização com lambda=1.5 e mu=2.5",
        "Probabilidade de 3 clientes com chegada=1 e atendimento=2",
        "P(N>2) com λ=0.8 e μ=1.2"
    ]

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 Teste {i}: '{test_case}'")

        state = {
            "messages": [{"role": "user", "content": test_case}],
            "lambda_rate": None,
            "mu_rate": None,
            "n_value": None,
            "k_value": None,
            "calculation_result": None,
            "error_message": None
        }
        result_state = extract_parameters(state)

        print(f"λ extraído: {result_state.get('lambda_rate')}")
        print(f"μ extraído: {result_state.get('mu_rate')}")
        print(f"n extraído: {result_state.get('n_value')}")
        print(f"k extraído: {result_state.get('k_value')}")

    print("\n✅ Testes de extração concluídos!")

def main():
    """Executa todos os testes"""
    print("🌳 Iniciando testes do Bosquinho - Assistente M/M/1")
    print("=" * 50)

    try:
        test_mm1_calculator()
        test_parameter_extraction()
        test_bosquinho_agent()
        test_examples()

        print("\n" + "=" * 50)
        print("🎉 Todos os testes concluídos com sucesso!")
        print("\n💡 Para executar a interface, use: streamlit run Chatbot.py")

    except Exception as e:
        print(f"\n❌ Erro durante os testes: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
