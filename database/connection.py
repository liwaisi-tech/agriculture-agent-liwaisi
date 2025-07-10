"""
Conexión a la base de datos PostgreSQL
"""
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class DatabaseConnection:
    """Maneja la conexión a PostgreSQL"""
    
    def __init__(self):
        self.host = os.getenv('DB_HOST')
        self.port = os.getenv('DB_PORT', '5432')
        self.database = os.getenv('DB_NAME')
        self.user = os.getenv('DB_USER')
        self.password = os.getenv('DB_PASSWORD')
        
        if not all([self.host, self.database, self.user, self.password]):
            raise ValueError("Faltan variables de entorno de la base de datos")
    
    @contextmanager
    def get_connection(self):
        """Context manager para conexión a BD"""
        conn = None
        try:
            conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password,
                cursor_factory=RealDictCursor
            )
            yield conn
        except psycopg2.Error as e:
            logger.error(f"Error de conexión a BD: {e}")
            if conn:
                conn.rollback()
            raise
        finally:
            if conn:
                conn.close()
    
    def execute_query(self, query: str, params: Optional[tuple] = None) -> List[Dict[str, Any]]:
        """Ejecuta una consulta SELECT"""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, params)
                    results = cursor.fetchall()
                    return [dict(row) for row in results]
        except Exception as e:
            logger.error(f"Error ejecutando query: {e}")
            logger.error(f"Query: {query}")
            logger.error(f"Params: {params}")
            return []
    
    def execute_insert(self, query: str, params: Optional[tuple] = None) -> bool:
        """Ejecuta una consulta INSERT/UPDATE/DELETE"""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, params)
                    conn.commit()
                    return True
        except Exception as e:
            logger.error(f"Error ejecutando insert: {e}")
            return False
    
    def test_connection(self) -> bool:
        """Prueba la conexión a la BD"""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT 1")
                    result = cursor.fetchone()
                    return result is not None
        except Exception as e:
            logger.error(f"Error probando conexión: {e}")
            return False


# Instancia global
db = DatabaseConnection()