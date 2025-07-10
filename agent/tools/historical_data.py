from langchain.tools import BaseTool
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field
import logging
from database.queries import sensor_queries
from utils.date_parser import DateParser

logger = logging.getLogger(__name__)

class TimeRangeInput(BaseModel):
    time_expression: str = Field(description="Expresión de tiempo (ej: 'última semana', 'ayer')")
    location: Optional[str] = Field(default=None, description="Ubicación específica")

class GetHistoricalDataTool(BaseTool):
    """Herramienta para obtener datos históricos"""
    name = "get_historical_data"
    description = "Obtiene datos históricos de sensores para un período específico"
    args_schema = TimeRangeInput

    def _run(self, time_expression: str, location: Optional[str] = None) -> str:
        try:
            time_period = DateParser.parse_time_expression(time_expression)
            if not time_period:
                return f"No se pudo interpretar la expresión de tiempo: '{time_expression}'. Prueba con: 'ayer', 'última semana', '15/03/2024', etc."
            data = sensor_queries.get_historical_data(
                start_date=time_period['start'],
                end_date=time_period['end'],
                location=location
            )
            if not data:
                return f"No hay datos históricos disponibles para el período {DateParser.format_date_range(time_period['start'], time_period['end'])}."
            response = f"📈 **Datos históricos {DateParser.format_date_range(time_period['start'], time_period['end'])}:**\n\n"
            temperatures = [d['temperature'] for d in data if d.get('temperature') is not None]
            humidities = [d['humidity'] for d in data if d.get('humidity') is not None]
            if temperatures:
                response += f"🌡️ **Temperatura:**\n"
                response += f"   • Promedio: {sum(temperatures)/len(temperatures):.1f}°C\n"
                response += f"   • Mínima: {min(temperatures):.1f}°C\n"
                response += f"   • Máxima: {max(temperatures):.1f}°C\n\n"
            if humidities:
                response += f"💧 **Humedad:**\n"
                response += f"   • Promedio: {sum(humidities)/len(humidities):.1f}%\n"
                response += f"   • Mínima: {min(humidities):.1f}%\n"
                response += f"   • Máxima: {max(humidities):.1f}%\n\n"
            response += f"📊 Total de registros: {len(data)}"
            return response
        except Exception as e:
            logger.error(f"Error obteniendo datos históricos: {e}")
            return f"Error al obtener datos históricos: {str(e)}"
    def get_structured(self, time_expression: str, location: Optional[str] = None) -> List[Dict[str, Any]]:
        time_period = DateParser.parse_time_expression(time_expression)
        if not time_period:
            return []
        data = sensor_queries.get_historical_data(
            start_date=time_period['start'],
            end_date=time_period['end'],
            location=location
        )
        return data 