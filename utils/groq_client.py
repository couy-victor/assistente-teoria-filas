"""
Cliente Groq para o sistema Bosquinho
Integração com Llama 3.1 8B Instant para resolução de problemas M/M/1
VERSÃO UNIVERSAL: IA resolve QUALQUER problema de M/M/1
"""

import os
from typing import Dict, List, Optional
from groq import Groq
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()


class GroqClient:
    """Cliente para interação com Groq API usando Llama 3.1 8B Instant"""

    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY não encontrada no arquivo .env")

        self.client = Groq(api_key=self.api_key)
        self.model = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
        self.temperature = float(os.getenv("GROQ_TEMPERATURE", "0.1"))
        self.max_tokens = int(os.getenv("GROQ_MAX_TOKENS", "2000"))

    def enhance_calculation_explanation(self, calculation_result: Dict, user_question: str) -> str:
        """
        Usa Llama 3.1 8B para gerar explicações matemáticas detalhadas
        """
        try:
            # Prepara o contexto para o modelo matemático
            system_prompt = """IMPORTANTE: RESPONDA SEMPRE EM PORTUGUÊS BRASILEIRO!

Você é o Bosquinho, um assistente especializado em Teoria das Filas M/M/1.
Você deve explicar cálculos matemáticos de forma clara e didática, sempre mostrando:
1. O contexto do problema
2. As fórmulas utilizadas
3. A substituição dos valores
4. O resultado final
5. A interpretação prática do resultado

Use emojis e formatação markdown para tornar a explicação mais amigável.
LEMBRE-SE: SEMPRE EM PORTUGUÊS BRASILEIRO!"""

            user_prompt = f"""
            Pergunta do usuário: {user_question}

            Resultado do cálculo: {calculation_result}

            Por favor, explique este resultado de forma didática e completa, incluindo:
            - O que significa o resultado
            - Como foi calculado
            - Qual a interpretação prática
            - Se o sistema é estável ou não (quando aplicável)
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
            return self._generate_fallback_response(calculation_result)

    def solve_example_with_explanation(self, example_type: str, results: Dict) -> str:
        """
        Usa Llama 3.1 8B para explicar exemplos completos
        """
        try:
            system_prompt = """IMPORTANTE: RESPONDA SEMPRE EM PORTUGUÊS BRASILEIRO!

Você é o Bosquinho, especialista em Teoria das Filas M/M/1.
Explique exemplos práticos de forma didática, mostrando cada passo do cálculo
e a interpretação real do resultado.
LEMBRE-SE: SEMPRE EM PORTUGUÊS BRASILEIRO!"""

            if example_type == "airport_1":
                context = """
                EXEMPLO DO AEROPORTO 1:
                - Cenário: Aeroporto com pista única para pouso
                - Taxa de chegada: λ = 1/3 aviões por minuto (1 avião a cada 3 minutos)
                - Taxa de atendimento: μ = 1 avião por minuto
                """
            elif example_type == "airport_2":
                context = """
                EXEMPLO DO AEROPORTO 2:
                - Cenário: Aeroporto com pista de alta capacidade
                - Taxa de chegada: λ = 1 avião por minuto
                - Taxa de atendimento: μ = 3 aviões por minuto
                """
            else:
                context = f"Exemplo {example_type} com os seguintes resultados:"

            user_prompt = f"""
            {context}

            Resultados calculados: {results}

            Por favor, explique este exemplo completo de forma didática, incluindo:
            1. Descrição do cenário real
            2. Cada métrica calculada com sua fórmula
            3. Interpretação prática de cada resultado
            4. Conclusões sobre o desempenho do sistema
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
            return self._generate_fallback_example_response(example_type, results)

    def solve_problem_with_context(self, user_question: str, context: str) -> str:
        """
        Resolve um problema específico com contexto detalhado dos cálculos
        Específico para problemas completos como o do aeroporto
        """
        try:
            system_prompt = """IMPORTANTE: RESPONDA SEMPRE EM PORTUGUÊS BRASILEIRO!

Você é o Bosquinho, um assistente especializado em Teoria das Filas M/M/1.

TAREFA ESPECÍFICA:
- Você recebeu um problema completo com TODOS os cálculos já realizados
- Precisa explicar a solução de forma didática e completa
- Foque na interpretação prática dos resultados
- Explique cada métrica de forma clara
- Relacione com o contexto real do problema (aeroporto, aviões, etc.)

ESTRUTURA DA RESPOSTA:
1. 🎯 Resumo do problema
2. 📊 Parâmetros identificados
3. 🔢 Resultados principais
4. 💡 Interpretação prática
5. ✅ Respostas específicas às perguntas

LEMBRE-SE: SEMPRE EM PORTUGUÊS BRASILEIRO!"""

            user_prompt = f"""
PROBLEMA APRESENTADO PELO USUÁRIO:
{user_question}

CONTEXTO COMPLETO COM CÁLCULOS REALIZADOS:
{context}

Por favor, explique este problema de forma didática e completa, respondendo especificamente às perguntas do usuário. Use os resultados calculados para dar respostas precisas e educativas.

IMPORTANTE:
- Explique a diferença entre "aviões no sistema" (L) vs "aviões aguardando na fila" (Lq)
- Mostre as fórmulas quando relevante
- Interpretar os resultados no contexto prático
- Responda especificamente às letras a), b), c) se houver
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
            # Fallback específico para problemas com contexto
            return f"""🌳 **Bosquinho aqui!**

