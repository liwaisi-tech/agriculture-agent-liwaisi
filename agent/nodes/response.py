"""
Nodo de generación de respuestas del agente de agricultura regenerativa
"""
from typing import Dict, Any
import logging
from agent.core.state import AgricultureState
from agent.tools import AVAILABLE_TOOLS
from utils.date_parser import DateParser

logger = logging.getLogger(__name__)


def generate_final_response(state: AgricultureState) -> AgricultureState:
    """
    Genera la respuesta final basada en toda la información recopilada
    """
    try:
        # Crear diccionario de herramientas
        tools = {tool.name: tool for tool in AVAILABLE_TOOLS}
        
        response = None
        query_type = state["query_type"]
        user_query = state["user_query"]
        
        if query_type == "current_status":
            response = _generate_status_response(state)
        elif query_type == "climate_history":
            response = _generate_history_response(state)
        elif query_type == "recommendations":
            response = _generate_recommendations_response(state)
        elif query_type == "crop_advice":
            response = _generate_crop_advice_response(state)
        else:
            response = _generate_general_response(state)
        
        # Si el usuario pidió información general
        if state.get("general_info_requested"):
            tool = tools["get_general_agriculture_info"]
            info = tool._run(category=state.get("general_info_category", ""), value=None)
            response += f"\n\nℹ️ **Información agrícola solicitada:**\n{info}"
        
        # Si el agente detectó riesgo y debe sugerir información
        if state.get("suggest_general_info"):
            tool = tools["get_general_agriculture_info"]
            info = tool._run(category=state.get("suggested_category", "umbrales"), value=None)
            response += f"\n\n⚠️ **Sugerencia técnica:**\n{info}"
        
        state["final_answer"] = response
        state["confidence"] = 0.9  # Alta confianza si llegamos aquí
        state["processing_steps"].append("final_response_generated")
        
    except Exception as e:
        logger.error(f"Error generando respuesta final: {e}")
        state["error_message"] = f"Error generando respuesta final: {str(e)}"
        state["final_answer"] = "Lo siento, hubo un error procesando tu consulta. Por favor, intenta de nuevo."
    
    return state


def _generate_status_response(state: AgricultureState) -> str:
    """Genera respuesta para estado actual"""
    response = "🌤️ **Estado Climático Actual:**\n\n"
    
    if state["sensor_data"]:
        response += "📊 **Lecturas de sensores:**\n"
        response += "   • Datos de sensores disponibles\n"
    else:
        response += "⚠️ No hay datos de sensores disponibles en este momento.\n"
    
    if state["climate_summary"]:
        response += "\n🔬 **Resumen climático:**\n"
        response += _format_climate_analysis(state["climate_summary"])
        response += "\n"
    
    if state["recommendations"]:
        response += "\n💡 **Recomendaciones:**\n"
        for rec in state["recommendations"][:3]:
            response += f"   • {rec}\n"
    
    return response


def _generate_history_response(state: AgricultureState) -> str:
    """Genera respuesta para análisis histórico"""
    response = "📈 **Análisis Histórico:**\n\n"
    
    if state["time_period"]:
        period_str = DateParser.format_date_range(
            state["time_period"]["start"], 
            state["time_period"]["end"]
        )
        response += f"📅 **Período analizado:** {period_str}\n\n"
    
    if state["climate_summary"]:
        response += "🔬 **Resumen climático:**\n"
        response += _format_climate_analysis(state["climate_summary"])
        response += "\n"
    
    return response


def _generate_recommendations_response(state: AgricultureState) -> str:
    """Genera respuesta para recomendaciones"""
    response = "💡 **Recomendaciones Agrícolas:**\n\n"
    
    if state["season_info"]:
        season_name = state["season_info"].get("characteristics", "actual")
        response += f"🌤️ **Temporada actual:** {season_name}\n\n"
    
    if state["recommendations"]:
        response += "📋 **Recomendaciones:**\n"
        for rec in state["recommendations"]:
            response += f"   • {rec}\n"
    else:
        response += "No hay recomendaciones específicas disponibles en este momento.\n"
    
    return response


def _generate_crop_advice_response(state: AgricultureState) -> str:
    """Genera respuesta para consejos de cultivos"""
    response = "🌱 **Consejos de Cultivo:**\n\n"
    
    if state["crop_mentioned"] and state["crop_requirements"]:
        crop_name = state["crop_requirements"]["name"]
        response += f"📖 **Información de {crop_name}:**\n"
        
        # Condiciones óptimas
        temp_range = state["crop_requirements"]["optimal_temperature"]
        hum_range = state["crop_requirements"]["optimal_humidity"]
        
        response += f"   • Temperatura óptima: {temp_range['min']}-{temp_range['max']}°C\n"
        response += f"   • Humedad óptima: {hum_range['min']}-{hum_range['max']}%\n"
        response += f"   • Período de crecimiento: {state['crop_requirements']['growth_period_days']} días\n\n"
    
    if state["recommendations"]:
        response += "♻️ **Prácticas regenerativas:**\n"
        for rec in state["recommendations"]:
            response += f"   • {rec}\n"
    
    return response


def _generate_general_response(state: AgricultureState) -> str:
    """Genera respuesta general"""
    response = "🤖 **Asistente de Agricultura Regenerativa:**\n\n"
    response += "¡Hola! Soy tu asistente de agricultura regenerativa para Casanare.\n\n"
    response += "Puedo ayudarte con:\n"
    response += "   • 📊 Estado actual del clima\n"
    response += "   • 📈 Análisis histórico de datos\n"
    response += "   • 🌱 Información de cultivos\n"
    response += "   • 💡 Recomendaciones agrícolas\n"
    response += "   • 📅 Consejos estacionales\n\n"
    response += "¿En qué puedo ayudarte hoy?"
    
    return response


def _format_climate_analysis(analysis: Dict[str, Any]) -> str:
    """Formatea el análisis climático para mostrar en la respuesta"""
    lines = []
    
    # Estadísticas básicas
    basic = analysis.get('basic_stats', {})
    if basic:
        for metric in ['temperature', 'humidity']:
            stats = basic.get(metric, {})
            if 'mean' in stats:
                lines.append(f"• {metric.title()}: Promedio {stats['mean']:.1f}, Mín {stats['min']:.1f}, Máx {stats['max']:.1f}, Desv. {stats['std']:.1f}")
    
    # Tendencias
    trends = analysis.get('trends', {})
    for metric in ['temperature', 'humidity']:
        t = trends.get(metric, {})
        if 'trend_direction' in t:
            lines.append(f"• Tendencia de {metric}: {t['trend_direction']} (R²={t['r_squared']:.2f})")
    
    # Extremos
    extremes = analysis.get('extremes', {})
    for metric in ['temperature', 'humidity']:
        e = extremes.get(metric, {})
        if 'extreme_events' in e:
            lines.append(f"• Eventos extremos de {metric}: Altos {e['extreme_events']['high_count']}, Bajos {e['extreme_events']['low_count']}")
    
    # Cultivos recomendados
    ag = analysis.get('agricultural_analysis', {})
    if 'suitable_crops' in ag and ag['suitable_crops']:
        crops = ', '.join([c['name'] for c in ag['suitable_crops'][:3]])
        lines.append(f"• Cultivos recomendados: {crops}")
    
    # Calidad de datos
    dq = analysis.get('data_quality', {})
    if dq:
        lines.append(f"• Calidad de datos: {dq.get('quality', 'desconocida')}")
        if dq.get('issues'):
            lines.append(f"  Problemas: {', '.join(dq['issues'])}")
    
    return '\n'.join(lines) 