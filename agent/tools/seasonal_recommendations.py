from langchain.tools import BaseTool
from typing import Any
from pydantic import BaseModel, Field
import logging
from utils.date_parser import DateParser
from knowledge.casanare_crops import CasanareCrops

logger = logging.getLogger(__name__)

class QueryInput(BaseModel):
    query: str = Field(description="Consulta del usuario")

class GetSeasonalRecommendationsTool(BaseTool):
    """Herramienta para obtener recomendaciones estacionales"""
    name = "get_seasonal_recommendations"
    description = "Obtiene recomendaciones agrícolas para la temporada actual"
    args_schema = QueryInput

    def _run(self, query: str) -> str:
        try:
            current_season = DateParser.get_current_season()
            season_info = CasanareCrops.AGRICULTURAL_CALENDAR.get(current_season, {})
            if not season_info:
                return "No hay información de temporada disponible."
            return str(season_info)
        except Exception as e:
            logger.error(f"Error obteniendo recomendaciones estacionales: {e}")
            return f"Error obteniendo recomendaciones estacionales: {str(e)}" 