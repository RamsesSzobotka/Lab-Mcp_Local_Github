# PRD: Laboratorio MCP Local GitHub — Desarrollo de Software IX

> **Alcance del laboratorio**: Este laboratorio se enfoca exclusivamente en la creación del servidor MCP. La conexión con GitHub Copilot queda fuera del alcance de este documento.

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

Este laboratorio forma parte de la materia **Desarrollo de Software IX** y tiene como objetivo que los estudiantes construyan un servidor MCP (*Model Context Protocol*) local utilizando Python y la librería FastMCP. El servidor expondrá herramientas (*tools*) que podrán ser descubiertas y ejecutadas desde un cliente MCP compatible (GitHub Copilot en modo Agent).

El repositorio del proyecto se aloja en [https://github.com/RamsesSzobotka/Lab-Mcp_Local_Github](https://github.com/RamsesSzobotka/Lab-Mcp_Local_Github), rama `main`. El trabajo se centra en el desarrollo del servidor, su configuración en VS Code y la validación de su funcionamiento a través de pruebas ejecutadas desde Copilot.

---

## 2. Alcance

### Incluye

- Creación de un servidor MCP con FastMCP en Python.
- Implementación de 3 tools base.
- Implementación de 4 tools correspondientes a retos prácticos.
- Configuración del archivo `mcp.json` en `.vscode/` para registro del servidor en VS Code.
- Pruebas de descubrimiento y ejecución de tools desde GitHub Copilot en modo Agent.
- Lectura de datos desde `data_prueba.json` (archivo de datos de prueba).

### No incluye

- Integración directa con GitHub Copilot a nivel de extensión o plugin.
- Despliegue en producción del servidor MCP.
- Autenticación, autorización o manejo de usuarios.
- Persistencia en base de datos externa.
- Conexión a servicios cloud o APIs externas.

---

## 3. Requerimientos Funcionales

### 3.1 Tools Base (FastMCP)

| #  | Tool              | Descripción                                                        |
|----|-------------------|--------------------------------------------------------------------|
| 1  | `saludar`         | Recibe un nombre y devuelve un saludo personalizado.               |
| 2  | `sumar`           | Recibe dos números enteros y retorna su suma.                      |
| 3  | `contar_palabras` | Recibe un texto y retorna el número de palabras que lo componen.   |

### 3.2 Tools de Retos Prácticos

| #  | Tool               | Descripción                                                                  |
|----|--------------------|------------------------------------------------------------------------------|
| 1  | `buscar_cliente`   | Lee `data_prueba.json` y busca un cliente por su ID. Retorna nombre y email. |
| 2  | `calcular_promedio`| Recibe una lista de calificaciones y retorna el promedio.                    |
| 3  | `analizar_texto`   | Recibe un texto y retorna: cantidad de caracteres, palabras y vocales.       |
| 4  | `generar_resumen`  | Recibe un texto largo y retorna un resumen de las primeras N oraciones.      |

---

## 4. Requerimientos Técnicos

| Requerimiento          | Especificación                                      |
|------------------------|-----------------------------------------------------|
| Lenguaje               | Python 3.10+                                       |
| SDK                    | FastMCP (`pip install fastmcp`)                    |
| Sistema operativo      | Windows 10/11                                      |
| Editor                 | VS Code con extensión GitHub Copilot (modo Agent)  |
| Formato de datos       | JSON (`data_prueba.json`)                          |
| Gestor de paquetes     | `pip`                                              |
| Entorno virtual        | `venv` (opcional pero recomendado)                 |

### Estructura del proyecto

```
Lab-Mcp_Local_Github/
├── .vscode/
│   └── mcp.json                  # Configuración del servidor MCP
├── server.py                     # Servidor MCP con FastMCP
├── data_prueba.json              # Archivo de datos para retos prácticos
├── PRD.md                        # Este documento
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
      [server.py - FastMCP]
                ↓
     ┌──────┬──────┬──────┐
     │ Tool │ Tool │ Tool │
     │  1   │  2   │ ...  │
     └──────┴──────┴──────┘
                ↓
         [data_prueba.json]  (para tools que requieren datos)
```

### Componentes

1. **FastMCP Server**: Instancia principal que registra y expone las tools.
2. **Tools**: Funciones decoradas con `@mcp.tool()` que implementan la lógica de cada operación.
3. **Transporte**: Comunicación vía stdio entre VS Code y el servidor MCP.
4. **Datos**: Archivo `data_prueba.json` en la raíz del proyecto, leído por tools como `buscar_cliente`.

### Flujo de ejecución

1. VS Code inicia el servidor MCP mediante la configuración en `mcp.json`.
2. Copilot (modo Agent) descubre las herramientas disponibles vía MCP.
3. El usuario solicita una acción → Copilot invoca la tool correspondiente.
4. El servidor procesa la solicitud y devuelve un resultado estructurado.
5. Copilot presenta el resultado al usuario en lenguaje natural.

---

## 6. Configuración VS Code

### Archivo `.vscode/mcp.json`

El servidor se configura como un MCP server de tipo `stdio` que ejecuta el script `server.py` con el intérprete de Python.

```json
{
  "servers": {
    "lab-mcp-local": {
      "type": "stdio",
      "command": "python",
      "args": ["server.py"],
      "cwd": "C:\\Users\\ramse\\Documents\\Universidad\\Des_Software IX\\Lab-Mcp_Local_Github"
    }
  }
}
```

### Notas de configuración

- `type`: `"stdio"` — el servidor se comunica por entrada/salida estándar.
- `command`: `"python"` — debe estar disponible en el PATH del sistema.
- `args`: `["server.py"]` — script principal del servidor.
- `cwd`: Ruta absoluta al directorio raíz del proyecto (ajustar según la máquina del estudiante).

---

## 7. Plan de Pruebas

Las pruebas se ejecutan desde **GitHub Copilot en modo Agent** y verifican que las tools sean descubiertas y respondan correctamente.

### Prueba A: Tool base — `sumar`

| Campo     | Valor                                          |
|-----------|------------------------------------------------|
| Prompt    | "Usando el MCP server local, suma 15 y 27."   |
| Esperado  | El servidor responde con `42`.                 |

### Prueba B: Tool base — `contar_palabras`

| Campo     | Valor                                                              |
|-----------|--------------------------------------------------------------------|
| Prompt    | "Usando el MCP server local, cuenta las palabras del siguiente texto: 'Hola mundo, este es un laboratorio de MCP.'" |
| Esperado  | El servidor responde con `8`.                                      |

### Prueba C: Tool de reto — `buscar_cliente`

| Campo     | Valor                                                                   |
|-----------|-------------------------------------------------------------------------|
| Prompt    | "Usando el MCP server local, busca el cliente con ID 1 en el archivo de datos." |
| Esperado  | El servidor retorna el nombre y email del cliente con ID 1 desde `data_prueba.json`. |

---

## 8. Criterios de Evaluación (Rúbrica)

### 8.1 Servidor MCP Base (3 tools con FastMCP) — Peso 20%

| Nivel       | Pts | Descripción                                                                 |
|-------------|-----|-----------------------------------------------------------------------------|
| Excellent   | 4   | Las 3 tools funcionan y server.py compila sin errores; FastMCP nombrado correctamente. |
| Good        | 3   | Las 3 tools presentes y funcionan con detalles menores (campo o normalización incompleta). |
| Fair        | 2   | Solo 1-2 tools funcionan o compila con tools incompletas.                    |
| Poor        | 1   | server.py no compila o las tools base no funcionan.                          |

### 8.2 Registro y conexión en VS Code (mcp.json + List Servers) — Peso 20%

| Nivel       | Pts | Descripción                                                                 |
|-------------|-----|-----------------------------------------------------------------------------|
| Excellent   | 4   | mcp.json correcto (stdio, python, args/cwd) en .vscode/ y el servidor inicia desde MCP: List Servers sin tocar la terminal. |
| Good        | 3   | El servidor inicia pero con configuración subóptima o requiere reintentos.    |
| Fair        | 2   | mcp.json mal ubicado o el servidor inicia con dificultad / fuera del flujo de VS Code. |
| Poor        | 1   | El servidor no se registra ni inicia desde VS Code.                          |

### 8.3 Ejecución desde Copilot en modo Agent (3 pruebas) — Peso 20%

| Nivel       | Pts | Descripción                                                                 |
|-------------|-----|-----------------------------------------------------------------------------|
| Excellent   | 4   | Las tools aparecen en Copilot (Agent) y las 3 pruebas A, B y C devuelven respuestas estructuradas correctas. |
| Good        | 3   | Las 3 pruebas se ejecutan con 1 resultado parcial o autorización no documentada. |
| Fair        | 2   | Solo 1-2 pruebas se ejecutan correctamente desde Copilot.                    |
| Poor        | 1   | Copilot no descubre las tools o ninguna prueba se ejecuta.                   |

### 8.4 Retos prácticos (4 tools adicionales) — Peso 20%

| Nivel       | Pts | Descripción                                                                 |
|-------------|-----|-----------------------------------------------------------------------------|
| Excellent   | 4   | Los 4 retos implementados y probados con los casos indicados, incluyendo lectura de data_prueba.json en buscar_cliente. |
| Good        | 3   | 3 de 4 retos correctos y probados.                                          |
| Fair        | 2   | 1-2 retos correctos o probados parcialmente.                                |
| Poor        | 1   | Ningún reto implementado o probado.                                         |

### 8.5 Evidencias y documentación (tool, prompt, resultado) — Peso 20%

| Nivel       | Pts | Descripción                                                                 |
|-------------|-----|-----------------------------------------------------------------------------|
| Excellent   | 4   | Evidencia completa de cada prueba y reto: tool visible, prompt y resultado, organizada y legible en el repo. |
| Good        | 3   | Evidencia de la mayoría de pruebas/retos, con algunas capturas faltantes.    |
| Fair        | 2   | Evidencia escasa o sin el prompt/resultado correspondiente.                  |
| Poor        | 1   | Sin evidencias.                                                             |

---

*Documento generado para el laboratorio "MCP Local GitHub" de la materia Desarrollo de Software IX.*
