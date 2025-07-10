from langchain.tools import BaseTool
from typing import Any, Optional
from pydantic import BaseModel, Field
import logging
from knowledge.agriculture_data import AgricultureData

logger = logging.getLogger(__name__)

class GeneralAgricultureInfoInput(BaseModel):
    category: str = Field(description="Categoría de información: suelo, riego, fertilización, malezas, residuos, prácticas, plagas")
    value: Optional[str] = Field(default=None, description="Valor específico a consultar (ej: tipo de suelo, tipo de fertilización, cultivo para plagas)")

class GetGeneralAgricultureInfoTool(BaseTool):
    """Herramienta para obtener información agrícola general"""
    name = "get_general_agriculture_info"
    description = "Obtiene información general agrícola: suelos, riego, fertilización, malezas, residuos, prácticas universales, plagas."
    args_schema = GeneralAgricultureInfoInput

    def _run(self, category: str, value: Optional[str] = None) -> str:
        try:
            if category in ["suelo", "suelos"]:
                if value:
                    info = AgricultureData.get_soil_info(value)
                    return str(info) if info else f"No se encontró información para el tipo de suelo '{value}'."
                return str(AgricultureData.SOIL_TYPES)
            elif category in ["riego"]:
                return str(AgricultureData.get_irrigation_methods())
            elif category in ["fertilización", "fertilizacion"]:
                if value:
                    info = AgricultureData.get_fertilization_guide(value)
                    return str(info) if info else f"No se encontró información para el tipo de fertilización '{value}'."
                return str(AgricultureData.FERTILIZATION_GUIDE)
            elif category in ["malezas"]:
                return str(AgricultureData.get_weed_management_methods())
            elif category in ["residuos"]:
                return str(AgricultureData.get_residue_management())
            elif category in ["prácticas", "practicas"]:
                return str(AgricultureData.get_universal_practices())
            elif category in ["plagas"]:
                if value:
                    return str(AgricultureData.get_common_pests(value))
                return str(AgricultureData.get_common_pests())
            else:
                return "Categoría no reconocida. Usa: suelo, riego, fertilización, malezas, residuos, prácticas, plagas."
        except Exception as e:
            logger.error(f"Error obteniendo información agrícola general: {e}")
            return f"Error obteniendo información agrícola general: {str(e)}" 