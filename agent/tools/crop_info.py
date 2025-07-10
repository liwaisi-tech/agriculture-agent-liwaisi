from langchain.tools import BaseTool
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
import logging
from knowledge.casanare_crops import CasanareCrops

logger = logging.getLogger(__name__)

class CropInput(BaseModel):
    crop_name: str = Field(description="Nombre del cultivo")
    location: Optional[str] = Field(default=None, description="Ubicación específica")

class GetCropInfoTool(BaseTool):
    """Herramienta para obtener información de cultivos"""
    name = "get_crop_info"
    description = "Obtiene información detallada sobre un cultivo específico"
    args_schema = CropInput

    def _run(self, crop_name: str, location: Optional[str] = None) -> str:
        try:
            crop_info = CasanareCrops.get_crop_info(crop_name)
            if not crop_info:
                return f"No se encontró información para el cultivo '{crop_name}'."
            return str(crop_info)
        except Exception as e:
            logger.error(f"Error obteniendo información de cultivo: {e}")
            return f"Error obteniendo información de cultivo: {str(e)}" 