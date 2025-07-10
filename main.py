#!/usr/bin/env python3
"""
Punto de entrada principal del agente de agricultura regenerativa
"""
import os
import sys
import logging
import argparse
from typing import Dict, Any
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from agent.core.graph import create_agriculture_graph
from database.connection import db

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('agriculture_agent.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


class AgricultureAgent:
    """Clase principal del agente de agricultura regenerativa"""
    
    def __init__(self):
        """Inicializa el agente"""
        # Cargar variables de entorno
        load_dotenv()
        
        # Verificar configuración
        self._check_configuration()
        
        # Inicializar LLM
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.1,
            api_key=os.getenv('OPENAI_API_KEY')
        )
        
        # Crear grafo del agente
        self.graph = create_agriculture_graph(self.llm)
        
        logger.info("Agente de agricultura regenerativa inicializado correctamente")
    
    def _check_configuration(self):
        """Verifica que la configuración sea correcta"""
        required_vars = ['OPENAI_API_KEY']
        missing_vars = []
        
        for var in required_vars:
            if not os.getenv(var):
                missing_vars.append(var)
        
        if missing_vars:
            raise ValueError(f"Faltan variables de entorno requeridas: {', '.join(missing_vars)}")
        
        # Verificar conexión a base de datos (opcional)
        try:
            if db.test_connection():
                logger.info("Conexión a base de datos establecida")
            else:
                logger.warning("No se pudo conectar a la base de datos")
        except Exception as e:
            logger.warning(f"No se pudo verificar la conexión a la base de datos: {e}")
    
    def process_query(self, query: str) -> Dict[str, Any]:
        """
        Procesa una consulta del usuario
        
        Args:
            query: Consulta del usuario
            
        Returns:
            Respuesta del agente
        """
        try:
            logger.info(f"Procesando consulta: {query}")
            
            # Procesar consulta a través del grafo
            result = self.graph.process_query(query)
            
            logger.info(f"Consulta procesada. Tipo: {result['query_type']}, Confianza: {result['confidence']}")
            
            return result
            
        except Exception as e:
            logger.error(f"Error procesando consulta: {e}")
            return {
                "answer": f"Error interno del agente: {str(e)}",
                "confidence": 0.0,
                "query_type": "error",
                "error_message": str(e)
            }
    
    def interactive_mode(self):
        """Modo interactivo de línea de comandos"""
        print("🌱 **Asistente de Agricultura Regenerativa para Casanare**")
        print("=" * 60)
        print("¡Hola! Soy tu asistente de agricultura regenerativa.")
        print("Puedo ayudarte con:")
        print("  • 📊 Estado actual del clima")
        print("  • 📈 Análisis histórico de datos")
        print("  • 🌱 Información de cultivos")
        print("  • 💡 Recomendaciones agrícolas")
        print("  • 📅 Consejos estacionales")
        print("\nEscribe 'salir' para terminar.")
        print("=" * 60)
        
        while True:
            try:
                # Obtener consulta del usuario
                query = input("\n🤔 ¿En qué puedo ayudarte? ").strip()
                
                if query.lower() in ['salir', 'exit', 'quit']:
                    print("👋 ¡Hasta luego! Que tengas éxito en tu agricultura regenerativa.")
                    break
                
                if not query:
                    print("Por favor, ingresa una consulta.")
                    continue
                
                # Procesar consulta
                print("\n🔄 Procesando...")
                result = self.process_query(query)
                
                # Mostrar respuesta
                print("\n" + "=" * 60)
                print(result['answer'])
                print("=" * 60)
                
                # Mostrar metadata si está en modo debug
                if os.getenv('DEBUG', 'false').lower() == 'true':
                    print(f"\n📊 Metadata:")
                    print(f"  • Tipo de consulta: {result['query_type']}")
                    print(f"  • Confianza: {result['confidence']:.2f}")
                    print(f"  • Pasos de procesamiento: {len(result.get('processing_steps', []))}")
                    if result.get('metadata'):
                        meta = result['metadata']
                        print(f"  • Período de tiempo: {meta.get('time_period')}")
                        print(f"  • Cultivo mencionado: {meta.get('crop_mentioned')}")
                        print(f"  • Ubicación: {meta.get('location_mentioned')}")
                
            except KeyboardInterrupt:
                print("\n\n👋 ¡Hasta luego! Que tengas éxito en tu agricultura regenerativa.")
                break
            except Exception as e:
                logger.error(f"Error en modo interactivo: {e}")
                print(f"❌ Error: {str(e)}")
    
    def batch_mode(self, queries: list):
        """Modo batch para procesar múltiples consultas"""
        print(f"🔄 Procesando {len(queries)} consultas en modo batch...")
        
        results = []
        for i, query in enumerate(queries, 1):
            print(f"\n[{i}/{len(queries)}] Procesando: {query}")
            result = self.process_query(query)
            results.append({
                "query": query,
                "result": result
            })
            
            # Mostrar respuesta resumida
            print(f"   Tipo: {result['query_type']}, Confianza: {result['confidence']:.2f}")
        
        return results
    
    def get_system_info(self) -> Dict[str, Any]:
        """Obtiene información del sistema"""
        return {
            "agent_version": "1.0.0",
            "graph_info": self.graph.get_graph_info(),
            "database_connected": db.test_connection() if hasattr(db, 'test_connection') else False,
            "llm_model": self.llm.model_name if hasattr(self.llm, 'model_name') else "unknown"
        }


