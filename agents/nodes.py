"""
Nós do grafo LangGraph para o assistente Bosquinho - VERSÃO UNIVERSAL
A IA resolve QUALQUER problema de M/M/1
"""

import re
from typing import Dict, Any
from models.state import BosquinhoState
from utils.mm1_calculator import MM1Calculator


def extract_parameters(state: BosquinhoState) -> BosquinhoState:
    """Extrai parâmetros básicos - versão genérica que deixa a IA fazer o trabalho pesado"""
    if not state.get("messages"):
        return state

    last_message = state["messages"][-1]

    # Extrai o conteúdo da mensagem
    try:
        if isinstance(last_message, dict):
            content = last_message.get("content", "")
        elif hasattr(last_message, 'content'):
            content = str(last_message.content)
        else:
            content = str(last_message)
    except Exception:
        content = ""

    # EXTRAÇÃO GENÉRICA - pega números que possam ser parâmetros
    content_lower = content.lower()

    # Padrões mais amplos para capturar qualquer taxa/parâmetro
    number_patterns = [
        r'(\d+(?:\.\d+)?)',  # Números decimais
        r'(\d+/\d+)',        # Frações
        r'(\d+:\d+)',        # Razões
    ]

    # Extrai todos os números encontrados
    all_numbers = []
    for pattern in number_patterns:
        matches = re.findall(pattern, content)
        for match in matches:
            if '/' in match:
                nums = match.split('/')
                value = float(nums[0]) / float(nums[1])
            elif ':' in match:
                nums = match.split(':')
                value = float(nums[0]) / float(nums[1])
            else:
                value = float(match)
            all_numbers.append(value)

    # Tenta identificar λ e μ de forma mais inteligente
    lambda_keywords = ['lambda', 'λ', 'chegada', 'arrival', 'entrada']
    mu_keywords = ['mu', 'μ', 'atendimento', 'service', 'saída', 'processamento']

    # Procura por padrões tipo "λ = 2" ou "taxa de chegada = 3"
    for keyword in lambda_keywords:
        pattern = rf'{keyword}[^0-9]*?(\d+(?:\.\d+)?(?:/\d+)?)'
        match = re.search(pattern, content_lower)
        if match:
            value_str = match.group(1)
            if '/' in value_str:
                nums = value_str.split('/')
                state["lambda_rate"] = float(nums[0]) / float(nums[1])
            else:
                state["lambda_rate"] = float(value_str)
            break

    for keyword in mu_keywords:
        pattern = rf'{keyword}[^0-9]*?(\d+(?:\.\d+)?(?:/\d+)?)'
        match = re.search(pattern, content_lower)
        if match:
            value_str = match.group(1)
            if '/' in value_str:
                nums = value_str.split('/')
                state["mu_rate"] = float(nums[0]) / float(nums[1])
            else:
                state["mu_rate"] = float(value_str)
            break

    # Se não encontrou λ e μ explícitos, mas tem números, guarda para a IA analisar
    if not state.get("lambda_rate") and not state.get("mu_rate") and all_numbers:
        state["found_numbers"] = all_numbers[:5]  # Primeiros 5 números

    # Detecta se é um problema/exercício completo (palavras-chave)
    problem_keywords = [
        'problema', 'exercício', 'questão', 'exemplo', 'calcule', 'determine',
        'encontre', 'resolva', 'qual', 'aeroporto', 'banco', 'fila', 'sistema',
        'empresa', 'loja', 'cliente', 'atendimento', 'servidor'
    ]

    if any(keyword in content_lower for keyword in problem_keywords):
        state["is_complete_problem"] = True

    return state


def identify_calculation_type(state: BosquinhoState) -> BosquinhoState:
    """Identifica tipo de cálculo - versão que prioriza a IA"""
    if not state.get("messages"):
        return state

    # PRIORIDADE 1: Se é um problema completo, deixa a IA resolver tudo
    if state.get("is_complete_problem"):
        state["calculation_result"] = {"type": "ai_solve_complete"}
        return state

    # PRIORIDADE 2: Se tem λ e μ claros, faz cálculos e deixa IA explicar
    if state.get("lambda_rate") is not None and state.get("mu_rate") is not None:
        state["calculation_result"] = {"type": "calculate_and_explain"}
        return state

    # PRIORIDADE 3: Se tem números mas não sabe o que são, deixa IA descobrir
    if state.get("found_numbers"):
        state["calculation_result"] = {"type": "ai_interpret_numbers"}
        return state

    # PRIORIDADE 4: Qualquer outra coisa, IA resolve
    state["calculation_result"] = {"type": "ai_general"}
    return state


