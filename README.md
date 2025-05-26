# 🍖 Milanesa - Assistente Especializada em M/M/1

**Milanesa** é uma assistente de IA especializada em **Teoria das Filas M/M/1**, desenvolvida com **LangGraph** e **Streamlit**. Ela utiliza **Groq Llama 3.1 8B Instant** + **OCR EasyOCR** para calcular todas as métricas importantes de sistemas de filas M/M/1 de forma inteligente e interativa, incluindo **leitura de exercícios por imagem**!

## 🚀 Funcionalidades

### 📊 Métricas Principais
- **ρ (rho)**: Utilização do sistema (λ/μ)
- **L**: Número médio de clientes no sistema
- **Lq**: Número médio de clientes na fila
- **W**: Tempo médio no sistema
- **Wq**: Tempo médio na fila

### 🎯 Probabilidades
- **P0**: Probabilidade de sistema vazio
- **Pn**: Probabilidade de n clientes no sistema
- **P(N>k)**: Probabilidade de mais de k clientes

### 🧠 Inteligência com LangGraph
- Extração automática de parâmetros (λ, μ, n, k)
- Identificação inteligente do tipo de cálculo
- Validação de estabilidade do sistema
- Respostas explicativas detalhadas

## 🛠️ Instalação

### Método 1: Instalação Automática
```bash
python install.py
```

### Método 2: Instalação Manual
1. Clone o repositório:
```bash
git clone <seu-repositorio>
cd assistente-bene
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configure o arquivo .env:
```bash
# Crie o arquivo .env com sua chave Groq
GROQ_API_KEY=sua_chave_groq_aqui
GROQ_MODEL=llama-3.1-8b-instant
GROQ_TEMPERATURE=0.1
GROQ_MAX_TOKENS=2000
```

4. Execute a aplicação:
```bash
streamlit run Chatbot.py
```

## 💡 Como Usar

### Exemplos de Perguntas:

1. **Utilização do Sistema:**
   - "Calcule ρ com λ=2 e μ=3"
   - "Taxa de utilização com chegada=1.5 e atendimento=2"

2. **Número Médio de Clientes:**
   - "Número médio no sistema com λ=1 e μ=2"
   - "Quantos clientes na fila com λ=0.8 e μ=1.2"

3. **Tempos Médios:**
   - "Tempo médio no sistema com λ=2 e μ=3"
   - "Tempo de espera na fila com λ=1.5 e μ=2"

4. **Probabilidades:**
   - "Probabilidade de 3 clientes com λ=1 e μ=2"
   - "P(N>2) com λ=0.8 e μ=1.2"
   - "Probabilidade de sistema vazio com λ=1 e μ=1.5"

## 🔧 Arquitetura

### LangGraph Workflow:
1. **extract_parameters**: Extrai λ, μ, n, k da mensagem
2. **identify_calculation**: Identifica o tipo de cálculo
3. **perform_calculation**: Executa o cálculo usando ferramentas
4. **generate_response**: Gera resposta formatada

### Ferramentas M/M/1:
- `MM1Calculator`: Classe com todos os cálculos M/M/1
- Validação automática de estabilidade (ρ < 1)
- Tratamento de erros e casos especiais

## 📚 Fórmulas Implementadas

```
ρ = λ/μ
L = ρ/(1-ρ)
Lq = ρ²/(1-ρ)
W = 1/(μ-λ)
Wq = ρ/(μ-λ)
P0 = 1-ρ
Pn = (1-ρ)ρⁿ
P(N>k) = ρᵏ⁺¹
```

## 🎨 Interface

- **Sidebar**: Fórmulas, exemplos e configurações
- **Chat Interface**: Conversação natural com o Bosquinho
- **LaTeX**: Renderização matemática das fórmulas
- **Feedback Visual**: Indicadores de estabilidade e interpretações

## 🔮 Extensões Futuras

- Integração com Groq (Qwen QwQ 32B)
- Suporte a outros modelos de filas (M/M/c, M/G/1)
- Visualizações gráficas
- Exportação de resultados
- Histórico de cálculos

## 🤝 Contribuição

Contribuições são bem-vindas! Por favor, abra uma issue ou pull request.

## 📄 Licença

MIT License
