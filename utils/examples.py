"""
Exemplos reais para o sistema Bosquinho - M/M/1
"""

from typing import Dict, List, Any
from utils.mm1_calculator import MM1Calculator


class AirportExample:
    """Exemplos de aeroporto - Sistema de pouso de aviões"""
    
    @staticmethod
    def get_example_1() -> Dict[str, Any]:
        """
        Exemplo 1: Aeroporto com sistema de pouso
        Taxa de chegada: λ = 1/3 aviões por minuto
        Taxa de atendimento: μ = 1 avião por minuto
        """
        return {
            "title": "🛩️ Sistema de Pouso de Aviões - Exemplo 1",
            "description": """
**Cenário:** Aeroporto com pista única para pouso
- Aviões chegam em média a cada 3 minutos (λ = 1/3 por minuto)
- Tempo médio de pouso: 1 minuto (μ = 1 por minuto)
            """,
            "lambda_rate": 1/3,
            "mu_rate": 1,
            "questions": [
                "Qual a taxa de utilização da pista?",
                "Qual a probabilidade de não haver aviões no sistema?",
                "Qual a probabilidade de haver exatamente 1 avião?",
                "Qual a probabilidade de não haver mais que 3 aviões?",
                "Número médio de aviões aguardando pouso?",
                "Tempo médio que um avião fica sobrevoando?"
            ]
        }
    
    @staticmethod
    def get_example_2() -> Dict[str, Any]:
        """
        Exemplo 2: Aeroporto com maior capacidade
        Taxa de chegada: λ = 1 avião por minuto  
        Taxa de atendimento: μ = 3 aviões por minuto
        """
        return {
            "title": "🛩️ Sistema de Pouso de Aviões - Exemplo 2", 
            "description": """
**Cenário:** Aeroporto com pista de alta capacidade
- Aviões chegam em média 1 por minuto (λ = 1 por minuto)
- Consegue atender 3 aviões por minuto (μ = 3 por minuto)
            """,
            "lambda_rate": 1,
            "mu_rate": 3,
            "questions": [
                "Taxa de utilização do sistema?",
                "Probabilidade de nenhum avião na pista?", 
                "Probabilidade de apenas 1 avião no sistema?",
                "Número médio de aviões no sistema?",
                "Tempo médio no sistema?"
            ]
        }
    
    @staticmethod
    def solve_example_1() -> Dict[str, Any]:
        """Resolve o Exemplo 1 completamente"""
        calc = MM1Calculator()
        lambda_rate = 1/3
        mu_rate = 1
        
        results = {}
        
        # a) Taxa de utilização
        results["rho"] = calc.calculate_rho(lambda_rate, mu_rate)
        
        # b) Probabilidade de sistema vazio
        results["P0"] = calc.calculate_P0(lambda_rate, mu_rate)
        
        # c) Probabilidade de 1 avião
        results["P1"] = calc.calculate_Pn(lambda_rate, mu_rate, 1)
        
        # d) Probabilidade de não mais que 3 aviões: P(N≤3) = 1 - P(N>3)
        p_greater_3 = calc.calculate_P_greater_than_k(lambda_rate, mu_rate, 3)
        if "error" not in p_greater_3:
            results["P_leq_3"] = {
                "value": 1 - p_greater_3["value"],
                "description": f"P(N≤3) = 1 - P(N>3) = 1 - {p_greater_3['value']:.4f} = {1 - p_greater_3['value']:.4f}",
                "type": "P_leq_3"
            }
        
        # e) Número médio na fila (aguardando)
        results["Lq"] = calc.calculate_Lq(lambda_rate, mu_rate)
        
        # f) Tempo médio na fila (sobrevoando)
        results["Wq"] = calc.calculate_Wq(lambda_rate, mu_rate)
        
        return results
    
    @staticmethod
    def solve_example_2() -> Dict[str, Any]:
        """Resolve o Exemplo 2 completamente"""
        calc = MM1Calculator()
        lambda_rate = 1
        mu_rate = 3
        
        results = {}
        
        # a) Taxa de utilização
        results["rho"] = calc.calculate_rho(lambda_rate, mu_rate)
        
        # b) Probabilidade de sistema vazio
        results["P0"] = calc.calculate_P0(lambda_rate, mu_rate)
        
        # c) Probabilidade de 1 avião
        results["P1"] = calc.calculate_Pn(lambda_rate, mu_rate, 1)
        
        # d) Número médio no sistema
        results["L"] = calc.calculate_L(lambda_rate, mu_rate)
        
        # e) Tempo médio no sistema
        results["W"] = calc.calculate_W(lambda_rate, mu_rate)
        
        return results


class BankExample:
    """Exemplos de banco - Sistema de atendimento"""
    
    @staticmethod
    def get_example() -> Dict[str, Any]:
        """
        Exemplo: Banco com um caixa
        Taxa de chegada: λ = 2 clientes por minuto
        Taxa de atendimento: μ = 3 clientes por minuto
        """
        return {
            "title": "🏦 Sistema de Atendimento Bancário",
            "description": """
**Cenário:** Banco com um caixa eletrônico
- Clientes chegam em média 2 por minuto (λ = 2 por minuto)
- Caixa atende 3 clientes por minuto (μ = 3 por minuto)
            """,
            "lambda_rate": 2,
            "mu_rate": 3,
            "questions": [
                "Taxa de utilização do caixa?",
                "Número médio de clientes na fila?",
                "Tempo médio de espera na fila?",
                "Probabilidade de mais de 2 clientes no sistema?"
            ]
        }


class RestaurantExample:
    """Exemplos de restaurante - Sistema de pedidos"""
    
    @staticmethod
    def get_example() -> Dict[str, Any]:
        """
        Exemplo: Restaurante drive-thru
        Taxa de chegada: λ = 1.5 carros por minuto
        Taxa de atendimento: μ = 2 carros por minuto
        """
        return {
            "title": "🍔 Sistema Drive-Thru",
            "description": """
**Cenário:** Restaurante drive-thru com uma janela
- Carros chegam em média 1.5 por minuto (λ = 1.5 por minuto)
- Atendimento médio: 2 carros por minuto (μ = 2 por minuto)
            """,
            "lambda_rate": 1.5,
            "mu_rate": 2,
            "questions": [
                "Sistema está estável?",
                "Número médio de carros na fila?",
                "Tempo médio total no drive-thru?",
                "Probabilidade de sistema vazio?"
            ]
        }


def get_all_examples() -> List[Dict[str, Any]]:
    """Retorna todos os exemplos disponíveis"""
    return [
        AirportExample.get_example_1(),
        AirportExample.get_example_2(),
        BankExample.get_example(),
        RestaurantExample.get_example()
    ]


def get_example_solutions() -> Dict[str, Any]:
    """Retorna as soluções dos exemplos"""
    return {
        "airport_1": AirportExample.solve_example_1(),
        "airport_2": AirportExample.solve_example_2()
    }