def perform_calculation(state: BosquinhoState) -> BosquinhoState:
    """Executa cálculos quando possível - versão focada"""

    if not state.get("calculation_result"):
        return state

    calc_type = state["calculation_result"].get("type")

    # ÚNICA situação onde fazemos cálculos: quando temos λ e μ claros
    if calc_type == "calculate_and_explain":
        if state.get("lambda_rate") is not None and state.get("mu_rate") is not None:
            calculator = MM1Calculator()

            try:
                # Calcula TODAS as métricas principais
                results = {}
                results["rho"] = calculator.calculate_rho(state["lambda_rate"], state["mu_rate"])
                results["L"] = calculator.calculate_L(state["lambda_rate"], state["mu_rate"])
                results["Lq"] = calculator.calculate_Lq(state["lambda_rate"], state["mu_rate"])
                results["W"] = calculator.calculate_W(state["lambda_rate"], state["mu_rate"])
                results["Wq"] = calculator.calculate_Wq(state["lambda_rate"], state["mu_rate"])
                results["P0"] = calculator.calculate_P0(state["lambda_rate"], state["mu_rate"])

                # Adiciona parâmetros
                results["lambda"] = state["lambda_rate"]
                results["mu"] = state["mu_rate"]

                state["calculation_result"].update(results)

            except Exception as e:
                state["error_message"] = f"Erro no cálculo: {str(e)}"

    return state


def generate_response(state: BosquinhoState) -> BosquinhoState:
    """Gera resposta usando IA - versão que delega tudo para o Groq"""
    from utils.groq_client import groq_client

    # Extrai a pergunta do usuário
    user_question = ""
    if state.get("messages"):
        try:
            last_msg = state["messages"][-1]
            if isinstance(last_msg, dict):
                user_question = last_msg.get("content", "")
            elif hasattr(last_msg, 'content'):
                user_question = str(last_msg.content)
            else:
                user_question = str(last_msg)
        except Exception:
            user_question = ""

    print(f"🔍 DEBUG RESPONSE - Preparando resposta...")

    try:
        # Se há erro, trata o erro
        if state.get("error_message"):
            response = groq_client.handle_error_with_context(user_question, state['error_message'])

        # Se calculamos métricas, passa resultados para IA explicar
        elif state.get("calculation_result") and state["calculation_result"].get("type") == "calculate_and_explain":
            print("✅ DEBUG RESPONSE - IA explicará cálculos realizados")

            # Cria contexto detalhado para a IA
            calc_result = state["calculation_result"]
            context = f"""
CÁLCULOS REALIZADOS:

Parâmetros:
- λ (taxa de chegada) = {calc_result.get('lambda')}
- μ (taxa de atendimento) = {calc_result.get('mu')}

Resultados:
- ρ (utilização) = {calc_result.get('rho', {}).get('value', 'Erro')}
- L (clientes no sistema) = {calc_result.get('L', {}).get('value', 'Erro')}
- Lq (clientes na fila) = {calc_result.get('Lq', {}).get('value', 'Erro')}
- W (tempo no sistema) = {calc_result.get('W', {}).get('value', 'Erro')}
- Wq (tempo na fila) = {calc_result.get('Wq', {}).get('value', 'Erro')}
- P0 (probabilidade sistema vazio) = {calc_result.get('P0', {}).get('value', 'Erro')}

Status do sistema: {'Estável' if calc_result.get('rho', {}).get('value', 1) < 1 else 'Instável'}
"""

            response = groq_client.solve_with_calculations(user_question, context)

        # Para TODOS os outros casos, IA resolve do zero
        else:
            print("✅ DEBUG RESPONSE - IA resolverá problema do zero")

            # Prepara contexto com informações coletadas
            context = {}
            if state.get("lambda_rate"):
                context["lambda"] = state["lambda_rate"]
            if state.get("mu_rate"):
                context["mu"] = state["mu_rate"]
            if state.get("found_numbers"):
                context["numbers_found"] = state["found_numbers"]
            if state.get("is_complete_problem"):
                context["is_complete_problem"] = True

            response = groq_client.solve_any_mm1_problem(user_question, context)

    except Exception as e:
        print(f"❌ DEBUG RESPONSE - Erro: {e}")
        response = f"🌳 **Bosquinho aqui!** Tive um problema técnico: {str(e)}"

    # Adiciona resposta às mensagens
    if "messages" not in state:
        state["messages"] = []
    state["messages"].append({"role": "assistant", "content": response})

    print(f"✅ DEBUG RESPONSE - Resposta gerada: {len(response)} chars")
    return state