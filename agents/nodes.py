"""
Nós do grafo LangGraph para a assistente Milanesa - VERSÃO COM CONTEXTO MELHORADO
A IA resolve QUALQUER problema de M/M/1 E MANTÉM CONTEXTO
"""

import re
from typing import Dict, Any
from models.state import MilanesaState
from utils.mm1_calculator import MM1Calculator


def is_followup_question(message: str) -> bool:
    """
    Detecta se a mensagem é uma pergunta de follow-up que referencia algo anterior
    """
    message_lower = message.lower().strip()
    
    # Palavras que indicam referência ao contexto anterior
    followup_indicators = [
        'isso', 'isto', 'essa', 'esta', 'esse', 'este',
        'explique melhor', 'detalhe', 'me explique',
        'como assim', 'não entendi', 'pode explicar',
        'exemplifique', 'exemplo', 'mostre',
        'e se', 'mas e', 'porém',
        'anterior', 'problema anterior', 'cálculo anterior',
        'resultado', 'resposta', 'solução',
        'didático', 'didática', 'mais claro',
        'passo a passo', 'detalhado'
    ]
    
    # Verifica se é uma pergunta curta (geralmente follow-ups são mais curtos)
    is_short = len(message.split()) <= 10
    
    # Verifica se contém indicadores de follow-up
    has_followup_words = any(indicator in message_lower for indicator in followup_indicators)
    
    # Verifica se NÃO contém números (novos problemas geralmente têm números)
    has_numbers = bool(re.search(r'\d+', message))
    
    # Verifica se NÃO contém palavras de novo problema
    new_problem_words = ['problema', 'exercício', 'empresa', 'aeroporto', 'banco', 'chegam', 'atende']
    has_new_problem_words = any(word in message_lower for word in new_problem_words)
    
    result = (is_short and has_followup_words) or (has_followup_words and not has_numbers and not has_new_problem_words)
    
    print(f"🔍 DEBUG FOLLOWUP - Mensagem: '{message[:50]}...'")
    print(f"🔍 DEBUG FOLLOWUP - É curta: {is_short}, Tem indicadores: {has_followup_words}, Tem números: {has_numbers}")
    print(f"🔍 DEBUG FOLLOWUP - RESULTADO: {'FOLLOWUP' if result else 'NOVO PROBLEMA'}")
    
    return result


def extract_last_problem_context(state: MilanesaState) -> Dict:
    """
    Extrai o contexto do último problema resolvido das mensagens anteriores
    """
    context = {
        "last_problem": None,
        "last_solution": None,
        "last_parameters": {},
        "conversation_summary": ""
    }
    
    if not state.get("messages") or len(state["messages"]) < 2:
        return context
    
    try:
        # Procura pela última resposta da Milanesa que contém um problema resolvido
        for i in range(len(state["messages"]) - 1, -1, -1):
            msg = state["messages"][i]
            
            if isinstance(msg, dict):
                role = msg.get("role", "")
                content = msg.get("content", "")
            else:
                # Alterna entre user e assistant baseado na posição
                role = "assistant" if i % 2 == 1 else "user"
                content = str(msg.content) if hasattr(msg, 'content') else str(msg)
            
            # Se é resposta da Milanesa e contém cálculos/resultados
            if role == "assistant" and any(keyword in content.lower() for keyword in 
                ['λ', 'mu', 'rho', 'utilização', 'tempo médio', 'número médio', 'probabilidade']):
                
                context["last_solution"] = content
                print(f"✅ DEBUG CONTEXT - Última solução encontrada: {len(content)} chars")
                
                # Procura a pergunta correspondente (mensagem anterior do usuário)
                if i > 0:
                    prev_msg = state["messages"][i-1]
                    if isinstance(prev_msg, dict):
                        context["last_problem"] = prev_msg.get("content", "")
                    else:
                        context["last_problem"] = str(prev_msg.content) if hasattr(prev_msg, 'content') else str(prev_msg)
                    
                    print(f"✅ DEBUG CONTEXT - Último problema encontrado: {context['last_problem'][:100]}...")
                
                # Extrai parâmetros da solução anterior
                lambda_match = re.search(r'λ.*?=.*?(\d+(?:\.\d+)?(?:/\d+)?)', content.lower())
                if lambda_match:
                    context["last_parameters"]["lambda"] = lambda_match.group(1)
                
                mu_match = re.search(r'μ.*?=.*?(\d+(?:\.\d+)?(?:/\d+)?)', content.lower())
                if mu_match:
                    context["last_parameters"]["mu"] = mu_match.group(1)
                
                break
        
        # Constrói resumo da conversa (últimas 3 trocas)
        recent_messages = []
        for i in range(max(0, len(state["messages"]) - 6), len(state["messages"])):
            msg = state["messages"][i]
            if isinstance(msg, dict):
                role = msg.get("role", "user")
                content = msg.get("content", "")
            else:
                role = "assistant" if i % 2 == 1 else "user"
                content = str(msg.content) if hasattr(msg, 'content') else str(msg)
            
            speaker = "USUÁRIO" if role == "user" else "MILANESA"
            recent_messages.append(f"{speaker}: {content[:200]}")
        
        context["conversation_summary"] = "\n\n".join(recent_messages)
        
    except Exception as e:
        print(f"❌ DEBUG CONTEXT - Erro ao extrair contexto: {e}")
    
    return context


