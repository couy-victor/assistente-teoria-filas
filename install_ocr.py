#!/usr/bin/env python3
"""
Script para instalar dependências OCR do Bosquinho
"""

import subprocess
import sys

def install_ocr_dependencies():
    """Instala as dependências OCR"""
    dependencies = [
        "easyocr>=1.7.0",
        "pillow>=10.0.0", 
        "opencv-python>=4.8.0"
    ]
    
    print("📸 Instalando dependências OCR para o Bosquinho...")
    
    for dep in dependencies:
        try:
            print(f"📦 Instalando {dep}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
            print(f"✅ {dep} instalado com sucesso!")
        except subprocess.CalledProcessError as e:
            print(f"❌ Erro ao instalar {dep}: {e}")
            return False
    
    return True

def main():
    """Função principal"""
    print("🚀 Instalando OCR para o Bosquinho...")
    
    if install_ocr_dependencies():
        print("\n🎉 OCR instalado com sucesso!")
        print("\n📸 Agora você pode:")
        print("- Enviar fotos de exercícios")
        print("- Fazer upload de prints de PDF")
        print("- O Bosquinho lerá e resolverá automaticamente!")
        print("\n🌳 Execute: streamlit run Chatbot.py")
    else:
        print("\n❌ Falha na instalação do OCR")

if __name__ == "__main__":
    main()