Tive um problema técnico, mas posso te ajudar com base no que calculei:

{context}

💡 **Interpretação básica:**
- O problema envolve uma fila M/M/1 (aeroporto com pista única)
- Lq = número médio de aviões **aguardando** para pousar
- L = número médio de aviões **no sistema** (aguardando + pousando)

Você pode tentar novamente ou reformular sua pergunta!"""

    def solve_with_calculations(self, user_question: str, context: str) -> str:
        """
        IA explica problema quando já temos cálculos realizados
        """
        try:
            system_prompt = """IMPORTANTE: RESPONDA SEMPRE EM PORTUGUÊS BRASILEIRO!

Você é o Bosquinho, especialista em Teoria das Filas M/M/1.

TAREFA: Você recebeu uma pergunta do usuário e já foram feitos os cálculos principais.
Sua missão é:
1. Interpretar o problema apresentado pelo usuário
2. Explicar os resultados calculados de forma didática
3. Responder especificamente às perguntas feitas
4. Mostrar as fórmulas relevantes
5. Dar interpretação prática dos resultados

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

CÁLCULOS JÁ REALIZADOS:
{context}

Por favor, analise o problema do usuário e explique de forma completa e didática, usando os cálculos já realizados. Responda especificamente ao que foi perguntado, seja sobre número médio de clientes, tempos, probabilidades, etc.

IMPORTANTE: Relacione os resultados com o contexto real do problema (aeroporto, banco, empresa, etc.) se aplicável.
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
            return f"""🌳 **Bosquinho aqui!**

Tive um problema técnico, mas calculei os resultados:

{context}

💡 Use estes valores para interpretar o problema!"""

    def solve_any_mm1_problem(self, user_question: str, context: Dict) -> str:
        """
        IA resolve QUALQUER problema de M/M/1 do zero - MÉTODO PRINCIPAL
        """
        try:
            system_prompt = """IMPORTANTE: RESPONDA SEMPRE EM PORTUGUÊS BRASILEIRO!

Você é o Bosquinho, um assistente especializado em Teoria das Filas M/M/1.

CAPACIDADES:
- Interpretar QUALQUER problema de teoria das filas M/M/1
- Identificar parâmetros λ (taxa de chegada) e μ (taxa de atendimento) no texto
- Calcular todas as métricas: ρ, L, Lq, W, Wq, P0, Pn, P(N>k)
- Explicar resultados de forma prática e didática
- Resolver problemas completos com múltiplas perguntas

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
1. Leia e compreenda o problema
2. Identifique λ e μ (taxas, intervalos, frequências)
3. Calcule as métricas necessárias
4. Responda às perguntas específicas
5. Dê interpretação prática

TIPOS DE PROBLEMAS:
- Aeroportos (aviões, pistas)
- Bancos (clientes, caixas)
- Empresas (pedidos, atendimento)
- Restaurantes (clientes, garçons)
- Sistemas de TI (requisições, servidores)
- Qualquer fila de espera!

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

            user_prompt = f"""
PROBLEMA A RESOLVER:
{user_question}

INFORMAÇÕES COLETADAS:
{context_info if context_info else "Nenhuma informação específica coletada - analise o texto completo."}

INSTRUÇÕES:
1. Analise cuidadosamente o problema apresentado
2. Identifique os parâmetros λ e μ (mesmo que implícitos)
3. Calcule as métricas necessárias usando as fórmulas M/M/1
4. Responda especificamente às perguntas feitas
5. Explique de forma didática e prática

IMPORTANTE: Se o problema mencionar tempos (ex: "a cada 3 minutos"), converta para taxas (ex: λ = 1/3 por minuto). Se mencionar capacidades (ex: "pode atender 5 por hora"), isso é μ.

