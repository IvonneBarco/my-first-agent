# Documentación Técnica del Proyecto - LangGraph Multi-Agent System

## 📋 Tabla de Contenidos

1. [Visión General](#visión-general)
2. [Arquitectura del Proyecto](#arquitectura-del-proyecto)
3. [Estructura de Directorios](#estructura-de-directorios)
4. [Patrones y Buenas Prácticas](#patrones-y-buenas-prácticas)
5. [Guía de Creación de Agentes](#guía-de-creación-de-agentes)
6. [Migración a Arquitectura Limpia](#migración-a-arquitectura-limpia)
7. [Herramientas y Tecnologías](#herramientas-y-tecnologías)
8. [Guía de Inicio Rápido](#guía-de-inicio-rápido)

---

## 🎯 Visión General

Este proyecto implementa un sistema multi-agente utilizando **LangGraph**, siguiendo principios de arquitectura limpia y modularidad. El sistema está diseñado para ser escalable, mantenible y fácil de extender con nuevos agentes y funcionalidades.

### Principios Fundamentales

- **Separación de Responsabilidades**: Cada agente tiene una función específica
- **Modularidad**: Componentes independientes y reutilizables
- **Configuración Centralizada**: Gestión unificada de agentes en `langgraph.json`
- **Estado Tipado**: Uso de Pydantic para validación de datos
- **Escalabilidad Horizontal**: Fácil adición de nuevos agentes

---

## 🏗️ Arquitectura del Proyecto

### Diagrama de Arquitectura

```
┌─────────────────────────────────────────────────────────────┐
│                     langgraph.json                          │
│            (Configuración Central de Grafos)                │
└──────────────────────┬──────────────────────────────────────┘
                       │
       ┌───────────────┼───────────────┬──────────────┐
       │               │               │              │
       ▼               ▼               ▼              ▼
   ┌──────┐      ┌──────────┐    ┌────────┐    ┌─────────┐
   │Agent │      │  Simple  │    │  RAG   │    │Support  │
   └──────┘      └──────────┘    └────────┘    └─────────┘
                                                      │
                      ┌───────────────────────────────┼─────────────┐
                      │                               │             │
                      ▼                               ▼             ▼
              ┌──────────────┐              ┌──────────────┐  ┌─────────┐
              │  Extractor   │              │ Conversation │  │Vendedor │
              │  (Node)      │              │   (Node)     │  │ (Node)  │
              └──────────────┘              └──────────────┘  └─────────┘
                      │                               │             │
        ┌─────────────┼──────────────┐   ┌───────────┼──────┐      │
        ▼             ▼              ▼   ▼           ▼      ▼      ▼
    [State]      [Prompt]       [Schema] [Tools]  [Prompt] [LLM] [Tools]
```

### Capas de la Arquitectura

#### 1. **Capa de Configuración** (`langgraph.json`)
```json
{
    "dependencies": ["."],
    "graphs": {
        "agent": "./src/agents/main.py:agent",
        "simple": "./src/agents/simple.py:agent",
        "rag": "./src/agents/rag.py:agent",
        "support": "./src/agents/support/agent.py:agent",
        "booking": "./src/agents/support/nodes/booking/node.py:booking_node"
    },
    "env": ".env"
}
```

**Propósito**: Registro centralizado de todos los grafos disponibles en el sistema.

#### 2. **Capa de Agentes** (`src/agents/`)
Contiene los agentes principales del sistema:
- **main.py**: Agente principal
- **simple.py**: Agente simple para casos básicos
- **rag.py**: Agente con Retrieval Augmented Generation
- **support/**: Agente complejo con múltiples nodos

#### 3. **Capa de Nodos** (`src/agents/*/nodes/`)
Componentes especializados dentro de cada agente:
- **extractor**: Extracción de información estructurada
- **conversation**: Gestión de conversaciones
- **vendedor**: Agente de ventas con herramientas
- **booking**: Agente de reservas (placeholder)

#### 4. **Capa de Componentes**
Cada nodo contiene:
- `node.py`: Lógica principal del nodo
- `tools.py`: Herramientas disponibles
- `prompt.py`: Plantillas de prompts
- `__init__.py`: Exportaciones públicas

---

## 📁 Estructura de Directorios

```
my-first-agent/
├── langgraph.json              # Configuración de grafos
├── pyproject.toml              # Dependencias del proyecto
├── .env                        # Variables de entorno
├── README.md                   # Documentación general
├── ARCHITECTURE.md             # Este archivo
│
├── notebooks/                  # Jupyter notebooks para experimentación
│   ├── 01-notebook.ipynb
│   ├── 05-rag.ipynb
│   └── 07-structured_output.ipynb
│
└── src/
    ├── __init__.py
    └── agents/                 # Agentes del sistema
        ├── __init__.py
        ├── main.py            # Agente principal
        ├── simple.py          # Agente simple
        ├── rag.py             # Agente RAG
        │
        └── support/           # Agente de soporte (complejo)
            ├── __init__.py
            ├── agent.py       # Configuración del grafo
            ├── state.py       # Definición de estado
            ├── routes/        # Rutas condicionales (vacío)
            │
            └── nodes/         # Nodos del agente
                ├── __init__.py
                │
                ├── extractor/           # Extracción de datos
                │   ├── __init__.py
                │   ├── node.py
                │   ├── prompt.py
                │   └── (schema definido en node.py)
                │
                ├── conversation/        # Gestión de conversación
                │   ├── __init__.py
                │   ├── node.py
                │   ├── prompt.py
                │   └── tools.py
                │
                ├── vendedor/           # Agente de ventas
                │   ├── __init__.py
                │   ├── node.py
                │   ├── prompt.py
                │   └── tools.py
                │
                └── booking/            # Agente de reservas
                    ├── __init__.py
                    ├── node.py
                    ├── prompt.py
                    └── tools.py
```

---

## 🎨 Patrones y Buenas Prácticas

### 1. **Patrón de Estado Tipado**

```python
from langgraph.graph import MessagesState
from typing import Annotated

class State(MessagesState):
    """Estado del agente con validación de tipos"""
    customer_name: str
    phone: str
    my_age: str
```

**Ventajas**:
- ✅ Validación automática de tipos
- ✅ Autocompletado en IDEs
- ✅ Documentación implícita
- ✅ Detección temprana de errores

### 2. **Patrón de Nodo Modular**

Cada nodo sigue esta estructura:

```python
# node.py
from agents.support.state import State
from agents.support.nodes.extractor.prompt import SYSTEM_PROMPT
from agents.support.nodes.extractor.tools import tools

def node_function(state: State) -> dict:
    """
    Función del nodo que procesa el estado
    
    Args:
        state: Estado actual del agente
        
    Returns:
        dict: Actualizaciones parciales del estado
    """
    # 1. Extraer información del estado
    history = state["messages"]
    
    # 2. Procesar lógica del nodo
    result = process_logic(history)
    
    # 3. Retornar actualizaciones parciales
    return {
        "messages": [result],
        "custom_field": value
    }
```

**Principios**:
- ✅ Una responsabilidad por nodo
- ✅ Estado inmutable (retornar nuevas actualizaciones)
- ✅ Dependencias explícitas
- ✅ Funciones puras cuando sea posible

### 3. **Patrón de Herramientas (Tools)**

```python
# tools.py
import requests
from langchain_core.tools import tool

@tool("get_products", description="Obtiene la lista de productos disponibles")
def get_products() -> str:
    """Obtiene productos desde la API"""
    response = requests.get("https://api.example.com/products")
    products = response.json()
    return "\n".join([f"{p['title']} - ${p['price']}" for p in products])

@tool("calculate_discount", description="Calcula descuentos según cantidad")
def calculate_discount(quantity: int, price: float) -> str:
    """Calcula el descuento aplicable"""
    discount = 0.15 if quantity >= 10 else 0.10 if quantity >= 5 else 0.0
    total = quantity * price * (1 - discount)
    return f"Total: ${total:.2f} (Descuento: {int(discount*100)}%)"

# Exportar lista de herramientas
tools = [get_products, calculate_discount]
```

**Buenas Prácticas**:
- ✅ Usar decorador `@tool` con descripción clara
- ✅ Docstrings descriptivos
- ✅ Validación de tipos en parámetros
- ✅ Manejo de errores explícito
- ✅ Retornar strings formateados para el LLM

### 4. **Patrón de Prompts**

```python
# prompt.py
from langchain_core.prompts import PromptTemplate
from datetime import date

template = """\
Eres un asistente profesional especializado en {specialty}.
Fecha actual: {today}

Instrucciones:
1. {instruction_1}
2. {instruction_2}
3. {instruction_3}

Herramientas disponibles:
{tools_description}

Reglas:
- {rule_1}
- {rule_2}
"""

today = date.today().strftime("%Y-%m-%d")

prompt_template = PromptTemplate.from_template(template)
SYSTEM_PROMPT = prompt_template.format(
    specialty="ventas",
    today=today,
    instruction_1="Saluda al cliente",
    instruction_2="Identifica necesidades",
    instruction_3="Ofrece soluciones",
    tools_description="- get_products\n- calculate_discount",
    rule_1="Sé profesional",
    rule_2="Usa las herramientas"
)
```

**Ventajas**:
- ✅ Prompts parametrizables
- ✅ Fácil actualización
- ✅ Reutilización de templates
- ✅ Separación de lógica y contenido

### 5. **Patrón de Extracción Estructurada**

```python
from pydantic import BaseModel, Field
from langchain.chat_models import init_chat_model

class ContactInfo(BaseModel):
    """Schema de información de contacto"""
    name: str = Field(description="Nombre completo")
    email: str = Field(description="Email válido")
    phone: str = Field(description="Teléfono")
    age: int = Field(description="Edad", ge=0, le=150)

llm = init_chat_model("openai:gpt-4o", temperature=0)
llm_with_structured_output = llm.with_structured_output(schema=ContactInfo)

def extractor(state: State):
    history = state["messages"]
    
    # El LLM retorna un objeto ContactInfo validado
    schema = llm_with_structured_output.invoke([
        ("system", SYSTEM_PROMPT),
        *history
    ])
    
    return {
        "customer_name": schema.name,
        "phone": schema.phone,
        "my_age": str(schema.age)
    }
```

**Clave**:
- ✅ Usar `with_structured_output()` en lugar de `invoke()` simple
- ✅ Definir schemas con Pydantic
- ✅ Validación automática de tipos

---

## 🚀 Guía de Creación de Agentes

### Paso 1: Decidir el Tipo de Agente

#### Opción A: Agente Simple (Sin Nodos)
Para casos de uso directos sin lógica compleja.

```python
# src/agents/my_simple_agent.py
from langgraph.graph import StateGraph, START, END, MessagesState
from langchain.chat_models import init_chat_model

llm = init_chat_model("openai:gpt-4o-mini", temperature=0)

def process(state: MessagesState):
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

builder = StateGraph(MessagesState)
builder.add_node("process", process)
builder.add_edge(START, "process")
builder.add_edge("process", END)

agent = builder.compile()
```

#### Opción B: Agente con Nodos (Recomendado)
Para casos complejos con múltiples pasos.

### Paso 2: Crear la Estructura de Directorios

```bash
# Para un agente complejo
src/agents/my_agent/
├── __init__.py
├── agent.py              # Configuración del grafo
├── state.py              # Definición de estado
├── routes/               # Rutas condicionales (opcional)
└── nodes/
    ├── __init__.py
    ├── node_1/
    │   ├── __init__.py
    │   ├── node.py
    │   ├── prompt.py
    │   └── tools.py
    └── node_2/
        ├── __init__.py
        ├── node.py
        ├── prompt.py
        └── tools.py
```

### Paso 3: Definir el Estado

```python
# state.py
from langgraph.graph import MessagesState
from typing import Annotated

class State(MessagesState):
    """Estado personalizado del agente"""
    # Campos adicionales según necesidad
    user_id: str
    session_data: dict
    processing_status: str
```

### Paso 4: Crear los Nodos

#### 4.1. Nodo con LLM Simple

```python
# nodes/processor/node.py
from agents.my_agent.state import State
from langchain.chat_models import init_chat_model

llm = init_chat_model("openai:gpt-4o-mini", temperature=0)

def processor(state: State) -> dict:
    """Procesa mensajes con LLM"""
    messages = state["messages"]
    response = llm.invoke(messages)
    
    return {
        "messages": [response],
        "processing_status": "completed"
    }
```

#### 4.2. Nodo con Herramientas

```python
# nodes/tools_node/tools.py
from langchain_core.tools import tool

@tool("my_tool", description="Descripción de la herramienta")
def my_tool(param: str) -> str:
    """Realiza una operación"""
    return f"Resultado: {param}"

tools = [my_tool]

# nodes/tools_node/node.py
from agents.my_agent.state import State
from langchain.chat_models import init_chat_model
from agents.my_agent.nodes.tools_node.tools import tools

llm = init_chat_model("openai:gpt-4o-mini", temperature=0)
llm = llm.bind_tools(tools)

def tools_node(state: State) -> dict:
    """Nodo con capacidad de usar herramientas"""
    messages = state["messages"]
    response = llm.invoke(messages)
    
    return {"messages": [response]}
```

#### 4.3. Nodo con Extracción Estructurada

```python
# nodes/extractor/node.py
from pydantic import BaseModel, Field
from agents.my_agent.state import State
from langchain.chat_models import init_chat_model

class DataSchema(BaseModel):
    field1: str = Field(description="Descripción del campo 1")
    field2: int = Field(description="Descripción del campo 2")

llm = init_chat_model("openai:gpt-4o", temperature=0)
llm_with_structured_output = llm.with_structured_output(schema=DataSchema)

def extractor(state: State) -> dict:
    """Extrae datos estructurados"""
    messages = state["messages"]
    
    # IMPORTANTE: Usar llm_with_structured_output, no llm.invoke()
    data = llm_with_structured_output.invoke(messages)
    
    return {
        "user_id": data.field1,
        "session_data": {"field2": data.field2}
    }
```

### Paso 5: Configurar el Grafo

```python
# agent.py
from langgraph.graph import StateGraph, START, END
from agents.my_agent.state import State
from agents.my_agent.nodes.processor.node import processor
from agents.my_agent.nodes.extractor.node import extractor
from agents.my_agent.nodes.tools_node.node import tools_node

# Crear el grafo
builder = StateGraph(State)

# Agregar nodos
builder.add_node("extractor", extractor)
builder.add_node("processor", processor)
builder.add_node("tools_node", tools_node)

# Definir flujo
builder.add_edge(START, "extractor")
builder.add_edge("extractor", "processor")
builder.add_edge("processor", "tools_node")
builder.add_edge("tools_node", END)

# Compilar
agent = builder.compile()
```

### Paso 6: Registrar en langgraph.json

```json
{
    "dependencies": ["."],
    "graphs": {
        "my_agent": "./src/agents/my_agent/agent.py:agent"
    },
    "env": ".env"
}
```

### Paso 7: Validar

```bash
uv run langgraph dev
```

---

## 🔄 Migración a Arquitectura Limpia

### Situación Inicial: Código Monolítico

```python
# ❌ Antes: Todo en un archivo
from langchain.chat_models import init_chat_model
from pydantic import BaseModel

llm = init_chat_model("openai:gpt-4o")

class ContactInfo(BaseModel):
    name: str
    phone: str

def my_agent(messages):
    extractor = llm.with_structured_output(ContactInfo)
    contact = extractor.invoke(messages)
    response = llm.invoke(f"Hola {contact.name}")
    return response
```

### Paso 1: Identificar Responsabilidades

- **Extracción de datos** → Nodo `extractor`
- **Procesamiento de mensajes** → Nodo `processor`
- **Herramientas externas** → Nodo `tools`

### Paso 2: Crear Estructura Modular

```bash
mkdir -p src/agents/migrated_agent/{nodes/{extractor,processor},routes}
touch src/agents/migrated_agent/{__init__.py,agent.py,state.py}
touch src/agents/migrated_agent/nodes/{extractor,processor}/{__init__.py,node.py,prompt.py}
```

### Paso 3: Migrar Estado

```python
# ✅ state.py
from langgraph.graph import MessagesState

class State(MessagesState):
    customer_name: str
    phone: str
```

### Paso 4: Migrar Extractor

```python
# ✅ nodes/extractor/node.py
from pydantic import BaseModel, Field
from agents.migrated_agent.state import State
from langchain.chat_models import init_chat_model

class ContactInfo(BaseModel):
    name: str = Field(description="Nombre del cliente")
    phone: str = Field(description="Teléfono del cliente")

llm = init_chat_model("openai:gpt-4o", temperature=0)
llm_with_structured_output = llm.with_structured_output(schema=ContactInfo)

def extractor(state: State) -> dict:
    messages = state["messages"]
    contact = llm_with_structured_output.invoke(messages)
    
    return {
        "customer_name": contact.name,
        "phone": contact.phone
    }
```

### Paso 5: Migrar Procesador

```python
# ✅ nodes/processor/node.py
from agents.migrated_agent.state import State
from langchain.chat_models import init_chat_model

llm = init_chat_model("openai:gpt-4o", temperature=0)

def processor(state: State) -> dict:
    name = state.get("customer_name", "Cliente")
    response = llm.invoke(f"Hola {name}")
    
    return {"messages": [response]}
```

### Paso 6: Crear Grafo

```python
# ✅ agent.py
from langgraph.graph import StateGraph, START, END
from agents.migrated_agent.state import State
from agents.migrated_agent.nodes.extractor.node import extractor
from agents.migrated_agent.nodes.processor.node import processor

builder = StateGraph(State)
builder.add_node("extractor", extractor)
builder.add_node("processor", processor)

builder.add_edge(START, "extractor")
builder.add_edge("extractor", "processor")
builder.add_edge("processor", END)

agent = builder.compile()
```

### Paso 7: Registrar y Validar

```json
// langgraph.json
{
    "graphs": {
        "migrated_agent": "./src/agents/migrated_agent/agent.py:agent"
    }
}
```

```bash
uv run langgraph dev
```

### Checklist de Migración

- [ ] Código separado en nodos por responsabilidad
- [ ] Estado definido con tipos
- [ ] Prompts externalizados
- [ ] Herramientas modularizadas
- [ ] Sin lógica en `agent.py` (solo configuración)
- [ ] Imports relativos correctos
- [ ] Variables exportadas correctamente
- [ ] Sin código duplicado
- [ ] Documentación actualizada

---

## 🛠️ Herramientas y Tecnologías

### Core Framework

#### **LangGraph** (v1.0.6+)
**Valor**: Framework para construir aplicaciones multi-agente con grafos stateful.

**Ventajas**:
- ✅ Orquestación visual de flujos complejos
- ✅ Estado persistente entre nodos
- ✅ Debugging integrado
- ✅ Rutas condicionales
- ✅ Checkpointing automático

**Uso**:
```python
from langgraph.graph import StateGraph, START, END

builder = StateGraph(State)
builder.add_node("node1", function1)
builder.add_edge(START, "node1")
agent = builder.compile()
```

#### **LangChain** (v1.2.4+)
**Valor**: Biblioteca para desarrollo de aplicaciones con LLMs.

**Componentes Clave**:
- `init_chat_model`: Inicialización unificada de modelos
- `@tool`: Decorador para crear herramientas
- `PromptTemplate`: Gestión de prompts
- `with_structured_output`: Salidas estructuradas

**Uso**:
```python
from langchain.chat_models import init_chat_model
from langchain_core.tools import tool

llm = init_chat_model("openai:gpt-4o-mini", temperature=0)
```

#### **Pydantic** (Incluido en LangChain)
**Valor**: Validación de datos y creación de schemas.

**Uso en el Proyecto**:
```python
from pydantic import BaseModel, Field

class ContactInfo(BaseModel):
    name: str = Field(description="Nombre completo")
    age: int = Field(description="Edad", ge=0, le=150)
```

### Herramientas de Desarrollo

#### **UV** (Package Manager)
**Valor**: Gestor de paquetes ultrarrápido para Python.

**Comandos Principales**:
```bash
uv run langgraph dev          # Ejecutar servidor de desarrollo
uv add package-name           # Agregar dependencia
uv sync                       # Sincronizar dependencias
```

**Ventajas sobre pip**:
- ⚡ 10-100x más rápido
- 🔒 Lock files automáticos
- 🎯 Resolución de dependencias mejorada

#### **LangGraph CLI** (v0.4.11+)
**Valor**: CLI para desarrollo y testing de grafos.

**Características**:
- 🚀 Servidor de desarrollo con hot-reload
- 🎨 Studio UI para visualización
- 📊 API REST automática
- 🔍 Debugging interactivo

**Comandos**:
```bash
langgraph dev                 # Iniciar servidor
langgraph test                # Ejecutar tests
langgraph build               # Build para producción
```

#### **Jupyter Notebooks**
**Valor**: Experimentación y prototipado interactivo.

**Notebooks Incluidos**:
- `01-notebook.ipynb`: Introducción
- `05-rag.ipynb`: RAG patterns
- `07-structured_output.ipynb`: Salidas estructuradas

### Integraciones

#### **OpenAI** (vía LangChain-OpenAI)
**Valor**: Acceso a modelos GPT-4 y GPT-4o-mini.

**Configuración**:
```bash
# .env
OPENAI_API_KEY=sk-...
```

**Modelos Usados**:
- `gpt-4o`: Tareas complejas, extracción estructurada
- `gpt-4o-mini`: Conversación, tareas simples (más económico)

#### **APIs Externas**
El proyecto integra:
- **FakeStore API**: Productos de ejemplo
- **Open-Meteo**: Información meteorológica
- **Geocoding API**: Conversión de ciudades a coordenadas

### Gestión de Configuración

#### **langgraph.json**
**Valor**: Configuración centralizada de grafos.

```json
{
    "dependencies": ["."],
    "graphs": {
        "agent_name": "./path/to/agent.py:variable_name"
    },
    "env": ".env"
}
```

#### **.env**
**Valor**: Variables de entorno sensibles.

```bash
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-...
TEMPERATURE=0
```

---

## 🚀 Guía de Inicio Rápido

### 1. Setup Inicial

```bash
# Clonar/crear proyecto
cd my-first-agent

# Instalar dependencias
uv sync

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus API keys
```

### 2. Crear Primer Agente

```bash
# Crear estructura
mkdir -p src/agents/hello_agent
touch src/agents/hello_agent/{__init__.py,agent.py}
```

```python
# src/agents/hello_agent/agent.py
from langgraph.graph import StateGraph, START, END, MessagesState
from langchain.chat_models import init_chat_model

llm = init_chat_model("openai:gpt-4o-mini", temperature=0)

def hello(state: MessagesState):
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

builder = StateGraph(MessagesState)
builder.add_node("hello", hello)
builder.add_edge(START, "hello")
builder.add_edge("hello", END)

agent = builder.compile()
```

### 3. Registrar en langgraph.json

```json
{
    "dependencies": ["."],
    "graphs": {
        "hello": "./src/agents/hello_agent/agent.py:agent"
    },
    "env": ".env"
}
```

### 4. Ejecutar y Probar

```bash
# Iniciar servidor de desarrollo
uv run langgraph dev

# El servidor estará disponible en:
# - API: http://127.0.0.1:2024
# - Studio UI: https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024
```

### 5. Interactuar con el Agente

**Vía Studio UI**:
1. Abrir https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024
2. Seleccionar agente "hello"
3. Enviar mensajes

**Vía API REST**:
```bash
curl -X POST http://127.0.0.1:2024/assistants/hello/invoke \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "Hola"}]}'
```

**Vía Python**:
```python
from langgraph_sdk import get_client

client = get_client(url="http://127.0.0.1:2024")
response = client.runs.invoke(
    "hello",
    {"messages": [{"role": "user", "content": "Hola"}]}
)
print(response)
```

---

## 📚 Recursos Adicionales

### Documentación Oficial
- [LangGraph Docs](https://langchain-ai.github.io/langgraph/)
- [LangChain Docs](https://python.langchain.com/)
- [Pydantic Docs](https://docs.pydantic.dev/)

### Ejemplos en este Proyecto
- **Simple Agent**: `src/agents/simple.py`
- **RAG Agent**: `src/agents/rag.py`
- **Multi-Node Agent**: `src/agents/support/`
- **Tools Integration**: `src/agents/support/nodes/vendedor/`

### Troubleshooting Común

#### Error: "Could not find graph 'agent_name'"
**Solución**: Verificar que la variable exportada coincida con `langgraph.json`

#### Error: "name 'ContactInfo' is not defined"
**Solución**: Definir el schema antes de usarlo con `with_structured_output()`

#### Error: "'AIMessage' object has no attribute 'field'"
**Solución**: Usar `llm_with_structured_output.invoke()` en lugar de `llm.invoke()`

---

## 🎯 Próximos Pasos

1. **Explorar Notebooks**: Revisar ejemplos en `notebooks/`
2. **Crear Agente Personalizado**: Seguir la guía de creación
3. **Agregar Rutas Condicionales**: Implementar lógica de decisión
4. **Integrar Nuevas Herramientas**: Extender capacidades
5. **Deploy a Producción**: Usar LangSmith Deployment

---

**Última Actualización**: Enero 2026  
**Versión**: 1.0.0  
**Autor**: Equipo de Desarrollo
