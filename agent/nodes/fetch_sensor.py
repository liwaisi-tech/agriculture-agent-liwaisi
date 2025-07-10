"""
Nodo de obtención de datos de sensores del agente de agricultura regenerativa
"""
from typing import Dict, Any, List
import logging
from agent.core.state import AgricultureState
from agent.tools import AVAILABLE_TOOLS

logger = logging.getLogger(__name__)


def fetch_sensor_data(state: AgricultureState) -> AgricultureState:
    """
    Obtiene datos de sensores según el tipo de consulta
    """
    try:
        # Crear diccionario de herramientas
        tools = {tool.name: tool for tool in AVAILABLE_TOOLS}
        
        query_type = state["query_type"]
        time_period = state["time_period"]
        location = state["location_mentioned"]
        
        if query_type == "current_status":
            # Obtener lecturas actuales
            tool = tools["get_current_readings"]
            state["sensor_data"] = tool.get_structured(state["user_query"])
            
        elif query_type == "climate_history" and time_period:
            # Obtener datos históricos
            tool = tools["get_historical_data"]
            state["sensor_data"] = tool.get_structured(
                time_expression=_extract_time_expression(state["user_query"]),
                location=location
            )
            
        elif query_type in ["recommendations", "crop_advice"]:
            # Para recomendaciones, obtener datos actuales como contexto
            tool = tools["get_current_readings"]
            state["sensor_data"] = tool.get_structured("condiciones actuales")
        
        state["processing_steps"].append("sensor_data_fetched")
        
    except Exception as e:
        logger.error(f"Error obteniendo datos de sensores: {e}")
        state["error_message"] = f"Error obteniendo datos de sensores: {str(e)}"
    
    return state


def _extract_time_expression(query: str) -> str:
    """Extrae expresión de tiempo de la consulta"""
    time_keywords = [
        "ayer", "hoy", "mañana", "última semana", "ultima semana", 
        "próxima semana", "proxima semana", "último mes", "ultimo mes",
        "últimos días", "ultimos dias", "próximos días", "proximos dias"
    ]
    
    query_lower = query.lower()
    for keyword in time_keywords:
        if keyword in query_lower:
            return keyword
    
    return "última semana"  # Default 