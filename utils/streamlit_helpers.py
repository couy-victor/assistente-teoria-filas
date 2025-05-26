"""
Utilitários para a interface Streamlit
"""

import streamlit as st


def clean_qwen_response(content: str) -> str:
    """Remove as tags <think> do Qwen QwQ - VERSÃO STREAMLIT COM LOGS"""
    print(f"🔍 DEBUG - Conteúdo original (primeiros 200 chars): {content[:200] if content else 'VAZIO'}")

    if not content:
        print("❌ DEBUG - Conteúdo vazio!")
        return "🌳 **Bosquinho aqui!** Como posso ajudá-lo?"

    original_length = len(content)

    # MÉTODO SIMPLES: se tem <think>, pega só o que vem DEPOIS de </think>
    if '<think>' in content:
        print("🔍 DEBUG - Encontrou tags <think>")
        if '</think>' in content:
            # Pega tudo depois da última tag </think>
            parts = content.split('</think>')
            content = parts[-1] if len(parts) > 1 else content
            print(f"🔍 DEBUG - Após remoção de <think>: {content[:100]}...")
        else:
            # Se tem <think> mas não tem </think>, remove tudo a partir de <think>
            content = content.split('<think>')[0]
            print(f"🔍 DEBUG - Removeu <think> sem fechamento: {content[:100]}...")
    else:
        print("✅ DEBUG - Não tem tags <think>")

    # Limpa espaços
    content = content.strip()

    print(f"🔍 DEBUG - Tamanho: {original_length} -> {len(content)}")

    # Se ficou vazio, retorna resposta padrão
    if not content:
        print("❌ DEBUG - Conteúdo ficou vazio após limpeza!")
        return "🌳 **Bosquinho aqui!** Como posso ajudá-lo com Teoria das Filas M/M/1?"

    print(f"✅ DEBUG - Conteúdo final: {content[:100]}...")
    return content


def setup_sidebar():
    """Configura a sidebar com informações e exemplos"""
    with st.sidebar:

        st.markdown("### 📚 Fórmulas M/M/1")

        with st.expander("📊 Métricas Principais"):
            st.latex(r"\rho = \frac{\lambda}{\mu}")
            st.latex(r"L = \frac{\rho}{1-\rho}")
            st.latex(r"L_q = \frac{\rho^2}{1-\rho}")
            st.latex(r"W = \frac{1}{\mu-\lambda}")
            st.latex(r"W_q = \frac{\rho}{\mu-\lambda}")

        with st.expander("🎯 Probabilidades"):
            st.latex(r"P_0 = 1-\rho")
            st.latex(r"P_n = (1-\rho)\rho^n")
            st.latex(r"P(N>k) = \rho^{k+1}")

        st.markdown("---")
        st.markdown("### 💡 Exemplos Reais")

        # Exemplos de aeroporto
        with st.expander("🛩️ Aeroporto - Sistema de Pouso"):
            st.markdown("""
            **Exemplo 1:** λ=1/3, μ=1 (aviões/min)
            - "Taxa de utilização da pista com λ=0.33 e μ=1"
            - "Probabilidade de não mais que 3 aviões com λ=0.33 e μ=1"

            **Exemplo 2:** λ=1, μ=3 (aviões/min)
            - "Utilização do sistema com λ=1 e μ=3"
            - "Probabilidade de 1 avião com λ=1 e μ=3"
            """)

        with st.expander("🏦 Outros Exemplos"):
            st.markdown("""
            **Banco:** λ=2, μ=3 (clientes/min)
            **Drive-thru:** λ=1.5, μ=2 (carros/min)
            **Geral:** λ=2, μ=3 (qualquer unidade)
            """)

        return None  # Não retorna mais a chave, pois está no .env


def display_welcome_message():
    """Exibe a mensagem de boas-vindas"""
    return """🍖 **Olá! Sou a Milanesa, sua assistente especializada em Teoria das Filas M/M/1!**

Posso ajudá-lo a calcular:

📊 **Métricas principais:**
- **ρ (rho)**: Utilização do sistema (λ/μ)
- **L**: Número médio de clientes no sistema
- **Lq**: Número médio de clientes na fila
- **W**: Tempo médio no sistema
- **Wq**: Tempo médio na fila

🎯 **Probabilidades:**
- **P0**: Probabilidade de sistema vazio
- **Pn**: Probabilidade de n clientes no sistema
- **P(N>k)**: Probabilidade de mais de k clientes

✈️ **Exemplos prontos que posso resolver:**
- "Resolva o exemplo do aeroporto 1"
- "Exemplo do aeroporto 2"
- "Exemplo do banco"
- "Exemplo do drive-thru"

💡 **Ou calcule diretamente:**
"Calcule a utilização do sistema com λ=2 e μ=3"
"""