def safe_float_conversion(value_str: str, context: str = "unknown") -> float:
    """Converte string para float de forma segura, com logging detalhado"""
    try:
        clean_str = value_str.strip()
        print(f"🔍 DEBUG - Convertendo '{clean_str}' para float (contexto: {context})")
        
        clean_str = re.sub(r'[^\d./]', '', clean_str)
        
        if not clean_str or clean_str in ['.', '/']:
            raise ValueError(f"String vazia após limpeza: '{value_str}' -> '{clean_str}'")
        
        if '/' in clean_str:
            parts = clean_str.split('/')
            if len(parts) == 2 and parts[0] and parts[1]:
                result = float(parts[0]) / float(parts[1])
            else:
                raise ValueError(f"Fração inválida: '{clean_str}'")
        else:
            if not re.match(r'^\d+\.?\d*$', clean_str):
                raise ValueError(f"Formato numérico inválido: '{clean_str}'")
            result = float(clean_str)
        
        print(f"✅ DEBUG - Conversão bem-sucedida: '{value_str}' -> {result}")
        return result
        
    except Exception as e:
        print(f"❌ DEBUG - Erro na conversão float: '{value_str}' (contexto: {context}) -> {e}")
        raise ValueError(f"Erro ao converter '{value_str}' para float: {e}")


