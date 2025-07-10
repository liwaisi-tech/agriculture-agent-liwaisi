"""
Consultas SQL para datos de sensores
"""
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from .connection import db
import logging
import re
from geopy.distance import geodesic  # Necesitas instalar geopy

logger = logging.getLogger(__name__)


class SensorQueries:
    """Consultas para datos de sensores"""
    
    @staticmethod
    def get_current_readings(sensor_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Obtiene las lecturas más recientes"""
        query = """
        SELECT 
            sr.timestamp,
            sr.temperature,
            sr.humidity,
            sr.sensor_id,
            sr.location,
            s.name as sensor_name,
            s.location_description
        FROM sensor_readings sr
        LEFT JOIN sensors s ON sr.sensor_id = s.id
        WHERE sr.timestamp >= NOW() - INTERVAL '1 hour'
        """
        
        params = None
        if sensor_id:
            query += " AND sr.sensor_id = %s"
            params = (sensor_id,)
        
        query += " ORDER BY sr.timestamp DESC LIMIT 10"
        
        return db.execute_query(query, params)
    
    @staticmethod
    def get_historical_data(
        start_date: str,
        end_date: str,
        sensor_id: Optional[str] = None,
        location: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Obtiene datos históricos por período"""
        query = """
        SELECT 
            sr.timestamp,
            sr.temperature,
            sr.humidity,
            sr.sensor_id,
            sr.location,
            s.name as sensor_name
        FROM sensor_readings sr
        LEFT JOIN sensors s ON sr.sensor_id = s.id
        WHERE sr.timestamp >= %s AND sr.timestamp <= %s
        """
        
        params = [start_date, end_date]
        
        if sensor_id:
            query += " AND sr.sensor_id = %s"
            params.append(sensor_id)
        
        if location:
            query += " AND sr.location ILIKE %s"
            params.append(f"%{location}%")
        
        query += " ORDER BY sr.timestamp DESC"
        
        return db.execute_query(query, tuple(params))
    
    @staticmethod
    def get_climate_summary(
        start_date: str,
        end_date: str,
        sensor_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Obtiene resumen estadístico del clima"""
        query = """
        SELECT 
            COUNT(*) as total_readings,
            AVG(temperature) as avg_temperature,
            MIN(temperature) as min_temperature,
            MAX(temperature) as max_temperature,
            AVG(humidity) as avg_humidity,
            MIN(humidity) as min_humidity,
            MAX(humidity) as max_humidity,
            STDDEV(temperature) as temp_stddev,
            STDDEV(humidity) as humidity_stddev
        FROM sensor_readings
        WHERE timestamp >= %s AND timestamp <= %s
        """
        
        params = [start_date, end_date]
        
        if sensor_id:
            query += " AND sensor_id = %s"
            params.append(sensor_id)
        
        results = db.execute_query(query, tuple(params))
        return results[0] if results else {}
    
    @staticmethod
    def get_daily_averages(
        start_date: str,
        end_date: str,
        sensor_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Obtiene promedios diarios"""
        query = """
        SELECT 
            DATE(timestamp) as date,
            AVG(temperature) as avg_temperature,
            MIN(temperature) as min_temperature,
            MAX(temperature) as max_temperature,
            AVG(humidity) as avg_humidity,
            MIN(humidity) as min_humidity,
            MAX(humidity) as max_humidity,
            COUNT(*) as readings_count
        FROM sensor_readings
        WHERE timestamp >= %s AND timestamp <= %s
        """
        
        params = [start_date, end_date]
        
        if sensor_id:
            query += " AND sensor_id = %s"
            params.append(sensor_id)
        
        query += " GROUP BY DATE(timestamp) ORDER BY date DESC"
        
        return db.execute_query(query, tuple(params))
    
    @staticmethod
    def get_hourly_averages(
        start_date: str,
        end_date: str,
        sensor_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Obtiene promedios por hora"""
        query = """
        SELECT 
            DATE_TRUNC('hour', timestamp) as hour,
            AVG(temperature) as avg_temperature,
            AVG(humidity) as avg_humidity,
            COUNT(*) as readings_count
        FROM sensor_readings
        WHERE timestamp >= %s AND timestamp <= %s
        """
        
        params = [start_date, end_date]
        
        if sensor_id:
            query += " AND sensor_id = %s"
            params.append(sensor_id)
        
        query += " GROUP BY DATE_TRUNC('hour', timestamp) ORDER BY hour DESC"
        
        return db.execute_query(query, tuple(params))
    
    @staticmethod
    def get_available_sensors() -> List[Dict[str, Any]]:
        """Obtiene lista de sensores disponibles"""
        query = """
        SELECT 
            id,
            name,
            type,
            location_description,
            latitude,
            longitude,
            installation_date,
            is_active
        FROM sensors
        WHERE is_active = TRUE
        ORDER BY name
        """
        
        return db.execute_query(query)


# Instancia para usar en otros módulos
sensor_queries = SensorQueries()

def extract_location_or_coords(query: str):
    # Buscar coordenadas (formato: número,número)
    coord_match = re.search(r'(-?\d+\.\d+)\s*,\s*(-?\d+\.\d+)', query)
    if coord_match:
        lat, lon = float(coord_match.group(1)), float(coord_match.group(2))
        return {'coords': (lat, lon)}
    # Buscar ubicaciones compuestas después de 'en' o 'de'
    loc_match = re.search(r'(?:en|de)\s+([^\.,;!?]+)', query, re.IGNORECASE)
    if loc_match:
        location = loc_match.group(1).strip()
        # Limpiar si termina en signo de puntuación
        location = re.sub(r'[.,;!?]+$', '', location)
        return {'location': location}
    return {}

def get_structured(self, query: str) -> List[Dict[str, Any]]:
    filtro = extract_location_or_coords(query)
    readings = sensor_queries.get_current_readings()
    if 'coords' in filtro:
        lat, lon = filtro['coords']
        # Filtrar por cercanía (ejemplo: 10 km)
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