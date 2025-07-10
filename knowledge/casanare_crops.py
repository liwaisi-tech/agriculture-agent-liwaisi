"""
Base de conocimiento de cultivos para Casanare, Colombia
"""
from typing import Dict, List, Any
from datetime import datetime


class CasanareCrops:
    """Conocimiento específico de cultivos para Casanare"""
    
    # Cultivos principales de Casanare
    CROPS_DATA = {
        "arroz": {
            "name": "Arroz",
            "scientific_name": "Oryza sativa",
            "optimal_temperature": {"min": 20, "max": 35, "ideal": 28},
            "optimal_humidity": {"min": 70, "max": 85, "ideal": 78},
            "planting_seasons": ["marzo-mayo", "agosto-octubre"],
            "growth_period_days": 120,
            "water_requirements": "alto",
            "soil_type": "arcilloso, bien drenado",
            "regenerative_practices": [
                "Rotación con leguminosas",
                "Manejo integrado de plagas",
                "Uso de abonos orgánicos",
                "Sistema de riego eficiente"
            ],
            "casanare_notes": "Cultivo principal de los llanos, se adapta bien al clima tropical"
        },
        "maiz": {
            "name": "Maíz",
            "scientific_name": "Zea mays",
            "optimal_temperature": {"min": 15, "max": 35, "ideal": 25},
            "optimal_humidity": {"min": 60, "max": 80, "ideal": 70},
            "planting_seasons": ["marzo-mayo", "septiembre-noviembre"],
            "growth_period_days": 90,
            "water_requirements": "medio",
            "soil_type": "franco, bien drenado",
            "regenerative_practices": [
                "Asociación con frijol",
                "Mulching con residuos",
                "Compostaje",
                "Control biológico de plagas"
            ],
            "casanare_notes": "Excelente adaptación al clima llanero, resistente a sequías"
        },
        "yuca": {
            "name": "Yuca",
            "scientific_name": "Manihot esculenta",
            "optimal_temperature": {"min": 20, "max": 35, "ideal": 27},
            "optimal_humidity": {"min": 50, "max": 80, "ideal": 65},
            "planting_seasons": ["marzo-mayo", "agosto-octubre"],
            "growth_period_days": 240,
            "water_requirements": "bajo",
            "soil_type": "franco-arenoso, bien drenado",
            "regenerative_practices": [
                "Policultivo con frutales",
                "Abonos verdes",
                "Conservación de suelos",
                "Uso de residuos orgánicos"
            ],
            "casanare_notes": "Muy resistente a sequías, ideal para agricultura de subsistencia"
        },
        "platano": {
            "name": "Plátano",
            "scientific_name": "Musa paradisiaca",
            "optimal_temperature": {"min": 20, "max": 35, "ideal": 28},
            "optimal_humidity": {"min": 70, "max": 90, "ideal": 80},
            "planting_seasons": ["marzo-mayo", "septiembre-noviembre"],
            "growth_period_days": 365,
            "water_requirements": "alto",
            "soil_type": "franco, materia orgánica alta",
            "regenerative_practices": [
                "Sistemas agroforestales",
                "Mulching con hojas",
                "Compostaje de residuos",
                "Policultivo con cacao"
            ],
            "casanare_notes": "Requiere zonas protegidas del viento, ideal cerca de fuentes de agua"
        },
        "cacao": {
            "name": "Cacao",
            "scientific_name": "Theobroma cacao",
            "optimal_temperature": {"min": 20, "max": 32, "ideal": 26},
            "optimal_humidity": {"min": 75, "max": 85, "ideal": 80},
            "planting_seasons": ["marzo-mayo"],
            "growth_period_days": 1095,  # 3 años para producción
            "water_requirements": "alto",
            "soil_type": "franco, rico en materia orgánica",
            "regenerative_practices": [
                "Sistemas agroforestales",
                "Sombra con árboles nativos",
                "Compostaje",
                "Diversificación de cultivos"
            ],
            "casanare_notes": "Requiere sombra y alta humedad, ideal en zonas de galería"
        },
        "citricos": {
            "name": "Cítricos",
            "scientific_name": "Citrus spp.",
            "optimal_temperature": {"min": 15, "max": 35, "ideal": 25},
            "optimal_humidity": {"min": 60, "max": 80, "ideal": 70},
            "planting_seasons": ["marzo-mayo", "septiembre-octubre"],
            "growth_period_days": 1095,  # 3 años para producción
            "water_requirements": "medio",
            "soil_type": "franco, bien drenado",
            "regenerative_practices": [
                "Podas sanitarias",
                "Manejo integrado de plagas",
                "Abonos orgánicos",
                "Conservación de agua"
            ],
            "casanare_notes": "Naranjas y limones se adaptan bien, requieren buen drenaje"
        }
    }
    
    # Calendario agrícola de Casanare
    AGRICULTURAL_CALENDAR = {
        "epoca_seca": {
            "months": ["diciembre", "enero", "febrero", "marzo"],
            "characteristics": "Baja precipitación, temperaturas altas",
            "recommendations": [
                "Preparación de suelos",
                "Siembra de cultivos resistentes a sequía",
                "Mantenimiento de sistemas de riego",
                "Cosecha de cultivos de temporada lluviosa"
            ]
        },
        "inicio_lluvias": {
            "months": ["abril", "mayo"],
            "characteristics": "Incremento de precipitaciones",
            "recommendations": [
                "Siembra principal de arroz",
                "Siembra de maíz",
                "Preparación de almácigos",
                "Control de malezas",
                "Esperar la segundas lluvia fuerte para sembrar"
            ]
        },
        "epoca_lluviosa": {
            "months": ["junio", "julio", "agosto", "septiembre", "octubre"],
            "characteristics": "Alta precipitación y humedad",
            "recommendations": [
                "Mantenimiento de cultivos",
                "Control de plagas y enfermedades",
                "Cosecha de cultivos de ciclo corto",
                "Siembra de segunda temporada"
            ]
        },
        "transicion": {
            "months": ["noviembre"],
            "characteristics": "Disminución gradual de lluvias",
            "recommendations": [
                "Cosecha principal",
                "Preparación para época seca",
                "Almacenamiento de agua",
                "Planificación de próxima temporada"
            ]
        }
    }
    
    @classmethod
    def get_crop_info(cls, crop_name: str) -> Dict[str, Any]:
        """Obtiene información de un cultivo específico"""
        crop_key = crop_name.lower().replace("í", "i").replace("ñ", "n")
        return cls.CROPS_DATA.get(crop_key, {})
    
    @classmethod
    def get_suitable_crops_for_conditions(
        cls, 
        temperature: float, 
        humidity: float
    ) -> List[Dict[str, Any]]:
        """Obtiene cultivos adecuados para las condiciones dadas"""
        suitable_crops = []
        
        for crop_key, crop_data in cls.CROPS_DATA.items():
            temp_range = crop_data["optimal_temperature"]
            humidity_range = crop_data["optimal_humidity"]
            
            # Verificar si las condiciones están dentro del rango óptimo
            temp_suitable = temp_range["min"] <= temperature <= temp_range["max"]
            humidity_suitable = humidity_range["min"] <= humidity <= humidity_range["max"]
            
            if temp_suitable and humidity_suitable:
                suitable_crops.append({
                    "crop": crop_data["name"],
                    "suitability": "óptimo",
                    "temp_match": abs(temperature - temp_range["ideal"]),
                    "humidity_match": abs(humidity - humidity_range["ideal"]),
                    **crop_data
                })
            elif temp_suitable or humidity_suitable:
                suitable_crops.append({
                    "crop": crop_data["name"],
                    "suitability": "aceptable",
                    "temp_match": abs(temperature - temp_range["ideal"]),
                    "humidity_match": abs(humidity - humidity_range["ideal"]),
                    **crop_data
                })
        
        # Ordenar por mejor coincidencia
        suitable_crops.sort(key=lambda x: x["temp_match"] + x["humidity_match"])
        
        return suitable_crops
    
    @classmethod
    def get_current_season_recommendations(cls) -> Dict[str, Any]:
        """Obtiene recomendaciones para la época actual"""
        current_month = datetime.now().strftime("%B").lower()
        
        # Mapear meses en español
        month_mapping = {
            "january": "enero", "february": "febrero", "march": "marzo",
            "april": "abril", "may": "mayo", "june": "junio",
            "july": "julio", "august": "agosto", "september": "septiembre",
            "october": "octubre", "november": "noviembre", "december": "diciembre"
        }
        
        spanish_month = month_mapping.get(current_month, "enero")
        
        for season, data in cls.AGRICULTURAL_CALENDAR.items():
            if spanish_month in [m.lower() for m in data["months"]]:
                return {
                    "season": season,
                    "current_month": spanish_month,
                    **data
                }
        
        return cls.AGRICULTURAL_CALENDAR["epoca_seca"]  # Default
    
    @classmethod
    def get_regenerative_practices(cls, crop_name: str = None) -> List[str]:
        """Obtiene prácticas regenerativas generales o específicas"""
        if crop_name:
            crop_info = cls.get_crop_info(crop_name)
            return crop_info.get("regenerative_practices", [])
        
        # Prácticas generales para Casanare
        return [
            "Rotación de cultivos con leguminosas",
            "Uso de abonos orgánicos y compost",
            "Conservación de suelos con coberturas",
            "Sistemas agroforestales",
            "Manejo integrado de plagas",
            "Conservación de agua lluvia",
            "Diversificación de cultivos",
            "Uso de microorganismos benéficos"
        ]


# Instancia para usar en otros módulos
casanare_crops = CasanareCrops()