def extract_parameters(state: MilanesaState) -> MilanesaState:
    """Extrai parâmetros básicos - AGORA COM DETECÇÃO DE FOLLOW-UP"""
    try:
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
        except Exception as e:
            print(f"⚠️ DEBUG - Erro ao extrair conteúdo: {e}")
            content = ""

        print(f"🔍 DEBUG EXTRACT - Processando: '{content[:50]}...'")

        # 🔧 NOVA FUNCIONALIDADE: Detecta se é follow-up
        if is_followup_question(content):
            state["is_followup"] = True
            state["followup_context"] = extract_last_problem_context(state)
            print("✅ DEBUG EXTRACT - FOLLOW-UP detectado, contexto extraído")
            return state

        # Para mensagens simples (saudações), pula processamento numérico
        simple_messages = ['ola', 'olá', 'oi', 'oii', 'hello', 'hi', 'bom dia', 'boa tarde', 'boa noite']
        if content.lower().strip() in simple_messages:
            print("✅ DEBUG EXTRACT - Mensagem simples detectada, pulando extração numérica")
            return state

        # EXTRAÇÃO GENÉRICA - pega números que possam ser parâmetros
        content_lower = content.lower()

        # Detecta se é um problema/exercício completo
        problem_keywords = [
            'problema', 'exercício', 'questão', 'exemplo', 'calcule', 'determine',
            'encontre', 'resolva', 'qual', 'aeroporto', 'banco', 'fila', 'sistema',
            'empresa', 'loja', 'cliente', 'atendimento', 'servidor', 'padaria'
        ]

        if any(keyword in content_lower for keyword in problem_keywords):
            state["is_complete_problem"] = True

        # Extração de números do texto
        all_numbers = []
        number_pattern = r'\b\d+(?:\.\d+)?(?:/\d+(?:\.\d+)?|:\d+(?:\.\d+)?)?\b'
        matches = re.findall(number_pattern, content)
        
        print(f"🔍 DEBUG EXTRACT - Matches encontrados: {matches}")
        
        for i, match in enumerate(matches):
            try:
                print(f"🔍 DEBUG EXTRACT - Processando match {i}: '{match}'")
                value = safe_float_conversion(match, f"number_extraction_{i}")
                
                if 0 <= value <= 10000:
                    all_numbers.append(value)
                    print(f"✅ DEBUG EXTRACT - Número válido adicionado: {value}")
                else:
                    print(f"⚠️ DEBUG EXTRACT - Número fora do range: {value}")

            except Exception as e:
                print(f"⚠️ DEBUG EXTRACT - Erro na conversão do match '{match}': {e}")
                continue

        # Tenta identificar λ e μ
        lambda_keywords = ['lambda', 'λ', 'chegada', 'arrival', 'entrada']
        mu_keywords = ['mu', 'μ', 'atendimento', 'service', 'saída', 'processamento']

        for keyword in lambda_keywords:
            pattern = rf'{keyword}[^0-9]*?(\d+(?:\.\d+)?(?:/\d+)?)'
            match = re.search(pattern, content_lower)
            if match:
                value_str = match.group(1)
                try:
                    print(f"🔍 DEBUG EXTRACT - Tentando extrair lambda de: '{value_str}'")
                    state["lambda_rate"] = safe_float_conversion(value_str, "lambda_extraction")
                    print(f"✅ DEBUG EXTRACT - Lambda extraído: {state['lambda_rate']}")
                    break
                except Exception as e:
                    print(f"⚠️ DEBUG EXTRACT - Lambda inválido ignorado: '{value_str}' -> {e}")
                    continue

        for keyword in mu_keywords:
            pattern = rf'{keyword}[^0-9]*?(\d+(?:\.\d+)?(?:/\d+)?)'
            match = re.search(pattern, content_lower)
            if match:
                value_str = match.group(1)
                try:
                    print(f"🔍 DEBUG EXTRACT - Tentando extrair mu de: '{value_str}'")
                    state["mu_rate"] = safe_float_conversion(value_str, "mu_extraction")
                    print(f"✅ DEBUG EXTRACT - Mu extraído: {state['mu_rate']}")
                    break
                except Exception as e:
                    print(f"⚠️ DEBUG EXTRACT - Mu inválido ignorado: '{value_str}' -> {e}")
                    continue

        if not state.get("lambda_rate") and not state.get("mu_rate") and all_numbers:
            state["found_numbers"] = all_numbers[:5]
            print(f"✅ DEBUG EXTRACT - Números salvos para IA: {state['found_numbers']}")

        print(f"✅ DEBUG EXTRACT - Estado final: lambda={state.get('lambda_rate')}, mu={state.get('mu_rate')}, numbers={state.get('found_numbers')}")
        
        return state

    except Exception as e:
        print(f"❌ DEBUG EXTRACT - Erro geral na extração: {e}")
        return state


