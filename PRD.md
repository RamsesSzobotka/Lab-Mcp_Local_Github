# PRD: Laboratorio MCP Local — qaLabMcp

> **Alcance del laboratorio**: Este laboratorio se enfoca exclusivamente en la creación del servidor MCP con 3 tools base. No incluye retos adicionales.

---

## Tabla de Contenido

1. [Resumen Ejecutivo](#1-resumen-ejecutivo)
2. [Alcance](#2-alcance)
3. [Requerimientos Funcionales](#3-requerimientos-funcionales)
4. [Requerimientos Técnicos](#4-requerimientos-técnicos)
5. [Arquitectura del MCP Server](#5-arquitectura-del-mcp-server)
6. [Configuración VS Code](#6-configuración-vs-code)
7. [Plan de Pruebas](#7-plan-de-pruebas)
8. [Criterios de Evaluación (Rúbrica)](#8-criterios-de-evaluación-rúbrica)

---

## 1. Resumen Ejecutivo

Este laboratorio forma parte de la materia **Desarrollo de Software IX** y tiene como objetivo que los estudiantes construyan un servidor MCP (*Model Context Protocol*) local utilizando Python y la librería FastMCP. El servidor expone 3 herramientas (*tools*) que pueden ser descubiertas y ejecutadas desde un cliente MCP compatible (GitHub Copilot en modo Agent) dentro de Visual Studio Code.

El nombre del servidor FastMCP es `"qaLabMcp"`. El transporte es `stdio` y se configura mediante `.vscode/mcp.json`.

---

## 2. Alcance

### Incluye

- Creación de un servidor MCP con FastMCP en Python.
- Implementación de **3 tools base**:
  - `validar_cliente` — valida y normaliza datos de un cliente (CIP, teléfono, email).
  - `generar_caso_prueba` — genera un caso de prueba funcional para un endpoint.
  - `calcular_percentil_simple` — calcula un percentil simple sobre una lista de valores.
- Configuración del archivo `mcp.json` en `.vscode/` para registro del servidor en VS Code.
- Pruebas de descubrimiento y ejecución de tools desde GitHub Copilot en modo Agent.

### No incluye

- Retos prácticos adicionales (fuera del alcance base).
- Integración directa con GitHub Copilot a nivel de extensión o plugin.
- Despliegue en producción del servidor MCP.
- Autenticación, autorización o manejo de usuarios.
- Persistencia en base de datos externa.
- Lectura de archivos JSON externos.

---

## 3. Requerimientos Funcionales

### Tools Base (FastMCP)

| #  | Tool                      | Descripción                                                       |
|----|---------------------------|-------------------------------------------------------------------|
| 1  | `validar_cliente`         | Valida y normaliza CIP, teléfono y email de un cliente.           |
| 2  | `generar_caso_prueba`     | Genera un caso de prueba funcional a partir de endpoint, método y escenario. |
| 3  | `calcular_percentil_simple` | Calcula un percentil simple usando interpolación lineal (método R7). |

#### Detalle de cada tool

**1. `validar_cliente(cip, telefono, email)`**
- CIP: valida que no esté vacío.
- Teléfono: extrae solo dígitos, valida mínimo 8 dígitos.
- Email: valida formato con regex, normaliza a minúsculas.
- Retorna `{"valido": True, ...}` con datos normalizados o `{"valido": False, "errores": {...}}`.

**2. `generar_caso_prueba(endpoint, metodo, escenario)`**
- Valida que el método HTTP sea uno de: GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS.
- Genera un ID único, lista de pasos y criterio de aceptación.
- Retorna un diccionario estructurado con el caso de prueba.

**3. `calcular_percentil_simple(valores, percentil)`**
- Ordena los valores y aplica interpolación lineal R7 (estándar Excel/NumPy).
- Retorna el valor del percentil solicitado.
- Lanza `ValueError` si el percentil está fuera del rango 0-100.

---

## 4. Requerimientos Técnicos

| Requerimiento          | Especificación                                      |
|------------------------|-----------------------------------------------------|
| Lenguaje               | Python 3.10+                                       |
| SDK                    | FastMCP (`pip install mcp[cli]` o `pip install fastmcp`) |
| Sistema operativo      | Windows 10/11                                      |
| Editor                 | VS Code con extensión GitHub Copilot (modo Agent)  |
| Gestor de paquetes     | `pip`                                              |
| Entorno virtual        | `venv` (opcional pero recomendado)                 |

### Estructura del proyecto

```
qaLabMcp/
├── .vscode/
│   └── mcp.json                  # Configuración del servidor MCP
├── server.py                     # Servidor MCP con FastMCP (3 tools)
├── PRD.md                        # Este documento
├── EVIDENCIAS.md                 # Resultados de pruebas
└── README.md                     # Instrucciones del laboratorio
```

---

## 5. Arquitectura del MCP Server

### Diagrama de flujo

```
[VS Code] → [MCP Client (Copilot Agent)]
                ↓
         [stdio transport]
                ↓
      [server.py - FastMCP("qaLabMcp")]
                ↓
     ┌──────────┬──────────┬──────────┐
     │validar_  │generar_  │calcular_ │
     │cliente   │caso_     │percentil_│
     │          │prueba    │simple    │
     └──────────┴──────────┴──────────┘
```

### Componentes

1. **FastMCP Server**: Instancia `FastMCP("qaLabMcp")` que registra y expone las tools.
2. **Tools**: Funciones decoradas con `@mcp.tool()` que implementan la lógica de cada operación.
3. **Transporte**: Comunicación vía `stdio` entre VS Code y el servidor MCP.

### Flujo de ejecución

1. VS Code inicia el servidor MCP mediante la configuración en `mcp.json`.
2. Copilot (modo Agent) descubre las herramientas disponibles vía MCP (`list_tools`).
3. El usuario solicita una acción → Copilot invoca la tool correspondiente (`call_tool`).
4. El servidor procesa la solicitud y devuelve un resultado estructurado.
5. Copilot presenta el resultado al usuario en lenguaje natural.

---

## 6. Configuración VS Code

### Archivo `.vscode/mcp.json`

El servidor se configura como un MCP server de tipo `stdio` que ejecuta el script `server.py` con el intérprete de Python:

```json
{
  "servers": {
    "qaLabMcp": {
      "type": "stdio",
      "command": "python",
      "args": ["server.py"],
      "cwd": "C:\\Users\\ramse\\Documents\\Universidad\\Des_Software IX\\Lab-Mcp_Local_Github"
    }
  }
}
```

### Verificación

1. Abrir VS Code en la raíz del proyecto.
2. Abrir la paleta de comandos (`Ctrl+Shift+P`).
3. Ejecutar `MCP: List Servers`.
4. Debería aparecer `qaLabMcp` como servidor disponible.
5. Seleccionar `qaLabMcp` > `Start Server`.

**Regla importante**: No ejecutar `python server.py` manualmente en otra terminal. VS Code maneja el proceso stdio automáticamente.

---

## 7. Plan de Pruebas

Las pruebas se ejecutan desde **GitHub Copilot en modo Agent** y verifican que las tools sean descubiertas y respondan correctamente.

### Prueba A: `validar_cliente`

| Campo     | Valor                                                       |
|-----------|-------------------------------------------------------------|
| Prompt    | "Usando el MCP server, valida el cliente con CIP 12345, teléfono 6677-8899, correo prueba@demo.com." |
| Esperado  | `{"valido": True, "cip": "12345", "telefono": "66778899", "email": "prueba@demo.com"}` |

### Prueba B: `generar_caso_prueba`

| Campo     | Valor                                                       |
|-----------|-------------------------------------------------------------|
| Prompt    | "Usando el MCP server, genera un caso de prueba para POST /api/login con credenciales inválidas." |
| Esperado  | Caso de prueba estructurado con ID, endpoint, pasos y criterio de aceptación. |

### Prueba C: `calcular_percentil_simple`

| Campo     | Valor                                                       |
|-----------|-------------------------------------------------------------|
| Prompt    | "Usando el MCP server, calcula el percentil 95 de [120, 130, 150, 300, 90, 100, 500, 220]." |
| Esperado  | `318.0` (valor del percentil 95, método simple)              |

---

## 8. Criterios de Evaluación (Rúbrica)

### 8.1 Servidor MCP Base (3 tools con FastMCP) — Peso 25%

| Nivel       | Pts | Descripción |
|-------------|-----|-------------|
| Excellent   | 5   | Las 3 tools funcionan y `server.py` compila sin errores; FastMCP nombrado `"qaLabMcp"`. |
| Good        | 4   | Las 3 tools presentes y funcionan con detalles menores (normalización incompleta). |
| Fair        | 2   | Solo 1-2 tools funcionan o compila con tools incompletas. |
| Poor        | 0   | `server.py` no compila o las tools base no funcionan. |

### 8.2 Registro y conexión en VS Code (mcp.json + List Servers) — Peso 25%

| Nivel       | Pts | Descripción |
|-------------|-----|-------------|
| Excellent   | 5   | `mcp.json` correcto (stdio, python, args, cwd) en `.vscode/` y el servidor inicia desde `MCP: List Servers` sin tocar la terminal. |
| Good        | 4   | El servidor inicia pero con configuración subóptima o requiere reintentos. |
| Fair        | 2   | `mcp.json` mal ubicado o el servidor inicia con dificultad. |
| Poor        | 0   | El servidor no se registra ni inicia desde VS Code. |

### 8.3 Ejecución desde Copilot en modo Agent (3 pruebas) — Peso 25%

| Nivel       | Pts | Descripción |
|-------------|-----|-------------|
| Excellent   | 5   | Las tools aparecen en Copilot (Agent) y las 3 pruebas (A, B, C) devuelven respuestas estructuradas correctas. |
| Good        | 4   | Las 3 pruebas se ejecutan con 1 resultado parcial. |
| Fair        | 2   | Solo 1-2 pruebas se ejecutan correctamente. |
| Poor        | 0   | Copilot no descubre las tools o ninguna prueba se ejecuta. |

### 8.4 Evidencias y documentación — Peso 25%

| Nivel       | Pts | Descripción |
|-------------|-----|-------------|
| Excellent   | 5   | Evidencia completa de cada prueba: tool visible, prompt y resultado, organizada y legible. |
| Good        | 4   | Evidencia de la mayoría de pruebas, con algunas capturas faltantes. |
| Fair        | 2   | Evidencia escasa o sin el prompt/resultado correspondiente. |
| Poor        | 0   | Sin evidencias. |

---

*Documento generado para el laboratorio "MCP Local — qaLabMcp" de la materia Desarrollo de Software IX.*
