"""
Calculadora para métricas de sistemas de filas M/M/1
"""

from typing import Dict, Any
from models.state import MM1Parameters, CalculationResult


class MM1Calculator:
    """Calculadora especializada em sistemas de filas M/M/1"""
    
    @staticmethod
    def calculate_rho(lambda_rate: float, mu_rate: float) -> Dict[str, Any]:
        """Calcula a utilização do sistema (ρ = λ/μ)"""
        try:
            params = MM1Parameters(lambda_rate, mu_rate)
            error = params.validate()
            if error:
                return {"error": error}
            
            result = CalculationResult(
                value=params.rho,
                description=f"Utilização do sistema: ρ = λ/μ = {lambda_rate}/{mu_rate} = {params.rho:.4f}",
                calc_type="rho",
                is_stable=params.is_stable,
                lambda_rate=lambda_rate,
                mu_rate=mu_rate
            )
            
            return result.to_dict()
            
        except Exception as e:
            return {"error": f"Erro no cálculo de ρ: {str(e)}"}
    
    @staticmethod
    def calculate_L(lambda_rate: float, mu_rate: float) -> Dict[str, Any]:
        """Calcula o número médio de clientes no sistema (L)"""
        try:
            params = MM1Parameters(lambda_rate, mu_rate)
            error = params.validate()
            if error:
                return {"error": error}
            
            if not params.is_stable:
                return {"error": "Sistema instável (ρ ≥ 1). O sistema não pode processar a demanda."}
            
            L = params.rho / (1 - params.rho)
            
            result = CalculationResult(
                value=L,
                description=f"Número médio no sistema: L = ρ/(1-ρ) = {params.rho:.4f}/(1-{params.rho:.4f}) = {L:.4f}",
                calc_type="L",
                rho=params.rho
            )
            
            return result.to_dict()
            
        except Exception as e:
            return {"error": f"Erro no cálculo de L: {str(e)}"}
    
    @staticmethod
    def calculate_Lq(lambda_rate: float, mu_rate: float) -> Dict[str, Any]:
        """Calcula o número médio de clientes na fila (Lq)"""
        try:
            params = MM1Parameters(lambda_rate, mu_rate)
            error = params.validate()
            if error:
                return {"error": error}
            
            if not params.is_stable:
                return {"error": "Sistema instável (ρ ≥ 1). O sistema não pode processar a demanda."}
            
            Lq = (params.rho ** 2) / (1 - params.rho)
            
            result = CalculationResult(
                value=Lq,
                description=f"Número médio na fila: Lq = ρ²/(1-ρ) = {params.rho:.4f}²/(1-{params.rho:.4f}) = {Lq:.4f}",
                calc_type="Lq",
                rho=params.rho
            )
            
            return result.to_dict()
            
        except Exception as e:
            return {"error": f"Erro no cálculo de Lq: {str(e)}"}
    
    @staticmethod
    def calculate_W(lambda_rate: float, mu_rate: float) -> Dict[str, Any]:
        """Calcula o tempo médio no sistema (W)"""
        try:
            params = MM1Parameters(lambda_rate, mu_rate)
            error = params.validate()
            if error:
                return {"error": error}
            
            if not params.is_stable:
                return {"error": "Sistema instável (ρ ≥ 1). O sistema não pode processar a demanda."}
            
            W = 1 / (mu_rate - lambda_rate)
            
            result = CalculationResult(
                value=W,
                description=f"Tempo médio no sistema: W = 1/(μ-λ) = 1/({mu_rate}-{lambda_rate}) = {W:.4f}",
                calc_type="W"
            )
            
            return result.to_dict()
            
        except Exception as e:
            return {"error": f"Erro no cálculo de W: {str(e)}"}
    
    @staticmethod
    def calculate_Wq(lambda_rate: float, mu_rate: float) -> Dict[str, Any]:
        """Calcula o tempo médio na fila (Wq)"""
        try:
            params = MM1Parameters(lambda_rate, mu_rate)
            error = params.validate()
            if error:
                return {"error": error}
            
            if not params.is_stable:
                return {"error": "Sistema instável (ρ ≥ 1). O sistema não pode processar a demanda."}
            
            Wq = params.rho / (mu_rate - lambda_rate)
            
            result = CalculationResult(
                value=Wq,
                description=f"Tempo médio na fila: Wq = ρ/(μ-λ) = {params.rho:.4f}/({mu_rate}-{lambda_rate}) = {Wq:.4f}",
                calc_type="Wq",
                rho=params.rho
            )
            
            return result.to_dict()
            
        except Exception as e:
            return {"error": f"Erro no cálculo de Wq: {str(e)}"}
    
    @staticmethod
    def calculate_P0(lambda_rate: float, mu_rate: float) -> Dict[str, Any]:
        """Calcula a probabilidade de 0 clientes no sistema (P0)"""
        try:
            params = MM1Parameters(lambda_rate, mu_rate)
            error = params.validate()
            if error:
                return {"error": error}
            
            if not params.is_stable:
                return {"error": "Sistema instável (ρ ≥ 1). O sistema não pode processar a demanda."}
            
            P0 = 1 - params.rho
            
            result = CalculationResult(
                value=P0,
                description=f"Probabilidade de sistema vazio: P0 = 1-ρ = 1-{params.rho:.4f} = {P0:.4f}",
                calc_type="P0",
                rho=params.rho
            )
            
            return result.to_dict()
            
        except Exception as e:
            return {"error": f"Erro no cálculo de P0: {str(e)}"}
    
    @staticmethod
    def calculate_Pn(lambda_rate: float, mu_rate: float, n: int) -> Dict[str, Any]:
        """Calcula a probabilidade de n clientes no sistema (Pn)"""
        try:
            params = MM1Parameters(lambda_rate, mu_rate, n=n)
            error = params.validate()
            if error:
                return {"error": error}
            
            if not params.is_stable:
                return {"error": "Sistema instável (ρ ≥ 1). O sistema não pode processar a demanda."}
            
            Pn = (1 - params.rho) * (params.rho ** n)
            
            result = CalculationResult(
                value=Pn,
                description=f"Probabilidade de {n} clientes: Pn = (1-ρ)×ρⁿ = (1-{params.rho:.4f})×{params.rho:.4f}^{n} = {Pn:.4f}",
                calc_type="Pn",
                n=n,
                rho=params.rho
            )
            
            return result.to_dict()
            
        except Exception as e:
            return {"error": f"Erro no cálculo de Pn: {str(e)}"}
    
    @staticmethod
    def calculate_P_greater_than_k(lambda_rate: float, mu_rate: float, k: int) -> Dict[str, Any]:
        """Calcula a probabilidade de mais de k clientes no sistema P(N>k)"""
        try:
            params = MM1Parameters(lambda_rate, mu_rate, k=k)
            error = params.validate()
            if error:
                return {"error": error}
            
            if not params.is_stable:
                return {"error": "Sistema instável (ρ ≥ 1). O sistema não pode processar a demanda."}
            
            P_greater_k = params.rho ** (k + 1)
            
            result = CalculationResult(
                value=P_greater_k,
                description=f"Probabilidade de mais de {k} clientes: P(N>{k}) = ρ^{k+1} = {params.rho:.4f}^{k+1} = {P_greater_k:.4f}",
                calc_type="P_greater_k",
                k=k,
                rho=params.rho
            )
            
            return result.to_dict()
            
        except Exception as e:
            return {"error": f"Erro no cálculo de P(N>k): {str(e)}"}
