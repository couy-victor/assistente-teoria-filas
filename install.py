#!/usr/bin/env python3
"""
Script de instalação do Bosquinho - Assistente M/M/1
"""

import subprocess
import sys
import os

def install_requirements():
    """Instala as dependências necessárias"""
    requirements = [
        "streamlit>=1.28.0",
        "langgraph>=0.0.40", 
        "langchain>=0.1.0",
        "typing-extensions>=4.5.0",
        "groq>=0.4.0",
        "python-dotenv>=1.0.0"
    ]
    
    print("🌳 Instalando dependências do Bosquinho...")
    
    for req in requirements:
        try:
            print(f"📦 Instalando {req}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", req])
            print(f"✅ {req} instalado com sucesso!")
        except subprocess.CalledProcessError as e:
            print(f"❌ Erro ao instalar {req}: {e}")
            return False
    
    return True

def check_env_file():
    """Verifica se o arquivo .env existe"""
    if not os.path.exists(".env"):
        print("❌ Arquivo .env não encontrado!")
        print("💡 Crie o arquivo .env com sua chave do Groq:")
        print("GROQ_API_KEY=sua_chave_aqui")
        return False
    
    print("✅ Arquivo .env encontrado!")
    return True

def main():
    """Função principal"""
    print("🚀 Iniciando instalação do Bosquinho...")
    
    if not install_requirements():
        print("❌ Falha na instalação das dependências")
        return
    
    if not check_env_file():
        print("❌ Configure o arquivo .env antes de continuar")
        return
    
    print("\n🎉 Instalação concluída com sucesso!")
    print("\n🌳 Para executar o Bosquinho:")
    print("streamlit run Chatbot.py")

if __name__ == "__main__":
    main()
