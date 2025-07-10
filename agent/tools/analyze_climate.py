from langchain.tools import BaseTool
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
import logging
from database.queries import sensor_queries
from utils.climate_analyzer import climate_analyzer

logger = logging.getLogger(__name__)

class ClimateAnalysisInput(BaseModel):
    time_period: Dict[str, str] = Field(description="Período de tiempo {'start': 'YYYY-MM-DD', 'end': 'YYYY-MM-DD'}")
    location: Optional[str] = Field(default=None, description="Ubicación específica")

class AnalyzeClimateTool(BaseTool):
    """Herramienta para análisis climático detallado"""
    name = "analyze_climate"
    description = "Realiza un análisis detallado de datos climáticos y genera recomendaciones agrícolas"
    args_schema = ClimateAnalysisInput

    def _run(self, time_period: Dict[str, str], location: Optional[str] = None) -> str:
        try:
            data = sensor_queries.get_historical_data(
                start_date=time_period['start'],
                end_date=time_period['end'],
                location=location
            )
            if not data:
                return "No hay datos suficientes para análisis climático."
            analysis = climate_analyzer.analyze_climate_data(data)
            return str(analysis)
        except Exception as e:
            logger.error(f"Error en análisis climático: {e}")
            return f"Error en análisis climático: {str(e)}" 