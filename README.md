# 🌱 Agente de Agricultura Regenerativa para Casanare

Un agente inteligente basado en LangGraph que proporciona asistencia especializada en agricultura regenerativa para la región de Casanare, Colombia.

## 🎯 Características Principales

- **📊 Análisis Climático**: Procesamiento de datos de sensores de temperatura y humedad
- **🌱 Información de Cultivos**: Base de conocimiento específica para cultivos de Casanare
- **💡 Recomendaciones Agrícolas**: Consejos basados en condiciones climáticas actuales
- **📅 Calendario Agrícola**: Guía estacional para prácticas agrícolas
- **🔍 Parser de Fechas**: Interpretación de expresiones de tiempo en español
- **📈 Análisis Histórico**: Evaluación de tendencias climáticas

## 🏗️ Arquitectura

El proyecto utiliza una arquitectura basada en **LangGraph** con los siguientes componentes:

```
agriculture-agent/
├── agent/           # Núcleo del agente
│   ├── core/        # Componentes principales
│   ├── nodes/       # Nodos del grafo
│   └── tools/       # Herramientas del agente
├── utils/           # Utilidades
├── knowledge/       # Base de conocimiento
├── database/        # Capa de datos
├── tests/           # Tests
├── main.py          # Punto de entrada
├── requirements.txt # Dependencias
├── README.md        # Documentación
├── .gitignore       # Configuración Git
├── env.example      # Variables de entorno
└── venv/            # Entorno virtual (ignorado por Git)
```

## 🚀 Instalación

### Prerrequisitos

- Python 3.8+
- PostgreSQL (opcional, para datos de sensores)
- API Key de OpenAI

### Instalación

1. **Clonar el repositorio**:
```bash
git clone <repository-url>
cd agriculture-agent
```

2. **Crear entorno virtual**:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias**:
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**:
```bash
cp env.example .env
# Editar .env con tus credenciales
```

Variables de entorno requeridas:
```env
OPENAI_API_KEY=tu_api_key_aqui
DB_HOST=localhost
DB_PORT=5432
DB_NAME=agriculture_db
DB_USER=usuario
DB_PASSWORD=contraseña
```

## 🎮 Uso

### Modo Interactivo

```bash
python main.py
```

### Consulta Única

```bash
python main.py -q "¿Cómo está el clima hoy?"
```

### Modo Batch

```bash
python main.py -f consultas.txt
```

### Información del Sistema

```bash
python main.py --info
```

### Modo Debug

```bash
python main.py --debug
```

## 📋 Ejemplos de Consultas

### Estado Climático Actual
```
¿Cómo está el clima hoy?
¿Cuál es la temperatura actual?
¿Qué humedad hay en los sensores?
```

### Análisis Histórico
```
¿Cómo estuvo el clima la semana pasada?
¿Cuál fue la temperatura promedio del mes pasado?
Análisis climático de los últimos 7 días
```

### Información de Cultivos
```
¿Qué necesito saber sobre el cultivo de arroz?
Información sobre el maíz
¿Cómo cultivar yuca en Casanare?
```

### Recomendaciones Agrícolas
```
¿Qué puedo sembrar ahora?
Recomendaciones para esta temporada
¿Qué cultivos son mejores para el clima actual?
```

## 🔧 Componentes Principales

### 1. Date Parser (`utils/date_parser.py`)

Interpreta expresiones de tiempo en español:
- "ayer", "hoy", "mañana"
- "última semana", "próximo mes"
- "15 de marzo", "2024-03-15"
- Temporadas agrícolas

### 2. Climate Analyzer (`utils/climate_analyzer.py`)

Analiza datos climáticos y genera insights:
- Estadísticas básicas (promedio, min, max)
- Análisis de tendencias
- Detección de eventos extremos
- Evaluación de condiciones agrícolas
- Recomendaciones basadas en datos

### 3. Tools (`agent/tools/`)

Herramientas modulares del agente:
- `current_readings.py`: Lecturas actuales de sensores
- `historical_data.py`: Datos históricos
- `analyze_climate.py`: Análisis climático detallado
- `crop_info.py`: Información de cultivos
- `seasonal_recommendations.py`: Recomendaciones estacionales
- `general_agriculture_info.py`: Información agrícola general