Resolva o problema completamente!"""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=self.temperature + 0.1,  # Pouco mais criativo para resolução
                max_tokens=self.max_tokens + 500      # Mais tokens para problemas complexos
            )

            return response.choices[0].message.content

        except Exception as e:
            return f"""🌳 **Bosquinho aqui!**

Tive um problema técnico ao resolver o problema: {str(e)}

💡 **Dica:** Tente reformular sua pergunta incluindo:
- Taxa de chegada (λ) - quantos chegam por unidade de tempo
- Taxa de atendimento (μ) - quantos são atendidos por unidade de tempo

**Exemplo:** "Em um banco, chegam 2 clientes por minuto e cada caixa atende 3 clientes por minuto. Qual o tempo médio na fila?"
"""

    def general_help_response(self, user_question: str) -> str:
        """
        Usa Llama 3.1 8B para responder QUALQUER pergunta de forma inteligente
        """
        try:
            system_prompt = """IMPORTANTE: RESPONDA SEMPRE EM PORTUGUÊS BRASILEIRO!

Você é o Bosquinho, um assistente especializado em Teoria das Filas M/M/1.

REGRAS OBRIGATÓRIAS:
1. SEMPRE responda em português brasileiro
2. Se for SAUDAÇÃO (olá, oi, bom dia), seja caloroso e se apresente
3. Se for pergunta sobre M/M/1, explique didaticamente com exemplos
4. Se mencionarem "exemplo do aeroporto" SEM parâmetros, explique os exemplos disponíveis
5. Se pedirem cálculos COM λ e μ, faça os cálculos passo a passo
6. Se pedirem cálculos SEM λ e μ, peça os parâmetros
7. Sempre seja educativo, use emojis e explique o contexto prático

LEMBRE-SE: PORTUGUÊS BRASILEIRO SEMPRE!

EXEMPLOS DISPONÍVEIS:
- Aeroporto 1: λ=1/3, μ=1 (pista única)
- Aeroporto 2: λ=1, μ=3 (alta capacidade)
- Banco: λ=2, μ=3 (caixa eletrônico)
- Drive-thru: λ=1.5, μ=2 (restaurante)

FÓRMULAS M/M/1:
- ρ = λ/μ (utilização)
- L = ρ/(1-ρ) (clientes no sistema)
- Lq = ρ²/(1-ρ) (clientes na fila)
- W = 1/(μ-λ) (tempo no sistema)
- Wq = ρ/(μ-λ) (tempo na fila)
- P0 = 1-ρ (sistema vazio)
- Pn = (1-ρ)ρⁿ (n clientes)
- P(N>k) = ρᵏ⁺¹ (mais de k clientes)"""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_question}
                ],
                temperature=self.temperature + 0.1,  # Ligeiramente mais criativo para ajuda geral
                max_tokens=self.max_tokens // 2  # Menos tokens para respostas gerais
            )

            return response.choices[0].message.content

        except Exception as e:
            return self._generate_fallback_help_response()

    def handle_error_with_context(self, user_question: str, error_context: str) -> str:
        """
        Usa Llama 3.1 8B para explicar erros de forma didática
        """
        try:
            system_prompt = """IMPORTANTE: RESPONDA SEMPRE EM PORTUGUÊS BRASILEIRO!

Você é o Bosquinho, especialista em Teoria das Filas M/M/1.
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
                temperature=self.temperature,
                max_tokens=self.max_tokens // 2
            )

            return response.choices[0].message.content

        except Exception as e:
            return f"❌ **Erro:** {error_context}\n\n💡 **Dica:** Certifique-se de fornecer os valores corretos de λ e μ."



    def _generate_fallback_response(self, calculation_result: Dict) -> str:
        """Resposta de fallback quando Groq não está disponível"""
        if "description" in calculation_result:
            return f"🌳 **Bosquinho aqui!** Calculei para você:\n\n📊 **Resultado:** {calculation_result['description']}"
        return "🌳 **Bosquinho aqui!** Cálculo realizado com sucesso!"

    def _generate_fallback_example_response(self, example_type: str, results: Dict) -> str:
        """Resposta de fallback para exemplos"""
        return f"🌳 **Bosquinho resolveu o exemplo {example_type}!**\n\nResultados calculados com sucesso."

    def _generate_fallback_help_response(self) -> str:
        """Resposta de fallback para ajuda geral"""
        return """🌳 **Bosquinho aqui!**

Sou especializado em Teoria das Filas M/M/1. Posso ajudar com:
- Cálculos de utilização (ρ)
- Número médio de clientes (L, Lq)
- Tempos médios (W, Wq)
- Probabilidades (P0, Pn, P(N>k))
- Exemplos práticos (aeroporto, banco, etc.)

Como posso ajudá-lo?"""


# Instância global do cliente Groq
groq_client = GroqClient()