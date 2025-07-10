"""
Nodos de control del flujo del agente de agricultura regenerativa
"""
from typing import Dict, Any
import logging
from agent.core.state import AgricultureState

logger = logging.getLogger(__name__)


def handle_error(state: AgricultureState) -> AgricultureState:
    """
    Maneja errores y genera respuesta de error
    """
    if state.get("error_message"):
        state["final_answer"] = f"❌ **Error:** {state['error_message']}\n\n"
        state["final_answer"] += "Por favor, intenta reformular tu consulta o contacta soporte si el problema persiste."
        state["confidence"] = 0.0
    
    return state


def should_continue(state: AgricultureState) -> bool:
    """
    Determina si el flujo debe continuar
    """
    # Continuar si no hay error y no se ha generado respuesta final
    return not state.get("error_message") and not state.get("final_answer") 