### 4. Nodes (`agent/nodes/`)

Nodos modulares del grafo de procesamiento:
- `classify.py`: Clasifica el tipo de consulta
- `fetch_sensor.py`: Obtiene datos de sensores
- `analyze.py`: Analiza datos climáticos
- `recommendations.py`: Genera recomendaciones
- `response.py`: Construye respuesta final
- `control.py`: Control de flujo y manejo de errores

### 5. Core (`agent/core/`)

Componentes principales del agente:
- `state.py`: Estado compartido del grafo
- `graph.py`: Construcción y gestión del grafo de flujo

### 6. Graph (`agent/core/graph.py`)

Define el flujo del agente:
```
classify_query → fetch_sensor_data → analyze_climate_data → get_crop_recommendations → generate_final_response
```

## 🌾 Base de Conocimiento

### Cultivos Soportados

- **Arroz**: Cultivo principal de los llanos
- **Maíz**: Excelente adaptación al clima llanero
- **Yuca**: Muy resistente a sequías
- **Plátano**: Requiere zonas protegidas del viento
- **Cacao**: Ideal en zonas de galería
- **Cítricos**: Naranjas y limones

### Temporadas Agrícolas

1. **Época Seca** (Dic-Mar): Baja precipitación, temperaturas altas
2. **Inicio de Lluvias** (Abr-May): Incremento de precipitaciones
3. **Época Lluviosa** (Jun-Oct): Alta precipitación y humedad
4. **Transición** (Nov): Disminución gradual de lluvias

## 🗄️ Base de Datos

### Esquema de Sensores

```sql
-- Tabla de sensores
CREATE TABLE sensors (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    type VARCHAR(50),
    location_description TEXT,
    latitude DECIMAL(10,8),
    longitude DECIMAL(11,8),
    installation_date DATE,
    is_active BOOLEAN DEFAULT TRUE
);

-- Tabla de lecturas
CREATE TABLE sensor_readings (
    id SERIAL PRIMARY KEY,
    sensor_id INTEGER REFERENCES sensors(id),
    timestamp TIMESTAMP,
    temperature DECIMAL(5,2),
    humidity DECIMAL(5,2),
    location VARCHAR(100)
);
```

## 🧪 Testing

```bash
# Ejecutar tests
pytest tests/

# Con cobertura
pytest --cov=src/agriculture_agent tests/
```

## 📊 Logging

El sistema genera logs en:
- `agriculture_agent.log`: Archivo de log principal
- Consola: Output en tiempo real

Niveles de log:
- `INFO`: Operaciones normales
- `WARNING`: Advertencias
- `ERROR`: Errores
- `DEBUG`: Información detallada (con `--debug`)

## 🔄 Flujo de Procesamiento

1. **Clasificación**: El agente clasifica el tipo de consulta
2. **Obtención de Datos**: Recupera datos relevantes de sensores
3. **Análisis**: Procesa y analiza los datos climáticos
4. **Recomendaciones**: Genera consejos específicos
5. **Respuesta**: Construye la respuesta final

## 🛠️ Desarrollo

### Estructura de Desarrollo

```bash
# Formatear código
black src/ tests/

# Linting
flake8 src/ tests/

# Type checking
mypy src/
```

### Agregar Nuevos Cultivos

1. Editar `knowledge/casanare_crops.py`
2. Agregar datos del cultivo en `CROPS_DATA`
3. Actualizar patrones de reconocimiento en `nodes.py`

### Agregar Nuevas Herramientas

1. Crear clase en `tools.py`
2. Heredar de `BaseTool`
3. Implementar método `_run`
4. Agregar a `AVAILABLE_TOOLS`

## 🤝 Contribución

1. Fork el proyecto
2. Crear rama feature (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 📞 Soporte

Para soporte técnico o preguntas:
- Crear un issue en GitHub
- Contactar al equipo de desarrollo

## 🗺️ Roadmap

- [ ] Integración con APIs meteorológicas
- [ ] Predicciones climáticas
- [ ] Interfaz web
- [ ] Notificaciones automáticas
- [ ] Análisis de suelos
- [ ] Integración con IoT

---

**Desarrollado con ❤️ para la agricultura regenerativa de Casanare** 