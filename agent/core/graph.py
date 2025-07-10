"""
Construcción del grafo del agente de agricultura regenerativa
"""
from typing import Dict, Any, List
import logging
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI

from agent.core.state import AgricultureState, create_initial_state
from agent.nodes import classify_query, fetch_sensor_data, analyze_climate_data, get_crop_recommendations, generate_final_response, handle_error

logger = logging.getLogger(__name__)


class AgricultureGraph:
    """Grafo del agente de agricultura regenerativa"""
    
    def __init__(self, llm: ChatOpenAI):
        self.llm = llm
        # Los nodos ahora son funciones importadas directamente
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """
        Construye el grafo de flujo del agente
        """
        workflow = StateGraph(AgricultureState)
        
        # Agregar nodos
        workflow.add_node("classify_query", classify_query)
        workflow.add_node("fetch_sensor_data", fetch_sensor_data)
        workflow.add_node("analyze_climate_data", analyze_climate_data)
        workflow.add_node("get_crop_recommendations", get_crop_recommendations)
        workflow.add_node("generate_final_response", generate_final_response)
        workflow.add_node("handle_error", handle_error)
        
        # Definir el punto de entrada
        workflow.set_entry_point("classify_query")
        
        # Definir las transiciones condicionales
        workflow.add_conditional_edges(
            "classify_query",
            self._route_after_classification,
            {
                "fetch_data": "fetch_sensor_data",
                "crop_advice": "get_crop_recommendations",
                "recommendations": "get_crop_recommendations",
                "error": "handle_error",
                "end": END
            }
        )
        
        workflow.add_conditional_edges(
            "fetch_sensor_data",
            self._route_after_fetch_data,
            {
                "analyze": "analyze_climate_data",
                "crop_advice": "get_crop_recommendations",
                "recommendations": "get_crop_recommendations",
                "error": "handle_error",
                "end": END
            }
        )
        
        workflow.add_conditional_edges(
            "analyze_climate_data",
            self._route_after_analysis,
            {
                "crop_advice": "get_crop_recommendations",
                "recommendations": "get_crop_recommendations",
                "generate_response": "generate_final_response",
                "error": "handle_error",
                "end": END
            }
        )
        
        workflow.add_conditional_edges(
            "get_crop_recommendations",
            self._route_after_crop_recommendations,
            {
                "generate_response": "generate_final_response",
                "error": "handle_error",
                "end": END
            }
        )
        
        workflow.add_conditional_edges(
            "generate_final_response",
            self._route_after_final_response,
            {
                "end": END,
                "error": "handle_error"
            }
        )
        
        workflow.add_conditional_edges(
            "handle_error",
            lambda state: "end",
            {
                "end": END
            }
        )
        
        return workflow.compile()
    
    def _route_after_classification(self, state: AgricultureState) -> str:
        try:
            if state.get("error_message"):
                return "error"
            query_type = state.get("query_type", "")
            if query_type in ["current_status", "climate_history"]:
                return "fetch_data"
            elif query_type == "crop_advice":
                return "crop_advice"
            elif query_type == "recommendations":
                return "recommendations"
            else:
                return "end"
        except Exception as e:
            logger.error(f"Error en routing después de clasificación: {e}")
            return "error"
    
    def _route_after_fetch_data(self, state: AgricultureState) -> str:
        try:
            if state.get("error_message"):
                return "error"
            query_type = state.get("query_type", "")
            if state.get("sensor_data"):
                return "analyze"
            elif query_type == "crop_advice":
                return "crop_advice"
            elif query_type == "recommendations":
                return "recommendations"
            else:
                return "end"
        except Exception as e:
            logger.error(f"Error en routing después de obtener datos: {e}")
            return "error"
    
    def _route_after_analysis(self, state: AgricultureState) -> str:
        try:
            if state.get("error_message"):
                return "error"
            query_type = state.get("query_type", "")
            if query_type == "crop_advice":
                return "crop_advice"
            elif query_type == "recommendations":
                return "recommendations"
            else:
                return "generate_response"
        except Exception as e:
            logger.error(f"Error en routing después de análisis: {e}")
            return "error"
    
    def _route_after_crop_recommendations(self, state: AgricultureState) -> str:
        try:
            if state.get("error_message"):
                return "error"
            return "generate_response"
        except Exception as e:
            logger.error(f"Error en routing después de recomendaciones de cultivos: {e}")
            return "error"
    
    def _route_after_final_response(self, state: AgricultureState) -> str:
        try:
            if state.get("error_message"):
                return "error"
            if state.get("final_answer"):
                return "end"
            return "error"
        except Exception as e:
            logger.error(f"Error en routing después de respuesta final: {e}")
            return "error"
    
    def process_query(self, user_query: str) -> Dict[str, Any]:
        try:
            initial_state = create_initial_state(user_query)
            result = self.graph.invoke(initial_state)
            response = {
                "answer": result.get("final_answer", "No se pudo generar una respuesta."),
                "confidence": result.get("confidence", 0.0),
                "query_type": result.get("query_type", "unknown"),
                "processing_steps": result.get("processing_steps", []),
                "error_message": result.get("error_message"),
                "timestamp": result.get("timestamp"),
                "metadata": {
                    "time_period": result.get("time_period"),
                    "crop_mentioned": result.get("crop_mentioned"),
                    "location_mentioned": result.get("location_mentioned"),
                    "has_sensor_data": len(result.get("sensor_data", [])) > 0,
                    "has_climate_analysis": bool(result.get("climate_summary")),
                    "recommendations_count": len(result.get("recommendations", []))
                }
            }
            logger.info(f"Consulta procesada exitosamente. Tipo: {response['query_type']}, Confianza: {response['confidence']}")
            return response
        except Exception as e:
            logger.error(f"Error procesando consulta: {e}")
            return {
                "answer": "Lo siento, hubo un error procesando tu consulta. Por favor, intenta de nuevo.",
                "confidence": 0.0,
                "query_type": "error",
                "processing_steps": [],
                "error_message": str(e),
                "timestamp": None,
                "metadata": {}
            }
    
    def get_graph_info(self) -> Dict[str, Any]:
        return {
            "nodes": [
                "classify_query",
                "fetch_sensor_data", 
                "analyze_climate_data",
                "get_crop_recommendations",
                "generate_final_response",
                "handle_error"
            ],
            "entry_point": "classify_query",
            "exit_points": ["end"],
            "description": "Grafo de flujo para agente de agricultura regenerativa"
        }


def create_agriculture_graph(llm: ChatOpenAI) -> AgricultureGraph:
    """Crea una instancia del grafo de agricultura"""
    return AgricultureGraph(llm) 