"""
Analizador de datos climáticos para agricultura regenerativa
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import logging
from database.queries import sensor_queries
from knowledge.casanare_crops import CasanareCrops

logger = logging.getLogger(__name__)


class ClimateAnalyzer:
    """Analizador de datos climáticos para agricultura"""
    
    def __init__(self):
        self.crops_knowledge = CasanareCrops()
    
    def analyze_climate_data(
        self, 
        sensor_data: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Analiza datos de sensores y genera insights climáticos
        
        Args:
            sensor_data: Lista de lecturas de sensores
            
        Returns:
            Diccionario con análisis climático
        """
        if not sensor_data:
            return self._empty_analysis()
        
        try:
            # Convertir a DataFrame para análisis
            df = pd.DataFrame(sensor_data)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            # Análisis básico
            basic_stats = self._calculate_basic_stats(df)
            
            # Análisis de tendencias
            trends = self._analyze_trends(df)
            
            # Análisis de extremos
            extremes = self._analyze_extremes(df)
            
            # Análisis de variabilidad
            variability = self._analyze_variability(df)
            
            # Análisis agrícola
            agricultural_analysis = self._analyze_agricultural_conditions(df)
            
            # Análisis de temporada
            season_analysis = self._analyze_seasonal_patterns(df)
            
            return {
                "basic_stats": basic_stats,
                "trends": trends,
                "extremes": extremes,
                "variability": variability,
                "agricultural_analysis": agricultural_analysis,
                "season_analysis": season_analysis,
                "data_quality": self._assess_data_quality(df),
                "analysis_timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error analizando datos climáticos: {e}")
            return self._empty_analysis()
    
    def _calculate_basic_stats(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Calcula estadísticas básicas de temperatura y humedad"""
        stats = {}
        
        for metric in ['temperature', 'humidity']:
            if metric in df.columns:
                values = df[metric].dropna()
                if len(values) > 0:
                    stats[metric] = {
                        "mean": float(values.mean()),
                        "median": float(values.median()),
                        "min": float(values.min()),
                        "max": float(values.max()),
                        "std": float(values.std()),
                        "count": int(len(values))
                    }
                else:
                    stats[metric] = {"error": "No hay datos válidos"}
            else:
                stats[metric] = {"error": "Columna no encontrada"}
        
        return stats
    
    def _analyze_trends(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analiza tendencias temporales en los datos"""
        trends = {}
        
        # Ordenar por timestamp
        df_sorted = df.sort_values('timestamp')
        
        for metric in ['temperature', 'humidity']:
            if metric in df_sorted.columns:
                values = df_sorted[metric].dropna()
                if len(values) > 1:
                    # Calcular tendencia lineal
                    x = np.arange(len(values))
                    slope, intercept = np.polyfit(x, values, 1)
                    
                    # Calcular R²
                    y_pred = slope * x + intercept
                    r_squared = 1 - (np.sum((values - y_pred) ** 2) / np.sum((values - values.mean()) ** 2))
                    
                    trends[metric] = {
                        "slope": float(slope),
                        "trend_direction": "increasing" if slope > 0.01 else "decreasing" if slope < -0.01 else "stable",
                        "trend_strength": "strong" if abs(r_squared) > 0.7 else "moderate" if abs(r_squared) > 0.3 else "weak",
                        "r_squared": float(r_squared),
                        "change_per_hour": float(slope * 60)  # Asumiendo datos cada minuto
                    }
                else:
                    trends[metric] = {"error": "Datos insuficientes para análisis de tendencia"}
            else:
                trends[metric] = {"error": "Columna no encontrada"}
        
        return trends
    
    def _analyze_extremes(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analiza eventos extremos y valores atípicos"""
        extremes = {}
        
        for metric in ['temperature', 'humidity']:
            if metric in df.columns:
                values = df[metric].dropna()
                if len(values) > 0:
                    # Calcular percentiles
                    percentiles = np.percentile(values, [5, 25, 50, 75, 95])
                    
                    # Identificar outliers usando IQR
                    Q1, Q3 = percentiles[1], percentiles[3]
                    IQR = Q3 - Q1
                    lower_bound = Q1 - 1.5 * IQR
                    upper_bound = Q3 + 1.5 * IQR
                    
                    outliers = values[(values < lower_bound) | (values > upper_bound)]
                    
                    # Eventos extremos (valores más altos/bajos del 5%)
                    extreme_high = values[values >= percentiles[4]]
                    extreme_low = values[values <= percentiles[0]]
                    
                    extremes[metric] = {
                        "percentiles": {
                            "p5": float(percentiles[0]),
                            "p25": float(percentiles[1]),
                            "p50": float(percentiles[2]),
                            "p75": float(percentiles[3]),
                            "p95": float(percentiles[4])
                        },
                        "outliers": {
                            "count": int(len(outliers)),
                            "percentage": float(len(outliers) / len(values) * 100),
                            "values": [float(x) for x in outliers.head(10).tolist()]
                        },
                        "extreme_events": {
                            "high_count": int(len(extreme_high)),
                            "low_count": int(len(extreme_low)),
                            "high_values": [float(x) for x in extreme_high.head(5).tolist()],
                            "low_values": [float(x) for x in extreme_low.head(5).tolist()]
                        }
                    }
                else:
                    extremes[metric] = {"error": "No hay datos válidos"}
            else:
                extremes[metric] = {"error": "Columna no encontrada"}
        
        return extremes
    
    def _analyze_variability(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analiza la variabilidad temporal de los datos"""
        variability = {}
        
        # Agrupar por hora para analizar variabilidad diaria
        df['hour'] = df['timestamp'].dt.hour
        df['day'] = df['timestamp'].dt.date
        
        for metric in ['temperature', 'humidity']:
            if metric in df.columns:
                # Variabilidad por hora del día
                hourly_stats = df.groupby('hour')[metric].agg(['mean', 'std']).reset_index()
                
                # Variabilidad por día
                daily_stats = df.groupby('day')[metric].agg(['mean', 'std', 'min', 'max']).reset_index()
                
                # Coeficiente de variación
                overall_cv = df[metric].std() / df[metric].mean() if df[metric].mean() != 0 else 0
                
                variability[metric] = {
                    "coefficient_of_variation": float(overall_cv),
                    "variability_level": "high" if overall_cv > 0.3 else "moderate" if overall_cv > 0.1 else "low",
                    "hourly_pattern": {
                        "hour_with_max_variability": int(hourly_stats.loc[hourly_stats['std'].idxmax(), 'hour']),
                        "hour_with_min_variability": int(hourly_stats.loc[hourly_stats['std'].idxmin(), 'hour']),
                        "max_std": float(hourly_stats['std'].max()),
                        "min_std": float(hourly_stats['std'].min())
                    },
                    "daily_pattern": {
                        "day_with_max_range": str(daily_stats.loc[(daily_stats['max'] - daily_stats['min']).idxmax(), 'day']),
                        "max_daily_range": float((daily_stats['max'] - daily_stats['min']).max()),
                        "avg_daily_range": float((daily_stats['max'] - daily_stats['min']).mean())
                    }
                }
            else:
                variability[metric] = {"error": "Columna no encontrada"}
        
        return variability
    
    def _analyze_agricultural_conditions(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analiza las condiciones para agricultura basado en los datos climáticos"""
        if 'temperature' not in df.columns or 'humidity' not in df.columns:
            return {"error": "Datos de temperatura y humedad requeridos"}
        
        temp_values = df['temperature'].dropna()
        humidity_values = df['humidity'].dropna()
        
        if len(temp_values) == 0 or len(humidity_values) == 0:
            return {"error": "Datos insuficientes"}
        
        # Calcular promedios
        avg_temp = temp_values.mean()
        avg_humidity = humidity_values.mean()
        
        # Obtener cultivos adecuados
        suitable_crops = self.crops_knowledge.get_suitable_crops_for_conditions(
            avg_temp, avg_humidity
        )
        
        # Analizar condiciones por cultivo
        crop_conditions = {}
        for crop_info in suitable_crops[:5]:  # Top 5 cultivos
            crop_name = crop_info['crop']
            temp_range = crop_info['optimal_temperature']
            humidity_range = crop_info['optimal_humidity']
            
            # Calcular qué porcentaje del tiempo las condiciones son óptimas
            temp_optimal = ((temp_values >= temp_range['min']) & 
                           (temp_values <= temp_range['max'])).mean() * 100
            humidity_optimal = ((humidity_values >= humidity_range['min']) & 
                              (humidity_values <= humidity_range['max'])).mean() * 100
            
            crop_conditions[crop_name] = {
                "suitability": crop_info['suitability'],
                "temp_optimal_percentage": float(temp_optimal),
                "humidity_optimal_percentage": float(humidity_optimal),
                "overall_optimal_percentage": float((temp_optimal + humidity_optimal) / 2),
                "recommendations": crop_info.get('regenerative_practices', [])
            }
        
        return {
            "average_conditions": {
                "temperature": float(avg_temp),
                "humidity": float(avg_humidity)
            },
            "suitable_crops": suitable_crops[:5],
            "crop_conditions": crop_conditions,
            "overall_assessment": self._assess_overall_conditions(avg_temp, avg_humidity)
        }
    
    def _analyze_seasonal_patterns(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analiza patrones estacionales en los datos"""
        if 'timestamp' not in df.columns:
            return {"error": "Columna timestamp requerida"}
        
        df['month'] = df['timestamp'].dt.month
        df['season'] = df['month'].apply(self._get_season)
        
        seasonal_stats = {}
        for metric in ['temperature', 'humidity']:
            if metric in df.columns:
                season_data = df.groupby('season')[metric].agg(['mean', 'std', 'min', 'max']).reset_index()
                seasonal_stats[metric] = season_data.to_dict('records')
        
        # Comparar con patrones típicos de Casanare
        casanare_patterns = self._get_casanare_seasonal_patterns()
        
        return {
            "seasonal_stats": seasonal_stats,
            "casanare_patterns": casanare_patterns,
            "season_comparison": self._compare_with_casanare_patterns(seasonal_stats, casanare_patterns)
        }
    
    def _get_season(self, month: int) -> str:
        """Determina la temporada basada en el mes"""
        if month in [12, 1, 2, 3]:
            return "epoca_seca"
        elif month in [4, 5]:
            return "inicio_lluvias"
        elif month in [6, 7, 8, 9, 10]:
            return "epoca_lluviosa"
        else:
            return "transicion"
    
    def _get_casanare_seasonal_patterns(self) -> Dict[str, Dict[str, Any]]:
        """Obtiene patrones estacionales típicos de Casanare"""
        return {
            "epoca_seca": {
                "temperature": {"mean": 32, "std": 3, "min": 25, "max": 38},
                "humidity": {"mean": 65, "std": 10, "min": 45, "max": 80}
            },
            "inicio_lluvias": {
                "temperature": {"mean": 30, "std": 2, "min": 24, "max": 35},
                "humidity": {"mean": 75, "std": 8, "min": 60, "max": 85}
            },
            "epoca_lluviosa": {
                "temperature": {"mean": 28, "std": 2, "min": 22, "max": 32},
                "humidity": {"mean": 85, "std": 5, "min": 75, "max": 95}
            },
            "transicion": {
                "temperature": {"mean": 29, "std": 3, "min": 23, "max": 34},
                "humidity": {"mean": 75, "std": 10, "min": 60, "max": 85}
            }
        }
    
    def _compare_with_casanare_patterns(
        self, 
        actual_stats: Dict[str, List], 
        expected_patterns: Dict[str, Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Compara estadísticas actuales con patrones típicos de Casanare"""
        comparison = {}
        
        for metric in ['temperature', 'humidity']:
            if metric in actual_stats:
                comparison[metric] = {}
                for season_data in actual_stats[metric]:
                    season = season_data['season']
                    if season in expected_patterns:
                        expected = expected_patterns[season][metric]
                        actual_mean = season_data['mean']
                        expected_mean = expected['mean']
                        
                        deviation = actual_mean - expected_mean
                        deviation_percent = (deviation / expected_mean) * 100
                        
                        comparison[metric][season] = {
                            "actual_mean": float(actual_mean),
                            "expected_mean": float(expected_mean),
                            "deviation": float(deviation),
                            "deviation_percent": float(deviation_percent),
                            "status": "above_normal" if deviation > 0 else "below_normal" if deviation < 0 else "normal"
                        }
        
        return comparison
    
    def _assess_overall_conditions(self, avg_temp: float, avg_humidity: float) -> str:
        """Evalúa las condiciones generales para agricultura"""
        if avg_temp < 15 or avg_temp > 40:
            return "desfavorable"
        elif avg_humidity < 40 or avg_humidity > 95:
            return "desfavorable"
        elif 20 <= avg_temp <= 35 and 60 <= avg_humidity <= 85:
            return "excelente"
        else:
            return "aceptable"
    
    def _assess_data_quality(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Evalúa la calidad de los datos"""
        total_rows = len(df)
        if total_rows == 0:
            return {"quality": "poor", "issues": ["No hay datos"]}
        
        issues = []
        
        # Verificar valores faltantes
        for col in ['temperature', 'humidity']:
            if col in df.columns:
                missing_pct = df[col].isna().sum() / total_rows * 100
                if missing_pct > 20:
                    issues.append(f"Muchos valores faltantes en {col}: {missing_pct:.1f}%")
        
        # Verificar valores fuera de rango razonable
        if 'temperature' in df.columns:
            temp_outliers = df[(df['temperature'] < -10) | (df['temperature'] > 50)]
            if len(temp_outliers) > 0:
                issues.append(f"Valores de temperatura fuera de rango: {len(temp_outliers)} registros")
        
        if 'humidity' in df.columns:
            humidity_outliers = df[(df['humidity'] < 0) | (df['humidity'] > 100)]
            if len(humidity_outliers) > 0:
                issues.append(f"Valores de humedad fuera de rango: {len(humidity_outliers)} registros")
        
        # Determinar calidad
        if len(issues) == 0:
            quality = "excellent"
        elif len(issues) <= 2:
            quality = "good"
        elif len(issues) <= 4:
            quality = "fair"
        else:
            quality = "poor"
        
        return {
            "quality": quality,
            "total_records": total_rows,
            "issues": issues,
            "completeness": float((total_rows - df.isna().sum().sum()) / (total_rows * len(df.columns)) * 100)
        }
    
    def _empty_analysis(self) -> Dict[str, Any]:
        """Retorna análisis vacío cuando no hay datos"""
        return {
            "basic_stats": {},
            "trends": {},
            "extremes": {},
            "variability": {},
            "agricultural_analysis": {"error": "No hay datos para analizar"},
            "season_analysis": {},
            "data_quality": {"quality": "poor", "issues": ["No hay datos"]},
            "analysis_timestamp": datetime.now().isoformat()
        }
    
    def get_climate_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """Genera recomendaciones basadas en el análisis climático"""
        recommendations = []
        
        # Verificar si hay análisis agrícola
        ag_analysis = analysis.get('agricultural_analysis', {})
        if 'error' in ag_analysis:
            recommendations.append("Se necesitan más datos climáticos para generar recomendaciones específicas")
            return recommendations
        
        # Recomendaciones basadas en condiciones promedio
        avg_conditions = ag_analysis.get('average_conditions', {})
        if avg_conditions:
            temp = avg_conditions.get('temperature', 0)
            humidity = avg_conditions.get('humidity', 0)
            
            if temp > 35:
                recommendations.append("Las temperaturas están altas. Considerar riego adicional y sombra para cultivos sensibles")
            elif temp < 20:
                recommendations.append("Las temperaturas están bajas. Considerar cultivos resistentes al frío o protección térmica")
            
            if humidity > 90:
                recommendations.append("La humedad está muy alta. Vigilar enfermedades fúngicas y mejorar ventilación")
            elif humidity < 50:
                recommendations.append("La humedad está baja. Considerar riego más frecuente y mulching")
        
        # Recomendaciones basadas en cultivos adecuados
        suitable_crops = ag_analysis.get('suitable_crops', [])
        if suitable_crops:
            top_crop = suitable_crops[0]
            recommendations.append(f"El cultivo más adecuado para las condiciones actuales es {top_crop['name']}")
        
        # Recomendaciones basadas en variabilidad
        variability = analysis.get('variability', {})
        temp_variability = variability.get('temperature', {})
        if temp_variability.get('variability_level') == 'high':
            recommendations.append("Hay alta variabilidad en temperatura. Considerar cultivos resistentes a cambios bruscos")
        
        return recommendations


# Instancia global para uso en otros módulos
climate_analyzer = ClimateAnalyzer()
