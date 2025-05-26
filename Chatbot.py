"""
🌳 Bosquinho - Assistente Especializado em Teoria das Filas M/M/1

Interface principal do sistema usando Streamlit
"""

import streamlit as st
from utils.streamlit_helpers import (
    setup_sidebar,
    initialize_session_state,
    display_chat_messages,
    process_user_input,
    process_image_upload,
    clear_conversation
)

# Configuração da página
st.set_page_config(
    page_title="🌳 Bosquinho - Assistente M/M/1",
    page_icon="🌳",
    layout="wide"
)


def main():
    """Função principal da aplicação"""
    # Configura a sidebar
    setup_sidebar()

    # CSS para interface moderna
    st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        margin-bottom: 2rem;
        color: white;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    .main-title {
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        font-size: 1.2rem;
        opacity: 0.9;
        margin-bottom: 0.5rem;
    }
    .tech-stack {
        font-size: 0.9rem;
        opacity: 0.8;
    }
    .stChatMessage {
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    .upload-section {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
    }
    </style>
    """, unsafe_allow_html=True)

    # Header moderno
    st.markdown("""
    <div class="main-header">
        <div class="main-title">🍖 Milanesa</div>
        <div class="subtitle">🎯 Seu Assistente Especializado em Teoria das Filas M/M/1</div>
        <div class="tech-stack">🧠 Powered by Groq Llama 3.1 8B + 📸 OCR EasyOCR</div>
    </div>
    """, unsafe_allow_html=True)

    # Inicializa o estado da sessão
    initialize_session_state()

    # Exibe mensagens do chat
    display_chat_messages()

    # CSS para estilizar o botão de câmera
    st.markdown("""
    <style>
    .camera-upload {
        position: fixed;
        bottom: 80px;
        right: 20px;
        z-index: 999;
        background: #ff6b6b;
        border-radius: 50%;
        width: 60px;
        height: 60px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        cursor: pointer;
        font-size: 24px;
    }
    </style>
    """, unsafe_allow_html=True)

    # Input de texto principal
    if prompt := st.chat_input("🍖 Pergunte ao Milanesa sobre M/M/1 ou envie uma foto 📸"):
        process_user_input(prompt)

    # Upload de imagem estilizado na sidebar
    with st.sidebar:
        st.markdown("---")
        st.markdown("""
        <div class="upload-section">
            <h4 style="margin-top: 0; color: #667eea;">📸 Upload de Exercício</h4>
            <p style="font-size: 0.9rem; color: #666; margin-bottom: 1rem;">
                Envie uma foto clara do exercício de M/M/1 e o Milanesa resolverá automaticamente!
            </p>
        </div>
        """, unsafe_allow_html=True)

        uploaded_file = st.file_uploader(
            "Escolher arquivo",
            type=['png', 'jpg', 'jpeg'],
            help="📸 Formatos aceitos: PNG, JPG, JPEG",
            label_visibility="collapsed"
        )

        if uploaded_file is not None:
            process_image_upload(uploaded_file)

    # Botão para limpar conversa
    clear_conversation()


if __name__ == "__main__":
    main()