def identify_calculation_type(state: MilanesaState) -> MilanesaState:
    """Identifica tipo de cálculo - AGORA COM CONTEXTO"""
    if not state.get("messages"):
        return state

    # 🔧 NOVA PRIORIDADE 0: Se é follow-up, usa contexto anterior
    if state.get("is_followup"):
        state["calculation_result"] = {"type": "ai_followup_with_context"}
        print("✅ DEBUG IDENTIFY - Tipo: ai_followup_with_context")
        return state

    # PRIORIDADE 1: Se é um problema completo, deixa a IA resolver tudo
    if state.get("is_complete_problem"):
        state["calculation_result"] = {"type": "ai_solve_complete"}
        print("✅ DEBUG IDENTIFY - Tipo: ai_solve_complete")
        return state

    # PRIORIDADE 2: Se tem λ e μ claros, faz cálculos e deixa IA explicar
    if state.get("lambda_rate") is not None and state.get("mu_rate") is not None:
        state["calculation_result"] = {"type": "calculate_and_explain"}
        print(f"✅ DEBUG IDENTIFY - Tipo: calculate_and_explain (λ={state.get('lambda_rate')}, μ={state.get('mu_rate')})")
        return state

    # PRIORIDADE 3: Se tem números mas não sabe o que são, deixa IA descobrir
    if state.get("found_numbers"):
        state["calculation_result"] = {"type": "ai_interpret_numbers"}
        print(f"✅ DEBUG IDENTIFY - Tipo: ai_interpret_numbers (números: {state.get('found_numbers')})")
        return state

    # PRIORIDADE 4: Qualquer outra coisa, IA resolve
    state["calculation_result"] = {"type": "ai_general"}
    print("✅ DEBUG IDENTIFY - Tipo: ai_general")
    return state


def perform_calculation(state: MilanesaState) -> MilanesaState:
    """Executa cálculos quando possível - versão focada"""
    if not state.get("calculation_result"):
        return state

    calc_type = state["calculation_result"].get("type")
    print(f"🔍 DEBUG CALC - Tipo de cálculo: {calc_type}")

    # Para follow-ups, não faz novos cálculos
    if calc_type == "ai_followup_with_context":
        print("✅ DEBUG CALC - Follow-up: pulando cálculos, usando contexto anterior")
        return state

    # ÚNICA situação onde fazemos cálculos: quando temos λ e μ claros
    if calc_type == "calculate_and_explain":
        if state.get("lambda_rate") is not None and state.get("mu_rate") is not None:
            calculator = MM1Calculator()

            try:
                print(f"🔍 DEBUG CALC - Iniciando cálculos com λ={state['lambda_rate']}, μ={state['mu_rate']}")
                
                lambda_val = float(state["lambda_rate"])
                mu_val = float(state["mu_rate"])
                
                if lambda_val < 0 or mu_val <= 0:
                    raise ValueError(f"Parâmetros inválidos: λ={lambda_val}, μ={mu_val}")
                
                if lambda_val >= mu_val:
                    print(f"⚠️ DEBUG CALC - Sistema instável detectado: ρ = {lambda_val/mu_val}")
                
                # Calcula TODAS as métricas principais
                results = {}
                results["rho"] = calculator.calculate_rho(lambda_val, mu_val)
                results["L"] = calculator.calculate_L(lambda_val, mu_val)
                results["Lq"] = calculator.calculate_Lq(lambda_val, mu_val)
                results["W"] = calculator.calculate_W(lambda_val, mu_val)
                results["Wq"] = calculator.calculate_Wq(lambda_val, mu_val)
                results["P0"] = calculator.calculate_P0(lambda_val, mu_val)

                results["lambda"] = lambda_val
                results["mu"] = mu_val

                state["calculation_result"].update(results)
                print(f"✅ DEBUG CALC - Cálculos concluídos com sucesso")

            except Exception as e:
                error_msg = f"Erro no cálculo: {str(e)}"
                print(f"❌ DEBUG CALC - {error_msg}")
                state["error_message"] = error_msg

    else:
        print(f"✅ DEBUG CALC - Tipo {calc_type} será tratado pela IA")

    return state


