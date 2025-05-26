"""
Agente principal Bosquinho - Especialista em Teoria das Filas M/M/1
VERSÃO UNIVERSAL: A IA resolve QUALQUER problema
"""

from langgraph.graph import StateGraph, END
from models.state import BosquinhoState
from agents.nodes import (
    extract_parameters,
    identify_calculation_type,
    perform_calculation,
    generate_response
)


class BosquinhoAgent:
    """Agente especializado em M/M/1 - IA resolve qualquer problema"""

    def __init__(self):
        self.graph = self._create_graph()

    def _create_graph(self) -> StateGraph:
        """Cria o grafo do assistente Bosquinho"""
        workflow = StateGraph(BosquinhoState)

        # Adiciona os nós
        workflow.add_node("extract_parameters", extract_parameters)
        workflow.add_node("identify_calculation", identify_calculation_type)
        workflow.add_node("perform_calculation", perform_calculation)
        workflow.add_node("generate_response", generate_response)

        # Define o fluxo
        workflow.set_entry_point("extract_parameters")
        workflow.add_edge("extract_parameters", "identify_calculation")
        workflow.add_edge("identify_calculation", "perform_calculation")
        workflow.add_edge("perform_calculation", "generate_response")
        workflow.add_edge("generate_response", END)

        return workflow.compile()

    def process_message(self, messages: list) -> dict:
        """Processa qualquer mensagem usando pipeline inteligente"""
        
        print(f"🔍 DEBUG AGENT - Mensagem: {messages[-1]['content'][:100]}...")
        
        try:
            # Usa o pipeline LangGraph completo
            initial_state = {"messages": messages}
            
            print("🔍 DEBUG AGENT - Executando pipeline universal...")
            result = self.graph.invoke(initial_state)
            
            print(f"✅ DEBUG AGENT - Pipeline concluído. Mensagens: {len(result['messages'])}")
            
            return result

        except Exception as e:
            print(f"❌ ERROR AGENT - Erro no pipeline: {str(e)}")
            # Fallback: chama IA diretamente
            from utils.groq_client import groq_client
            
            try:
                user_question = messages[-1]["content"] if messages else ""
                response = groq_client.solve_any_mm1_problem(user_question, {})
                messages.append({"role": "assistant", "content": response})
                return {"messages": messages}
            except:
                error_response = f"🌳 **Bosquinho aqui!** Desculpe, tive um problema: {str(e)}"
                messages.append({"role": "assistant", "content": error_response})
                return {"messages": messages}

    def get_welcome_message(self) -> str:
        """Retorna a mensagem de boas-vindas"""
        return """🌳 **Olá! Sou o Bosquinho, seu assistente especializado em Teoria das Filas M/M/1!**

🧠 **Posso resolver QUALQUER problema de fila M/M/1:**

📊 **Cálculos que faço:**
- **ρ (rho)**: Utilização do sistema
- **L**: Número médio de clientes no sistema  
- **Lq**: Número médio de clientes na fila
- **W**: Tempo médio no sistema
- **Wq**: Tempo médio na fila
- **P0**: Probabilidade de sistema vazio
- **Pn**: Probabilidade de n clientes
- **P(N>k)**: Probabilidade de mais de k clientes

🎯 **Tipos de problemas que resolvo:**
- 🛫 **Aeroportos** (aviões, pistas de pouso)
- 🏦 **Bancos** (clientes, caixas eletrônicos)
- 🍕 **Restaurantes** (pedidos, cozinha)
- 🏢 **Empresas** (requisições, servidores)
- 🚗 **Drive-thru** (carros, atendimento)
- 📞 **Call centers** (chamadas, operadores)
- **E muito mais!**

💡 **Como usar:**
Apenas descreva seu problema! Posso identificar automaticamente os parâmetros λ (chegada) e μ (atendimento).

**Exemplos:**
- "Em um aeroporto, chega 1 avião a cada 3 minutos e a pista consegue atender 1 por minuto..."
- "Um banco tem clientes chegando a uma taxa de 2 por minuto e cada caixa atende 3 por minuto..."
- "Uma empresa recebe 10 pedidos por hora e consegue processar 15 por hora..."

🚀 **Digite seu problema e eu resolvo completamente!**"""