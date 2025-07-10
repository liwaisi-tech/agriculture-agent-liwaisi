"""
Nodo de clasificación de consultas del agente de agricultura regenerativa
"""
from typing import Dict, Any
import logging
from agent.core.state import AgricultureState
from utils.date_parser import DateParser

logger = logging.getLogger(__name__)


def classify_query(state: AgricultureState) -> AgricultureState:
    """
    Clasifica el tipo de consulta del usuario
    """
    try:
        query = state["user_query"]
        
        # Sistema de clasificación basado en palabras clave
        query_lower = query.lower()
        
        # Patrones para diferentes tipos de consultas
        if any(word in query_lower for word in ["actual", "ahora", "hoy", "temperatura", "humedad", "sensor"]):
            query_type = "current_status"
        elif any(word in query_lower for word in ["histórico", "historia", "último", "pasado", "semana", "mes"]):
            query_type = "climate_history"
        elif any(word in query_lower for word in ["recomendación", "consejo", "qué sembrar", "cultivo"]):
            query_type = "recommendations"
        elif any(word in query_lower for word in ["arroz", "maíz", "yuca", "plátano", "cacao", "cítricos"]):
            query_type = "crop_advice"
        else:
            query_type = "general"
        
        # Extraer información adicional
        time_period = DateParser.parse_time_expression(query)
        crop_mentioned = _extract_crop_mention(query)
        location_mentioned = _extract_location_mention(query)
        
        # Actualizar estado
        state["query_type"] = query_type
        state["time_period"] = time_period
        state["crop_mentioned"] = crop_mentioned
        state["location_mentioned"] = location_mentioned
        state["processing_steps"].append("query_classified")
        
        logger.info(f"Consulta clasificada como: {query_type}")
        
        general_keywords = [
            "información general", "suelo", "suelos", "riego", "fertilización", "fertilizacion",
            "malezas", "residuos", "prácticas", "plagas", "umbrales", "estrés", "estres"
        ]
        for kw in general_keywords:
            if kw in query_lower:
                state["general_info_requested"] = True
                state["general_info_category"] = kw
                break
        
    except Exception as e:
        logger.error(f"Error clasificando consulta: {e}")
        state["error_message"] = f"Error clasificando la consulta: {str(e)}"
    
    return state


def _extract_crop_mention(query: str) -> str:
    """Extrae menciones de cultivos de la consulta"""
    crops = ["arroz", "maíz", "maiz", "yuca", "plátano", "platano", "cacao", "cítricos", "citricos"]
    query_lower = query.lower()
    
    for crop in crops:
        if crop in query_lower:
            return crop
    return None


def _extract_location_mention(query: str) -> str:
    """Extrae menciones de ubicación de la consulta"""
    # Ubicaciones comunes en Casanare
    locations = ["aguazul", "yopal", "villanueva", "tauramena", "monterrey", "sabanalarga"]
    query_lower = query.lower()
    
    for location in locations:
        if location in query_lower:
            return location
    return None 