def generate_response(state: MilanesaState) -> MilanesaState:
    """Gera resposta usando IA - VERSÃO COM CONTEXTO MELHORADO"""
    from utils.groq_client import groq_client

    # Extrai TODA a conversa para manter contexto
    conversation_history = ""
    current_question = ""

    if state.get("messages"):
        try:
            # Constrói histórico completo da conversa
            for i, msg in enumerate(state["messages"]):
                if isinstance(msg, dict):
                    role = msg.get("role", "user")
                    content = msg.get("content", "")
                elif hasattr(msg, 'content'):
                    role = "user" if i % 2 == 0 else "assistant"
                    content = str(msg.content)
                else:
                    role = "user"
                    content = str(msg)

                if role == "user":
                    conversation_history += f"USUÁRIO: {content}\n\n"
                    current_question = content
                else:
                    conversation_history += f"MILANESA: {content}\n\n"

        except Exception as e:
            print(f"⚠️ DEBUG RESPONSE - Erro ao construir histórico: {e}")
            current_question = ""

    print(f"🔍 DEBUG RESPONSE - Preparando resposta...")

    try:
        if groq_client is None:
            raise Exception("GroqClient não inicializado corretamente")

        # Se há erro, trata o erro
        if state.get("error_message"):
            print(f"⚠️ DEBUG RESPONSE - Tratando erro: {state['error_message']}")
            response = groq_client.handle_error_with_context(current_question, state['error_message'])

        # 🔧 NOVA FUNCIONALIDADE: Tratamento especial para follow-ups
        elif state.get("calculation_result", {}).get("type") == "ai_followup_with_context":
            print("✅ DEBUG RESPONSE - Processando FOLLOW-UP com contexto")
            
            followup_context = state.get("followup_context", {})
            
            # Monta contexto rico para follow-up
            context_text = f"""
CONTEXTO DA CONVERSA ANTERIOR:

ÚLTIMO PROBLEMA RESOLVIDO:
{followup_context.get('last_problem', 'Não encontrado')}

ÚLTIMA SOLUÇÃO FORNECIDA:
{followup_context.get('last_solution', 'Não encontrada')}

PARÂMETROS UTILIZADOS:
{followup_context.get('last_parameters', {})}

HISTÓRICO RECENTE:
{followup_context.get('conversation_summary', '')}
"""
            
            response = groq_client.answer_followup_question(current_question, context_text)

        # Se calculamos métricas, passa resultados para IA explicar
        elif state.get("calculation_result") and state["calculation_result"].get("type") == "calculate_and_explain":
            print("✅ DEBUG RESPONSE - IA explicará cálculos realizados")

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

            full_context = f"HISTÓRICO DA CONVERSA:\n{conversation_history}\n\nCÁLCULOS REALIZADOS:\n{context}"
            response = groq_client.solve_with_calculations(current_question, full_context)

        # Para TODOS os outros casos, IA resolve do zero
        else:
            print("✅ DEBUG RESPONSE - IA resolverá problema do zero")

            context = {}
            if state.get("lambda_rate"):
                context["lambda"] = state["lambda_rate"]
            if state.get("mu_rate"):
                context["mu"] = state["mu_rate"]
            if state.get("found_numbers"):
                context["numbers_found"] = state["found_numbers"]
            if state.get("is_complete_problem"):
                context["is_complete_problem"] = True

            context["conversation_history"] = conversation_history
            response = groq_client.solve_any_mm1_problem(current_question, context)

    except Exception as e:
        print(f"❌ DEBUG RESPONSE - Erro: {e}")
        response = f"""🍖 **Milanesa aqui!**

Tive um problema técnico: {str(e)}

💡 **Sugestões:**
1. Verifique se o arquivo .env está configurado corretamente
2. Certifique-se de que GROQ_TEMPERATURE não tem caracteres extras
3. Tente reformular sua pergunta"""

    if "messages" not in state:
        state["messages"] = []
    state["messages"].append({"role": "assistant", "content": response})

    print(f"✅ DEBUG RESPONSE - Resposta gerada: {len(response)} chars")
    return state