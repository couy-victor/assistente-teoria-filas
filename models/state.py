"""
Definições de estado e tipos de dados para o sistema Bosquinho
"""

from typing import Dict, Any, List, Optional, TypedDict
from typing_extensions import Annotated
from langgraph.graph.message import add_messages


class BosquinhoState(TypedDict):
    """Estado do grafo LangGraph para o assistente Bosquinho"""
    messages: Annotated[List[Dict], add_messages]
    lambda_rate: Optional[float]
    mu_rate: Optional[float]
    n_value: Optional[int]
    k_value: Optional[int]
    calculation_result: Optional[Dict]
    error_message: Optional[str]


class CalculationResult:
    """Resultado de um cálculo M/M/1"""
    def __init__(self, value: float, description: str, calc_type: str, **kwargs):
        self.value = value
        self.description = description
        self.calc_type = calc_type
        self.metadata = kwargs
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "value": self.value,
            "description": self.description,
            "type": self.calc_type,
            **self.metadata
        }


class MM1Parameters:
    """Parâmetros para cálculos M/M/1"""
    def __init__(self, lambda_rate: float, mu_rate: float, n: Optional[int] = None, k: Optional[int] = None):
        self.lambda_rate = lambda_rate
        self.mu_rate = mu_rate
        self.n = n
        self.k = k
        self.rho = lambda_rate / mu_rate if mu_rate > 0 else float('inf')
        self.is_stable = self.rho < 1
    
    def validate(self) -> Optional[str]:
        """Valida os parâmetros"""
        if self.lambda_rate < 0:
            return "Taxa de chegada (λ) deve ser não-negativa"
        if self.mu_rate <= 0:
            return "Taxa de atendimento (μ) deve ser positiva"
        if self.n is not None and self.n < 0:
            return "Valor de n deve ser não-negativo"
        if self.k is not None and self.k < 0:
            return "Valor de k deve ser não-negativo"
        return None
