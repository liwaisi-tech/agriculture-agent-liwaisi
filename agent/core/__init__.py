"""
Módulo core del agente de agricultura regenerativa

Contiene el grafo de flujo y la definición del estado del agente.
"""

from .graph import AgricultureGraph, create_agriculture_graph
from .state import AgricultureState, create_initial_state

__all__ = [
    'AgricultureGraph',
    'create_agriculture_graph',
    'AgricultureState', 
    'create_initial_state'
] 