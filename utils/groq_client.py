"""
Cliente Groq para o sistema Milanesa - VERSÃO COM CONTEXTO MELHORADO
Integração com Llama 3.1 8B Instant para resolução de problemas M/M/1
A IA MANTÉM CONTEXTO entre mensagens!
"""

import os
from typing import Dict, List, Optional
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


class GroqClient:
    """Cliente para interação com Groq API - VERSÃO COM CONTEXTO"""

    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY não encontrada no arquivo .env")

        self.client = Groq(api_key=self.api_key)
        self.model = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
        
        # Tratamento seguro das variáveis numéricas
        try:
            temp_str = os.getenv("GROQ_TEMPERATURE", "0.1")
            temp_clean = ''.join(c for c in temp_str if c.isdigit() or c == '.')
            self.temperature = float(temp_clean) if temp_clean else 0.1
            print(f"✅ DEBUG - Temperature carregada: {self.temperature}")
        except (ValueError, TypeError) as e:
            print(f"⚠️ DEBUG - Erro ao carregar GROQ_TEMPERATURE: {e}, usando 0.1")
            self.temperature = 0.1
        
        try:
            tokens_str = os.getenv("GROQ_MAX_TOKENS", "2000")
            tokens_clean = ''.join(c for c in tokens_str if c.isdigit())
            self.max_tokens = int(tokens_clean) if tokens_clean else 2000
            print(f"✅ DEBUG - Max tokens carregado: {self.max_tokens}")
        except (ValueError, TypeError) as e:
            print(f"⚠️ DEBUG - Erro ao carregar GROQ_MAX_TOKENS: {e}, usando 2000")
            self.max_tokens = 2000

    def answer_followup_question(self, current_question: str, context: str) -> str:
        """
        🔧 NOVA FUNCIONALIDADE: Responde perguntas de follow-up usando contexto anterior
        """
        try:
            system_prompt = """IMPORTANTE: RESPONDA SEMPRE EM PORTUGUÊS BRASILEIRO!

Você é a Milanesa, especialista em Teoria das Filas M/M/1.

SITUAÇÃO ESPECIAL: O usuário fez uma pergunta de FOLLOW-UP referente a um problema já resolvido anteriormente.

INSTRUÇÕES CRÍTICAS:
1. NÃO invente novos dados ou parâmetros
2. USE APENAS as informações do contexto anterior fornecido
3. Se o usuário pede "explique isso melhor", refira-se ao problema/solução anterior
4. Se o usuário menciona "isso", "essa", "resultado", refere-se ao contexto anterior
5. Mantenha os mesmos valores de λ, μ e resultados já calculados
6. Foque em explicar/detalhar/esclarecer o que já foi apresentado

PALAVRAS-CHAVE DE FOLLOW-UP:
- "isso" → refere-se ao problema/resultado anterior
- "explique melhor" → quer mais detalhes da mesma solução
- "como assim" → não entendeu a explicação anterior
- "exemplo" → quer exemplo baseado no problema anterior
- "didático" → quer explicação mais simples do mesmo problema

NUNCA mude os dados do problema original!"""

            user_prompt = f"""
PERGUNTA ATUAL DO USUÁRIO:
{current_question}

CONTEXTO COMPLETO DA CONVERSA ANTERIOR:
{context}

INSTRUÇÕES:
1. Analise o contexto anterior para entender qual problema foi resolvido
2. Identifique a que o usuário está se referindo com "isso" ou termos similares
3. Responda especificamente à pergunta usando APENAS os dados já estabelecidos
4. Se for pedido para explicar melhor, foque na didática, não mude os números
5. Se for pedido exemplo, use o mesmo problema com explicação mais clara

IMPORTANTE: Mantenha consistência total com o problema anterior!"""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=max(0.0, min(2.0, self.temperature)),
                max_tokens=max(100, min(4000, self.max_tokens))
            )

            return response.choices[0].message.content

        except Exception as e:
            print(f"❌ DEBUG - Erro em answer_followup_question: {e}")
            return f"""🍖 **Milanesa aqui!**

Entendo que você quer que eu explique melhor o problema anterior, mas tive um problema técnico.

Com base no contexto:
{context[:500]}...

Você pode reformular sua pergunta de forma mais específica? Por exemplo:
- "Explique melhor como calcular ρ"
- "O que significa L = 3,2 na prática?"
- "Como interpretado o tempo médio?"
"""

    def solve_with_calculations(self, user_question: str, context: str) -> str:
        """IA explica problema quando já temos cálculos realizados"""
        try:
            system_prompt = """IMPORTANTE: RESPONDA SEMPRE EM PORTUGUÊS BRASILEIRO!

Você é a Milanesa, especialista em Teoria das Filas M/M/1.

TAREFA: Você recebeu uma pergunta do usuário e já foram feitos os cálculos principais.
Sua missão é:
1. Interpretar o problema apresentado pelo usuário
2. Explicar os resultados calculados de forma didática
3. Responder especificamente às perguntas feitas
4. Mostrar as fórmulas relevantes
5. Dar interpretação prática dos resultados

MELHORIA DE CONTEXTO:
- Se a pergunta menciona "anterior", "isso", "essa solução", refira-se ao histórico
- Mantenha consistência com dados já estabelecidos na conversa
- Use o histórico para entender melhor o que o usuário quer

ESTRUTURA IDEAL:
🎯 Resumo do problema
📊 Parâmetros identificados
🔢 Cálculos e resultados
💡 Interpretação prática
✅ Respostas específicas

Use emojis, seja didático e sempre em PORTUGUÊS BRASILEIRO!"""

            user_prompt = f"""
PERGUNTA DO USUÁRIO:
{user_question}

CÁLCULOS JÁ REALIZADOS E HISTÓRICO:
{context}

Por favor, analise o problema do usuário e explique de forma completa e didática, usando os cálculos já realizados. Responda especificamente ao que foi perguntado, seja sobre número médio de clientes, tempos, probabilidades, etc.

IMPORTANTE: 
- Se o histórico mostra uma conversa anterior, mantenha consistência
- Relacione os resultados com o contexto real do problema (aeroporto, banco, empresa, etc.)
- Se o usuário pede algo sobre "isso" ou se refere a algo anterior, use o histórico
"""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )

            return response.choices[0].message.content

        except Exception as e:
            print(f"❌ DEBUG - Erro em solve_with_calculations: {e}")
            return f"""🍖 **Milanesa aqui!**

Tive um problema técnico, mas calculei os resultados:

{context}

💡 Use estes valores para interpretar o problema!"""

    def solve_any_mm1_problem(self, user_question: str, context: Dict) -> str:
        """IA resolve QUALQUER problema de M/M/1 do zero - VERSÃO COM CONTEXTO MELHORADO"""
        try:
            system_prompt = """IMPORTANTE: RESPONDA SEMPRE EM PORTUGUÊS BRASILEIRO!

Você é a Milanesa, uma assistente especializada em Teoria das Filas M/M/1.

CAPACIDADES MELHORADAS:
- Interpretar QUALQUER problema de teoria das filas M/M/1
- MANTER CONTEXTO de conversas anteriores
- Identificar quando o usuário se refere a problemas anteriores
- Não inventar dados quando há contexto anterior disponível
- Calcular todas as métricas: ρ, L, Lq, W, Wq, P0, Pn, P(N>k)
- Explicar resultados de forma prática e didática

REGRAS DE CONTEXTO:
1. Se há histórico da conversa, SEMPRE analise primeiro
2. Se o usuário menciona "isso", "anterior", "problema", pode estar se referindo ao histórico
3. Se há dados estabelecidos anteriormente, NÃO invente novos dados
4. Se é uma pergunta sobre problema novo COM números, trate como novo problema
5. Se é uma pergunta vaga SEM números, mas COM histórico, use o histórico

FÓRMULAS M/M/1:
- ρ = λ/μ (utilização do sistema)
- L = ρ/(1-ρ) = λ/(μ-λ) (número médio no sistema)
- Lq = ρ²/(1-ρ) = λ²/[μ(μ-λ)] (número médio na fila)
- W = 1/(μ-λ) (tempo médio no sistema)
- Wq = ρ/(μ-λ) = λ/[μ(μ-λ)] (tempo médio na fila)
- P0 = 1-ρ (probabilidade sistema vazio)
- Pn = (1-ρ)ρⁿ (probabilidade de n clientes)
- P(N>k) = ρᵏ⁺¹ (probabilidade de mais de k clientes)

PROCESSO:
1. PRIMEIRO: Analise o histórico para entender o contexto
2. Determine se é problema novo ou continuação
3. Se novo: identifique λ e μ e calcule
4. Se continuação: use dados estabelecidos
5. Responda às perguntas específicas
6. Dê interpretação prática

SEMPRE em PORTUGUÊS BRASILEIRO! Seja didático, use emojis e explique o contexto real."""

            # Prepara informações do contexto
            context_info = ""
            if context.get("lambda"):
                context_info += f"- Lambda (λ) identificado: {context['lambda']}\n"
            if context.get("mu"):
                context_info += f"- Mu (μ) identificado: {context['mu']}\n"
            if context.get("numbers_found"):
                context_info += f"- Números encontrados no texto: {context['numbers_found']}\n"
            if context.get("is_complete_problem"):
                context_info += "- Detectado como problema completo\n"

            # Inclui histórico da conversa - MELHORADO
            conversation_context = ""
            if context.get("conversation_history"):
                conversation_context = f"\n\nHISTÓRICO COMPLETO DA CONVERSA:\n{context['conversation_history']}"

            user_prompt = f"""
PROBLEMA A RESOLVER:
{user_question}

INFORMAÇÕES COLETADAS:
{context_info if context_info else "Nenhuma informação específica coletada - analise o texto completo."}
{conversation_context}

INSTRUÇÕES APRIMORADAS:
1. PRIMEIRO: Analise TODO o histórico da conversa para entender o contexto completo
2. DETERMINE: É um problema novo ou uma pergunta sobre algo já discutido?
3. Se a pergunta atual se refere a algo mencionado anteriormente ("isso", "explique melhor", "como assim"), use as informações do histórico SEM inventar novos dados
4. Se é um problema completamente novo com novos números, trate como novo problema
5. Identifique os parâmetros λ e μ (seja do texto atual ou do histórico)
6. Calcule as métricas necessárias usando as fórmulas M/M/1
7. Responda especificamente às perguntas feitas
8. Explique de forma didática e prática

IMPORTANTE:
- Se a pergunta atual se refere a algo do histórico, NÃO invente novos dados
- Use sempre as informações já estabelecidas na conversa
- Se o problema mencionar tempos (ex: "a cada 3 minutos"), converta para taxas (ex: λ = 1/3 por minuto)
- Se mencionar capacidades (ex: "pode atender 5 por hora"), isso é μ
- Mantenha consistência total com dados já estabelecidos

Resolva o problema completamente mantendo contexto e consistência!"""

            safe_temperature = max(0.0, min(2.0, self.temperature + 0.1))
            safe_max_tokens = max(100, min(4000, self.max_tokens + 500))

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=safe_temperature,
                max_tokens=safe_max_tokens
            )

            return response.choices[0].message.content

        except Exception as e:
            print(f"❌ DEBUG - Erro em solve_any_mm1_problem: {e}")
            return f"""🍖 **Milanesa aqui!**

Tive um problema técnico ao resolver o problema: {str(e)}

💡 **Dica:** Tente reformular sua pergunta incluindo:
- Taxa de chegada (λ) - quantos chegam por unidade de tempo
- Taxa de atendimento (μ) - quantos são atendidos por unidade de tempo

**Exemplo:** "Em um banco, chegam 2 clientes por minuto e cada caixa atende 3 clientes por minuto. Qual o tempo médio na fila?"
"""

    def general_help_response(self, user_question: str) -> str:
        """Usa Llama 3.1 8B para responder QUALQUER pergunta de forma inteligente"""
        try:
            system_prompt = """IMPORTANTE: RESPONDA SEMPRE EM PORTUGUÊS BRASILEIRO!

Você é o Milanesa, um assistente especializado em Teoria das Filas M/M/1.

REGRAS OBRIGATÓRIAS:
1. SEMPRE responda em português brasileiro
2. Se for SAUDAÇÃO (olá, oi, bom dia), seja caloroso e se apresente
3. Se for pergunta sobre M/M/1, explique didaticamente com exemplos
4. Se mencionarem "exemplo do aeroporto" SEM parâmetros, explique os exemplos disponíveis
5. Se pedirem cálculos COM λ e μ, faça os cálculos passo a passo
6. Se pedirem cálculos SEM λ e μ, peça os parâmetros
7. Sempre seja educativo, use emojis e explique o contexto prático

LEMBRE-SE: PORTUGUÊS BRASILEIRO SEMPRE!"""

            safe_temperature = max(0.0, min(2.0, self.temperature + 0.1))
            safe_max_tokens = max(100, min(4000, self.max_tokens // 2))

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_question}
                ],
                temperature=safe_temperature,
                max_tokens=safe_max_tokens
            )

            return response.choices[0].message.content

        except Exception as e:
            print(f"❌ DEBUG - Erro em general_help_response: {e}")
            return self._generate_fallback_help_response()

    def handle_error_with_context(self, user_question: str, error_context: str) -> str:
        """Usa Llama 3.1 8B para explicar erros de forma didática"""
        try:
            system_prompt = """IMPORTANTE: RESPONDA SEMPRE EM PORTUGUÊS BRASILEIRO!

Você é o Milanesa, especialista em Teoria das Filas M/M/1.
Explique erros de forma didática e ajude o usuário a corrigir o problema.
LEMBRE-SE: SEMPRE EM PORTUGUÊS BRASILEIRO!"""

            user_prompt = f"""
            Pergunta do usuário: {user_question}
            Erro encontrado: {error_context}

            Por favor, explique o erro de forma didática e sugira como corrigir.
            """

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=max(0.0, min(2.0, self.temperature)),
                max_tokens=max(100, min(4000, self.max_tokens // 2))
            )

            return response.choices[0].message.content

        except Exception as e:
            print(f"❌ DEBUG - Erro em handle_error_with_context: {e}")
            return f"❌ **Erro:** {error_context}\n\n💡 **Dica:** Certifique-se de fornecer os valores corretos de λ e μ."

    def _generate_fallback_response(self, calculation_result: Dict) -> str:
        """Resposta de fallback quando Groq não está disponível"""
        if "description" in calculation_result:
            return f"🍖 **Milanesa aqui!** Calculei para você:\n\n📊 **Resultado:** {calculation_result['description']}"
        return "🍖 **Milanesa aqui!** Cálculo realizado com sucesso!"

    def _generate_fallback_example_response(self, example_type: str, results: Dict) -> str:
        """Resposta de fallback para exemplos"""
        return f"🍖 **Milanesa resolveu o exemplo {example_type}!**\n\nResultados calculados com sucesso."

    def _generate_fallback_help_response(self) -> str:
        """Resposta de fallback para ajuda geral"""
        return """🍖 **Milanesa aqui!**

Sou especializada em Teoria das Filas M/M/1. Posso ajudar com:
- Cálculos de utilização (ρ)
- Número médio de clientes (L, Lq)
- Tempos médios (W, Wq)
- Probabilidades (P0, Pn, P(N>k))
- Exemplos práticos (aeroporto, banco, etc.)

Como posso ajudá-lo?"""


# Instância global do cliente Groq
try:
    groq_client = GroqClient()
    print("✅ DEBUG - GroqClient inicializado com sucesso")
except Exception as e:
    print(f"❌ DEBUG - Erro ao inicializar GroqClient: {e}")
    groq_client = None