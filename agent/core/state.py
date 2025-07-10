"""
Estado del agente de agricultura regenerativa
"""
from typing import TypedDict, List, Dict, Optional, Any
from datetime import datetime


class AgricultureState(TypedDict):
    """Estado compartido del agente de agricultura"""
    
    # Input del usuario
    user_query: str
    user_location: str
    
    # Análisis de la consulta
    query_type: str  # "climate_history", "recommendations", "current_status", "crop_advice"
    time_period: Optional[Dict[str, str]]  # {"start": "2024-01-01", "end": "2024-01-31"}
    crop_mentioned: Optional[str]  # Cultivo mencionado si hay
    location_mentioned: Optional[str]  # Ubicación específica si la menciona
    
    # Datos de sensores
    sensor_data: List[Dict[str, Any]]
    climate_summary: Dict[str, Any]  # Resumen estadístico
    
    # Conocimiento agrícola
    crop_requirements: Dict[str, Any]
    season_info: Dict[str, Any]
    recommendations: List[str]
    
    # Respuesta final
    final_answer: str
    confidence: float
    
    # Control de flujo
    needs_data_query: bool
    needs_crop_analysis: bool
    needs_clarification: bool
    error_message: Optional[str]
    
    # Metadata
    processing_steps: List[str]  # Para debugging
    timestamp: str


def create_initial_state(user_query: str) -> AgricultureState:
    """Crea el estado inicial del agente"""
    return AgricultureState(
        user_query=user_query,
        user_location="El Guineo, Aguazul, Casanare, Colombia",
        query_type="",
        time_period=None,
        crop_mentioned=None,
        location_mentioned=None,
        sensor_data=[],
        climate_summary={},
        crop_requirements={},
        season_info={},
        recommendations=[],
        final_answer="",
        confidence=0.0,
        needs_data_query=False,
        needs_crop_analysis=False,
        needs_clarification=False,
        error_message=None,
        processing_steps=[],
        timestamp=datetime.now().isoformat()
    ) 