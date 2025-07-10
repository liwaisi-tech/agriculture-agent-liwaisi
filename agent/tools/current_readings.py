from langchain.tools import BaseTool
from typing import Dict, List, Any
from pydantic import BaseModel, Field
from datetime import datetime
import logging
from database.queries import sensor_queries, extract_location_or_coords
from geopy.distance import geodesic

logger = logging.getLogger(__name__)

class QueryInput(BaseModel):
    query: str = Field(description="Consulta del usuario")

class GetCurrentReadingsTool(BaseTool):
    """Herramienta para obtener lecturas actuales de sensores"""
    name = "get_current_readings"
    description = "Obtiene las lecturas más recientes de los sensores climáticos"
    args_schema = QueryInput

    def _run(self, query: str) -> str:
        try:
            location = None
            if "en" in query.lower() or "de" in query.lower():
                words = query.lower().split()
                for i, word in enumerate(words):
                    if word in ["en", "de"] and i + 1 < len(words):
                        location = words[i + 1]
                        break
            readings = sensor_queries.get_current_readings()
            if not readings:
                return "No hay lecturas recientes disponibles de los sensores."
            if location:
                readings = [r for r in readings if location.lower() in r.get('location', '').lower()]
            if not readings:
                return f"No hay lecturas disponibles para la ubicación '{location}'."
            response = "📊 **Lecturas actuales de sensores:**\n\n"
            for reading in readings[:5]:
                timestamp = reading['timestamp']
                if isinstance(timestamp, str):
                    timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                response += f"📍 **{reading.get('sensor_name', 'Sensor')}** ({reading.get('location', 'Ubicación no especificada')})\n"
                response += f"🕐 {timestamp.strftime('%d/%m/%Y %H:%M')}\n"
                response += f"🌡️ Temperatura: {reading.get('temperature', 'N/A')}°C\n"
                response += f"💧 Humedad: {reading.get('humidity', 'N/A')}%\n\n"
            return response
        except Exception as e:
            logger.error(f"Error obteniendo lecturas actuales: {e}")
            return f"Error al obtener las lecturas de sensores: {str(e)}"
    def get_structured(self, query: str) -> List[Dict[str, Any]]:
        filtro = extract_location_or_coords(query)
        readings = sensor_queries.get_current_readings()
        if 'coords' in filtro:
            lat, lon = filtro['coords']
            def is_near(sensor):
                s_lat = sensor.get('latitude')
                s_lon = sensor.get('longitude')
                if s_lat is not None and s_lon is not None:
                    dist = geodesic((lat, lon), (s_lat, s_lon)).km
                    return dist < 10
                return False
            readings = [r for r in readings if is_near(r)]
        elif 'location' in filtro:
            loc = filtro['location'].lower()
            readings = [r for r in readings if loc in r.get('location', '').lower() or loc in r.get('location_description', '').lower()]
        return readings 