def initialize_session_state():
    """Inicializa o estado da sessão Streamlit"""
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": display_welcome_message()
            }
        ]

    if "milanesa_agent" not in st.session_state:
        from agents.bosquinho_agent import BosquinhoAgent
        st.session_state.milanesa_agent = BosquinhoAgent()


def display_chat_messages():
    """Exibe as mensagens do chat"""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            # Se a mensagem tem imagem, mostra ela primeiro
            if "image" in message:
                st.image(message["image"], caption="📸 Exercício enviado", use_column_width=True)

            st.markdown(message["content"])

    # Processa resposta de imagem se necessário
    if hasattr(st.session_state, 'process_image_response') and st.session_state.process_image_response:
        st.session_state.process_image_response = False

        with st.chat_message("assistant"):
            with st.spinner("🍖 Milanesa está analisando a imagem..."):
                try:
                    result = st.session_state.milanesa_agent.process_message(
                        st.session_state.messages.copy()
                    )

                    if result.get("messages") and len(result["messages"]) > len(st.session_state.messages):
                        assistant_message = result["messages"][-1]

                        if hasattr(assistant_message, 'content'):
                            content = str(assistant_message.content)
                        else:
                            content = assistant_message.get("content", "")

                        message_dict = {"role": "assistant", "content": content}
                        st.session_state.messages.append(message_dict)
                        st.markdown(content)
                        st.rerun()

                except Exception as e:
                    error_msg = f"❌ Erro ao processar imagem: {str(e)}"
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
                    st.markdown(error_msg)
                    st.rerun()


def process_user_input(prompt: str):
    """Processa a entrada do usuário"""
    # Adiciona mensagem do usuário
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    # Processa com o agente Bosquinho
    with st.chat_message("assistant"):
        with st.spinner("🍖 Milanesa está calculando..."):
            try:
                # Executa o agente
                result = st.session_state.milanesa_agent.process_message(
                    st.session_state.messages.copy()
                )

                # Obtém a última mensagem (resposta do assistente)
                if result.get("messages") and len(result["messages"]) > len(st.session_state.messages):
                    assistant_message = result["messages"][-1]

                    # Converte para dict se necessário
                    if hasattr(assistant_message, 'content'):
                        # É um objeto AIMessage
                        content = str(assistant_message.content)
                    else:
                        # Já é um dict
                        content = assistant_message.get("content", "")

                    message_dict = {
                        "role": "assistant",
                        "content": content
                    }

                    st.session_state.messages.append(message_dict)
                    st.markdown(content)
                else:
                    # Fallback se algo der errado
                    fallback_msg = "Desculpe, houve um problema. Tente novamente com uma pergunta mais específica."
                    st.session_state.messages.append({"role": "assistant", "content": fallback_msg})
                    st.markdown(fallback_msg)

            except Exception as e:
                error_msg = f"❌ Erro: {str(e)}\n\nTente reformular sua pergunta."
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
                st.markdown(error_msg)


def process_image_upload(uploaded_file):
    """Processa upload de imagem e extrai texto"""
    try:
        from PIL import Image
        from utils.ocr_processor import get_ocr_processor

        # Verifica se já processou esta imagem (evita loop)
        if hasattr(st.session_state, 'last_processed_image') and st.session_state.last_processed_image == uploaded_file.name:
            return

        # Marca como processada
        st.session_state.last_processed_image = uploaded_file.name

        # Carrega a imagem
        image = Image.open(uploaded_file)

        # Processa com OCR
        ocr_processor = get_ocr_processor()

        if ocr_processor.reader is None:
            st.error("❌ OCR não disponível. Instale: pip install easyocr")
            return

        # Extrai texto
        raw_text, clean_text = ocr_processor.process_exercise_image(image)

        # Valida se é conteúdo M/M/1
        if not ocr_processor.validate_mm1_content(clean_text):
            st.warning("⚠️ Não detectei conteúdo de Teoria das Filas. Verifique se a imagem está clara.")

        # Processa como pergunta normal se extraiu texto
        if clean_text.strip():
            # Cria prompt com imagem e texto
            prompt = f"📸 **Exercício da imagem:**\n\n{clean_text}"

            # Adiciona mensagem do usuário com imagem no chat central
            st.session_state.messages.append({
                "role": "user",
                "content": prompt,
                "image": image  # Adiciona a imagem para mostrar no chat
            })

            # Marca que precisa processar a resposta
            st.session_state.process_image_response = True

            # Força atualização da interface para mostrar no chat central
            st.rerun()

        else:
            st.error("❌ Não consegui extrair texto da imagem. Tente uma imagem mais clara.")

    except Exception as e:
        st.error(f"❌ Erro ao processar imagem: {str(e)}")


def clear_conversation():
    """Limpa a conversa mantendo apenas a mensagem de boas-vindas"""
    if st.button("🗑️ Limpar Conversa"):
        st.session_state.messages = [st.session_state.messages[0]]
        st.rerun()
