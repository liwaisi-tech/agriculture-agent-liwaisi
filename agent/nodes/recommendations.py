"""
Nodo de recomendaciones de cultivos del agente de agricultura regenerativa
"""
from typing import Dict, Any
import logging
from agent.core.state import AgricultureState
from agent.tools import AVAILABLE_TOOLS
from utils.date_parser import DateParser
from knowledge.casanare_crops import CasanareCrops

logger = logging.getLogger(__name__)


def get_crop_recommendations(state: AgricultureState) -> AgricultureState:
    """
    Obtiene recomendaciones específicas de cultivos
    """
    try:
        # Crear diccionario de herramientas
        tools = {tool.name: tool for tool in AVAILABLE_TOOLS}
        
        query_type = state["query_type"]
        crop_mentioned = state["crop_mentioned"]
        
        if query_type == "crop_advice" and crop_mentioned:
            # Obtener información específica del cultivo
            tool = tools["get_crop_info"]
            result = tool._run(crop_name=crop_mentioned, location=state["location_mentioned"])
            
            # Extraer información del cultivo
            crop_info = CasanareCrops.get_crop_info(crop_mentioned)
            if crop_info:
                state["crop_requirements"] = crop_info
                state["recommendations"].extend(crop_info.get("regenerative_practices", []))
        
        elif query_type == "recommendations":
            # Obtener recomendaciones estacionales
            tool = tools["get_seasonal_recommendations"]
            result = tool._run(state["user_query"])
            
            # Obtener información de la temporada actual
            current_season = DateParser.get_current_season()
            season_info = CasanareCrops.AGRICULTURAL_CALENDAR.get(current_season, {})
            state["season_info"] = season_info
        
        state["processing_steps"].append("crop_recommendations_generated")
        
    except Exception as e:
        logger.error(f"Error obteniendo recomendaciones de cultivos: {e}")
        state["error_message"] = f"Error obteniendo recomendaciones de cultivos: {str(e)}"
    
    return state 