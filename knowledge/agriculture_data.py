"""
Base de conocimiento agrícola general
"""
from typing import Dict, List, Any, Optional

class AgricultureData:
    """Conocimiento agrícola general (no específico de un cultivo)"""

    # Tipos de suelo y características
    SOIL_TYPES = {
        "arcilloso": {
            "description": "Suelos pesados, retienen agua, pobres en drenaje.",
            "recommended_crops": ["arroz", "pastos", "algunos frutales"],
            "improvement_practices": [
                "Incorporar materia orgánica",
                "Drenaje superficial"
            ]
        },
        "franco": {
            "description": "Suelos equilibrados, buena retención y drenaje.",
            "recommended_crops": ["maíz", "yuca", "hortalizas", "cacao"],
            "improvement_practices": [
                "Rotación de cultivos",
                "Cobertura vegetal"
            ]
        },
        "arenoso": {
            "description": "Suelos ligeros, drenan rápido, pobres en nutrientes.",
            "recommended_crops": ["maní", "sandía", "melón"],
            "improvement_practices": [
                "Aporte de compost",
                "Mulching"
            ]
        }
    }

    # Requerimientos hídricos generales (mm/semana)
    GENERAL_WATER_REQUIREMENTS = {
        "bajo": "Menos de 20 mm/semana",
        "medio": "20-40 mm/semana",
        "alto": "Más de 40 mm/semana"
    }

    # Umbrales de estrés térmico/hídrico
    STRESS_THRESHOLDS = {
        "temperature": {
            "low": 15,
            "high": 35
        },
        "humidity": {
            "low": 40,
            "high": 90
        }
    }

    # Prácticas regenerativas universales
    UNIVERSAL_PRACTICES = [
        "Rotación de cultivos",
        "Cobertura vegetal permanente",
        "Uso de abonos orgánicos",
        "No quema de residuos",
        "Siembra directa o mínima labranza"
    ]

    # Plagas y enfermedades comunes
    COMMON_PESTS = [
        {"name": "Gusano cogollero", "affects": ["maíz", "arroz"], "control": "Control biológico, trampas de feromonas"},
        {"name": "Mosca blanca", "affects": ["hortalizas", "frutales"], "control": "Aceites vegetales, enemigos naturales"},
        {"name": "Mildiu", "affects": ["yuca", "hortalizas"], "control": "Rotación, fungicidas orgánicos"}
    ]

    # Fertilización general
    FERTILIZATION_GUIDE = {
        "orgánica": {
            "description": "Uso de compost, estiércol, abonos verdes.",
            "benefits": ["Mejora la estructura del suelo", "Aumenta la biodiversidad microbiana"]
        },
        "química": {
            "description": "Uso racional de NPK y micronutrientes.",
            "recommendations": [
                "Aplicar según análisis de suelo",
                "Evitar sobredosificación"
            ]
        }
    }

    # Manejo de malezas
    WEED_MANAGEMENT = {
        "manual": "Deshierbe a mano o con herramientas simples, ideal en cultivos pequeños o ecológicos.",
        "mecánico": "Uso de maquinaria ligera para control de malezas en grandes extensiones.",
        "cobertura": "Uso de cultivos de cobertura o mulching para suprimir malezas.",
        "biológico": "Uso de extractos vegetales o enemigos naturales."
    }

    # Manejo de residuos
    RESIDUE_MANAGEMENT = [
        "Compostaje de residuos vegetales",
        "Incorporación de rastrojos al suelo",
        "Producción de biofertilizantes",
        "Evitar la quema de residuos"
    ]

    # Métodos de riego
    IRRIGATION_METHODS = {
        "gravedad": "Riego por surcos o canales, tradicional pero menos eficiente.",
        "aspersión": "Distribución uniforme, adecuado para hortalizas y pastos.",
        "goteo": "Alta eficiencia, ideal para frutales y cultivos de alto valor."
    }

    @classmethod
    def get_soil_info(cls, soil_type: str) -> Dict[str, Any]:
        """Devuelve información sobre un tipo de suelo"""
        return cls.SOIL_TYPES.get(soil_type.lower(), {})

    @classmethod
    def get_water_requirement_desc(cls, level: str) -> str:
        """Devuelve la descripción del requerimiento hídrico"""
        return cls.GENERAL_WATER_REQUIREMENTS.get(level.lower(), "")

    @classmethod
    def get_universal_practices(cls) -> List[str]:
        """Devuelve prácticas regenerativas universales"""
        return cls.UNIVERSAL_PRACTICES

    @classmethod
    def get_common_pests(cls, crop: Optional[str] = None) -> List[Dict[str, Any]]:
        """Devuelve plagas comunes, filtrando por cultivo si se indica"""
        if crop:
            return [p for p in cls.COMMON_PESTS if crop.lower() in [c.lower() for c in p["affects"]]]
        return cls.COMMON_PESTS

    @classmethod
    def get_stress_thresholds(cls) -> Dict[str, Any]:
        """Devuelve los umbrales de estrés térmico/hídrico"""
        return cls.STRESS_THRESHOLDS

    @classmethod
    def get_fertilization_guide(cls, type_: str) -> Dict[str, Any]:
        """Devuelve guía de fertilización por tipo"""
        return cls.FERTILIZATION_GUIDE.get(type_.lower(), {})

    @classmethod
    def get_weed_management_methods(cls) -> Dict[str, str]:
        """Devuelve métodos de manejo de malezas"""
        return cls.WEED_MANAGEMENT

    @classmethod
    def get_residue_management(cls) -> List[str]:
        """Devuelve prácticas de manejo de residuos"""
        return cls.RESIDUE_MANAGEMENT

    @classmethod
    def get_irrigation_methods(cls) -> Dict[str, str]:
        """Devuelve métodos de riego"""
        return cls.IRRIGATION_METHODS
