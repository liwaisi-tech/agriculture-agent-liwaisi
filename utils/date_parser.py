"""
Parser de fechas para interpretar expresiones de tiempo del usuario
"""
import re
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple
from dateutil import parser as date_parser
from dateutil.relativedelta import relativedelta
import logging

logger = logging.getLogger(__name__)


class DateParser:
    """Parser para interpretar expresiones de tiempo en español"""
    
    # Patrones para expresiones de tiempo en español
    TIME_PATTERNS = {
        # Días específicos
        "hoy": r"\b(hoy)\b",
        "ayer": r"\b(ayer)\b", 
        "mañana": r"\b(mañana|manana)\b",
        "anteayer": r"\b(anteayer|ante ayer)\b",
        "pasado mañana": r"\b(pasado mañana|pasado manana)\b",
        
        # Días de la semana
        "dias_semana": r"\b(lunes|martes|miércoles|miercoles|jueves|viernes|sábado|sabado|domingo)\b",
        
        # Meses
        "meses": r"\b(enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre)\b",
        
        # Períodos relativos
        "ultima_semana": r"\b(última semana|ultima semana|semana pasada)\b",
        "proxima_semana": r"\b(próxima semana|proxima semana|siguiente semana)\b",
        "ultimo_mes": r"\b(último mes|ultimo mes|mes pasado)\b",
        "proximo_mes": r"\b(próximo mes|proximo mes|siguiente mes)\b",
        "ultimo_ano": r"\b(último año|ultimo ano|año pasado|ano pasado)\b",
        "proximo_ano": r"\b(próximo año|proximo ano|siguiente año|siguiente ano)\b",
        
        # Períodos específicos
        "ultimos_dias": r"\b(últimos?\s+(\d+)\s+días?|ultimos?\s+(\d+)\s+dias)\b",
        "proximos_dias": r"\b(próximos?\s+(\d+)\s+días?|proximos?\s+(\d+)\s+dias)\b",
        "ultimas_semanas": r"\b(últimas?\s+(\d+)\s+semanas?|ultimas?\s+(\d+)\s+semanas?)\b",
        "proximas_semanas": r"\b(próximas?\s+(\d+)\s+semanas?|proximas?\s+(\d+)\s+semanas?)\b",
        "ultimos_meses": r"\b(últimos?\s+(\d+)\s+meses?|ultimos?\s+(\d+)\s+meses?)\b",
        "proximos_meses": r"\b(próximos?\s+(\d+)\s+meses?|proximos?\s+(\d+)\s+meses?)\b",
        
        # Fechas específicas
        "fecha_especifica": r"\b(\d{1,2})[/-](\d{1,2})[/-](\d{4})\b",  # DD/MM/YYYY o DD-MM-YYYY
        "fecha_texto": r"\b(\d{1,2})\s+(de\s+)?(enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre)(\s+(de\s+)?(\d{4}))?\b",
        
        # Temporadas agrícolas
        "temporada_actual": r"\b(temporada actual|época actual|epoca actual)\b",
        "temporada_pasada": r"\b(temporada pasada|época pasada|epoca pasada)\b",
        "temporada_proxima": r"\b(temporada próxima|temporada proxima|época próxima|epoca proxima)\b",
    }
    
    # Mapeo de días de la semana
    DIAS_SEMANA = {
        "lunes": 0, "martes": 1, "miércoles": 2, "miercoles": 2,
        "jueves": 3, "viernes": 4, "sábado": 5, "sabado": 5, "domingo": 6
    }
    
    # Mapeo de meses
    MESES = {
        "enero": 1, "febrero": 2, "marzo": 3, "abril": 4, "mayo": 5, "junio": 6,
        "julio": 7, "agosto": 8, "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12
    }
    
    @classmethod
    def parse_time_expression(cls, text: str) -> Optional[Dict[str, str]]:
        """
        Parsea una expresión de tiempo y retorna un diccionario con fechas de inicio y fin
        
        Args:
            text: Texto con expresión de tiempo
            
        Returns:
            Dict con 'start' y 'end' en formato YYYY-MM-DD, o None si no se puede parsear
        """
        text_lower = text.lower().strip()
        
        try:
            # Intentar parsear expresiones específicas
            result = cls._parse_specific_expressions(text_lower)
            if result:
                return result
            
            # Intentar parsear fechas específicas
            result = cls._parse_specific_dates(text_lower)
            if result:
                return result
            
            # Intentar parsear períodos relativos
            result = cls._parse_relative_periods(text_lower)
            if result:
                return result
            
            # Intentar parsear días de la semana
            result = cls._parse_weekday(text_lower)
            if result:
                return result
            
            logger.warning(f"No se pudo parsear la expresión de tiempo: {text}")
            return None
            
        except Exception as e:
            logger.error(f"Error parseando expresión de tiempo '{text}': {e}")
            return None
    
    @classmethod
    def _parse_specific_expressions(cls, text: str) -> Optional[Dict[str, str]]:
        """Parsea expresiones específicas como 'hoy', 'ayer', etc."""
        today = datetime.now()
        
        if re.search(cls.TIME_PATTERNS["hoy"], text):
            return {
                "start": today.strftime("%Y-%m-%d"),
                "end": today.strftime("%Y-%m-%d")
            }
        
        elif re.search(cls.TIME_PATTERNS["ayer"], text):
            yesterday = today - timedelta(days=1)
            return {
                "start": yesterday.strftime("%Y-%m-%d"),
                "end": yesterday.strftime("%Y-%m-%d")
            }
        
        elif re.search(cls.TIME_PATTERNS["mañana"], text):
            tomorrow = today + timedelta(days=1)
            return {
                "start": tomorrow.strftime("%Y-%m-%d"),
                "end": tomorrow.strftime("%Y-%m-%d")
            }
        
        elif re.search(cls.TIME_PATTERNS["anteayer"], text):
            day_before_yesterday = today - timedelta(days=2)
            return {
                "start": day_before_yesterday.strftime("%Y-%m-%d"),
                "end": day_before_yesterday.strftime("%Y-%m-%d")
            }
        
        elif re.search(cls.TIME_PATTERNS["pasado mañana"], text):
            day_after_tomorrow = today + timedelta(days=2)
            return {
                "start": day_after_tomorrow.strftime("%Y-%m-%d"),
                "end": day_after_tomorrow.strftime("%Y-%m-%d")
            }
        
        return None
    
    @classmethod
    def _parse_relative_periods(cls, text: str) -> Optional[Dict[str, str]]:
        """Parsea períodos relativos como 'última semana', 'próximo mes', etc."""
        today = datetime.now()
        
        # Última semana
        match = re.search(cls.TIME_PATTERNS["ultima_semana"], text)
        if match:
            end_date = today - timedelta(days=today.weekday() + 1)
            start_date = end_date - timedelta(days=6)
            return {
                "start": start_date.strftime("%Y-%m-%d"),
                "end": end_date.strftime("%Y-%m-%d")
            }
        
        # Próxima semana
        match = re.search(cls.TIME_PATTERNS["proxima_semana"], text)
        if match:
            start_date = today + timedelta(days=7-today.weekday())
            end_date = start_date + timedelta(days=6)
            return {
                "start": start_date.strftime("%Y-%m-%d"),
                "end": end_date.strftime("%Y-%m-%d")
            }
        
        # Último mes
        match = re.search(cls.TIME_PATTERNS["ultimo_mes"], text)
        if match:
            end_date = today.replace(day=1) - timedelta(days=1)
            start_date = end_date.replace(day=1)
            return {
                "start": start_date.strftime("%Y-%m-%d"),
                "end": end_date.strftime("%Y-%m-%d")
            }
        
        # Próximo mes
        match = re.search(cls.TIME_PATTERNS["proximo_mes"], text)
        if match:
            start_date = (today.replace(day=1) + relativedelta(months=1))
            end_date = (start_date + relativedelta(months=1)) - timedelta(days=1)
            return {
                "start": start_date.strftime("%Y-%m-%d"),
                "end": end_date.strftime("%Y-%m-%d")
            }
        
        # Últimos N días
        match = re.search(cls.TIME_PATTERNS["ultimos_dias"], text)
        if match:
            days = int(match.group(2) or match.group(3))
            end_date = today
            start_date = today - timedelta(days=days-1)
            return {
                "start": start_date.strftime("%Y-%m-%d"),
                "end": end_date.strftime("%Y-%m-%d")
            }
        
        # Próximos N días
        match = re.search(cls.TIME_PATTERNS["proximos_dias"], text)
        if match:
            days = int(match.group(2) or match.group(3))
            start_date = today
            end_date = today + timedelta(days=days-1)
            return {
                "start": start_date.strftime("%Y-%m-%d"),
                "end": end_date.strftime("%Y-%m-%d")
            }
        
        return None
    
    @classmethod
    def _parse_specific_dates(cls, text: str) -> Optional[Dict[str, str]]:
        """Parsea fechas específicas como '15/03/2024' o '15 de marzo'"""
        today = datetime.now()
        
        # Formato DD/MM/YYYY o DD-MM-YYYY
        match = re.search(cls.TIME_PATTERNS["fecha_especifica"], text)
        if match:
            day, month, year = int(match.group(1)), int(match.group(2)), int(match.group(3))
            try:
                date_obj = datetime(year, month, day)
                return {
                    "start": date_obj.strftime("%Y-%m-%d"),
                    "end": date_obj.strftime("%Y-%m-%d")
                }
            except ValueError:
                return None
        
        # Formato "15 de marzo" o "15 de marzo de 2024"
        match = re.search(cls.TIME_PATTERNS["fecha_texto"], text)
        if match:
            day = int(match.group(1))
            month_name = match.group(3)
            month = cls.MESES.get(month_name)
            year = int(match.group(5)) if match.group(5) else today.year
            
            try:
                date_obj = datetime(year, month, day)
                return {
                    "start": date_obj.strftime("%Y-%m-%d"),
                    "end": date_obj.strftime("%Y-%m-%d")
                }
            except ValueError:
                return None
        
        return None
    
    @classmethod
    def _parse_weekday(cls, text: str) -> Optional[Dict[str, str]]:
        """Parsea días de la semana como 'lunes', 'martes', etc."""
        today = datetime.now()
        
        for day_name, day_num in cls.DIAS_SEMANA.items():
            if day_name in text:
                # Calcular el próximo día de la semana
                days_ahead = day_num - today.weekday()
                if days_ahead <= 0:  # Si ya pasó esta semana, ir a la próxima
                    days_ahead += 7
                
                target_date = today + timedelta(days=days_ahead)
                return {
                    "start": target_date.strftime("%Y-%m-%d"),
                    "end": target_date.strftime("%Y-%m-%d")
                }
        
        return None
    
    @classmethod
    def get_current_season(cls) -> str:
        """Determina la temporada agrícola actual en Casanare"""
        today = datetime.now()
        month = today.month
        
        if month in [12, 1, 2, 3]:
            return "epoca_seca"
        elif month in [4, 5]:
            return "inicio_lluvias"
        elif month in [6, 7, 8, 9, 10]:
            return "epoca_lluviosa"
        else:  # noviembre
            return "transicion"
    
    @classmethod
    def format_date_range(cls, start_date: str, end_date: str) -> str:
        """Formatea un rango de fechas en español"""
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        
        if start == end:
            return f"el {start.strftime('%d de %B de %Y')}"
        else:
            return f"del {start.strftime('%d de %B')} al {end.strftime('%d de %B de %Y')}"


# Función de conveniencia para uso directo
def parse_time_expression(text: str) -> Optional[Dict[str, str]]:
    """Función de conveniencia para parsear expresiones de tiempo"""
    return DateParser.parse_time_expression(text)
