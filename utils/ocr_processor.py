"""
Processador OCR para extrair texto de imagens de exercícios
Integrado com o sistema Bosquinho M/M/1
"""

import streamlit as st
import numpy as np
import re
from PIL import Image
from typing import Optional, Tuple


class OCRProcessor:
    """Processador OCR para exercícios de Teoria das Filas"""

    def __init__(self):
        self.reader = None
        self._initialize_ocr()

    def _initialize_ocr(self):
        """Inicializa o EasyOCR com cache para performance"""
        try:
            import easyocr
            import warnings
            import os

            # Suprime warnings do torch e outros
            warnings.filterwarnings("ignore", category=UserWarning)
            os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

            if self.reader is None:
                with st.spinner("🔍 Inicializando OCR (primeira vez pode demorar)..."):
                    self.reader = easyocr.Reader(['pt', 'en'], gpu=False, verbose=False)
                st.success("✅ OCR inicializado com sucesso!")
        except ImportError:
            st.error("❌ EasyOCR não instalado. Execute: pip install easyocr")
            self.reader = None
        except Exception as e:
            st.error(f"❌ Erro ao inicializar OCR: {e}")
            self.reader = None

    def extract_text_from_image(self, image: Image.Image) -> str:
        """Extrai texto da imagem usando EasyOCR"""
        if self.reader is None:
            return "Erro: OCR não inicializado"

        try:
            # Converte PIL Image para numpy array
            img_array = np.array(image)

            # Extrai texto com EasyOCR
            with st.spinner("🔍 Extraindo texto da imagem..."):
                results = self.reader.readtext(img_array)

            # Combina todos os textos detectados
            extracted_text = ""
            for (bbox, text, confidence) in results:
                if confidence > 0.3:  # Filtra textos com baixa confiança
                    extracted_text += text + " "

            return extracted_text.strip()

        except Exception as e:
            st.error(f"❌ Erro na extração de texto: {e}")
            return ""

    def clean_and_format_text(self, raw_text: str) -> str:
        """Limpa e formata o texto extraído para melhor processamento"""
        if not raw_text:
            return ""

        # Remove caracteres especiais e normaliza espaços
        text = re.sub(r'\s+', ' ', raw_text)
        text = text.strip()

        # Correções comuns de OCR
        corrections = {
            'À': 'λ',  # Lambda mal reconhecido
            'µ': 'μ',  # Mu
            'p': 'ρ',  # Rho (quando apropriado)
            '|': 'l',  # Pipe como L
            '0': 'O',  # Zero como O (quando apropriado)
            '1/': '1/',  # Frações
        }

        for wrong, correct in corrections.items():
            text = text.replace(wrong, correct)

        # Melhora formatação de números e frações
        text = re.sub(r'(\d)\s*[/]\s*(\d)', r'\1/\2', text)  # 1 / 3 → 1/3
        text = re.sub(r'λ\s*=\s*', 'λ=', text)  # λ = → λ=
        text = re.sub(r'μ\s*=\s*', 'μ=', text)  # μ = → μ=

        return text

    def process_exercise_image(self, image: Image.Image) -> Tuple[str, str]:
        """
        Processa uma imagem de exercício completa
        Retorna: (texto_extraído, texto_limpo)
        """
        # Extrai texto bruto
        raw_text = self.extract_text_from_image(image)

        # Limpa e formata
        clean_text = self.clean_and_format_text(raw_text)

        return raw_text, clean_text

    def enhance_image_quality(self, image: Image.Image) -> Image.Image:
        """Melhora a qualidade da imagem para melhor OCR"""
        try:
            import cv2

            # Converte para numpy
            img_array = np.array(image)

            # Converte para escala de cinza se colorida
            if len(img_array.shape) == 3:
                gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            else:
                gray = img_array

            # Aplica filtros para melhorar OCR
            # Denoising
            denoised = cv2.fastNlMeansDenoising(gray)

            # Aumenta contraste
            enhanced = cv2.convertScaleAbs(denoised, alpha=1.2, beta=10)

            # Converte de volta para PIL
            return Image.fromarray(enhanced)

        except ImportError:
            st.warning("⚠️ OpenCV não disponível. Usando imagem original.")
            return image
        except Exception as e:
            st.warning(f"⚠️ Erro no processamento da imagem: {e}")
            return image

    def validate_mm1_content(self, text: str) -> bool:
        """Verifica se o texto contém conteúdo relacionado a M/M/1"""
        mm1_keywords = [
            'fila', 'queue', 'teoria das filas', 'queueing',
            'lambda', 'λ', 'mu', 'μ', 'rho', 'ρ',
            'chegada', 'atendimento', 'servidor', 'cliente',
            'aeroporto', 'banco', 'avião', 'aviões',
            'probabilidade', 'tempo médio', 'número médio',
            'utilização', 'sistema', 'poisson'
        ]

        text_lower = text.lower()
        return any(keyword in text_lower for keyword in mm1_keywords)


# Instância global do processador OCR
@st.cache_resource
def get_ocr_processor():
    """Retorna instância cached do processador OCR"""
    return OCRProcessor()