def main():
    """Función principal"""
    parser = argparse.ArgumentParser(
        description="Agente de Agricultura Regenerativa para Casanare",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python main.py                    # Modo interactivo
  python main.py -q "¿Cómo está el clima hoy?"  # Consulta única
  python main.py -f queries.txt     # Modo batch desde archivo
  python main.py --info             # Información del sistema
        """
    )
    
    parser.add_argument(
        '-q', '--query',
        type=str,
        help='Consulta única para procesar'
    )
    
    parser.add_argument(
        '-f', '--file',
        type=str,
        help='Archivo con consultas para procesar en modo batch'
    )
    
    parser.add_argument(
        '--info',
        action='store_true',
        help='Mostrar información del sistema'
    )
    
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Habilitar modo debug'
    )
    
    args = parser.parse_args()
    
    # Configurar debug si se solicita
    if args.debug:
        os.environ['DEBUG'] = 'true'
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        # Inicializar agente
        agent = AgricultureAgent()
        
        # Mostrar información del sistema si se solicita
        if args.info:
            info = agent.get_system_info()
            print("🔧 **Información del Sistema:**")
            print(f"  • Versión del agente: {info['agent_version']}")
            print(f"  • Modelo LLM: {info['llm_model']}")
            print(f"  • Base de datos conectada: {info['database_connected']}")
            print(f"  • Nodos del grafo: {', '.join(info['graph_info']['nodes'])}")
            return
        
        # Procesar consulta única
        if args.query:
            result = agent.process_query(args.query)
            print("\n" + "=" * 60)
            print(result['answer'])
            print("=" * 60)
            
            if args.debug:
                print(f"\n📊 Debug info:")
                print(f"  • Tipo: {result['query_type']}")
                print(f"  • Confianza: {result['confidence']:.2f}")
                print(f"  • Pasos: {result.get('processing_steps', [])}")
        
        # Procesar archivo de consultas
        elif args.file:
            if not os.path.exists(args.file):
                print(f"❌ Error: El archivo '{args.file}' no existe.")
                return
            
            with open(args.file, 'r', encoding='utf-8') as f:
                queries = [line.strip() for line in f if line.strip()]
            
            if not queries:
                print("❌ Error: El archivo no contiene consultas válidas.")
                return
            
            results = agent.batch_mode(queries)
            
            # Guardar resultados
            output_file = f"results_{os.path.basename(args.file)}"
            with open(output_file, 'w', encoding='utf-8') as f:
                for item in results:
                    f.write(f"Consulta: {item['query']}\n")
                    f.write(f"Respuesta: {item['result']['answer']}\n")
                    f.write(f"Tipo: {item['result']['query_type']}\n")
                    f.write(f"Confianza: {item['result']['confidence']:.2f}\n")
                    f.write("-" * 50 + "\n")
            
            print(f"\n✅ Resultados guardados en: {output_file}")
        
        # Modo interactivo por defecto
        else:
            agent.interactive_mode()
    
    except KeyboardInterrupt:
        print("\n\n👋 ¡Hasta luego!")
    except Exception as e:
        logger.error(f"Error en la aplicación principal: {e}")
        print(f"❌ Error fatal: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
