"""
Nodo de análisis de datos climáticos del agente de agricultura regenerativa
"""
from typing import Dict, Any
import logging
from agent.core.state import AgricultureState
from utils.climate_analyzer import climate_analyzer
from knowledge.agriculture_data import AgricultureData

logger = logging.getLogger(__name__)


def analyze_climate_data(state: AgricultureState) -> AgricultureState:
    """
    Analiza los datos climáticos obtenidos
    """
    try:
        if state["sensor_data"]:
            # Realizar análisis climático
            analysis = climate_analyzer.analyze_climate_data(state["sensor_data"])
            state["climate_summary"] = analysis
            
            # Detectar estrés térmico/hídrico
            thresholds = AgricultureData.get_stress_thresholds()
            avg_temp = analysis.get("basic_stats", {}).get("temperature", {}).get("mean")
            avg_hum = analysis.get("basic_stats", {}).get("humidity", {}).get("mean")
            if avg_temp is not None and (avg_temp < thresholds["temperature"]["low"] or avg_temp > thresholds["temperature"]["high"]):
                state["suggest_general_info"] = True
                state["suggested_category"] = "umbrales"
            if avg_hum is not None and (avg_hum < thresholds["humidity"]["low"] or avg_hum > thresholds["humidity"]["high"]):
                state["suggest_general_info"] = True
                state["suggested_category"] = "umbrales"
            
            # Generar recomendaciones basadas en el análisis
            recommendations = climate_analyzer.get_climate_recommendations(analysis)
            state["recommendations"].extend(recommendations)
        
        state["processing_steps"].append("climate_analyzed")
        
    except Exception as e:
        logger.error(f"Error analizando datos climáticos: {e}")
        state["error_message"] = f"Error analizando datos climáticos: {str(e)}"
    
    return state 