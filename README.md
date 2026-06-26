# Laboratorio MCP Local — qaLabMcp

Servidor MCP (*Model Context Protocol*) local construido con Python y FastMCP. Expone **3 tools** que pueden ser descubiertas y ejecutadas desde GitHub Copilot en modo Agent dentro de Visual Studio Code.

---

## Requisitos

- Python 3.10+ instalado en Windows (`python --version`)
- VS Code con la carpeta del proyecto abierta
- Extensión Python en VS Code
- GitHub Copilot Chat con sesión iniciada

### Instalación del SDK

```bash
pip install "mcp[cli]"
```

---

## Estructura del proyecto

```
qaLabMcp/
├── .vscode/
│   └── mcp.json                    # Configuración del servidor MCP
├── capturas/                       # Capturas de pantalla de evidencias
│   ├── evidencia-00-list-servers.png
│   ├── evidencia-0A.png
│   ├── evidencia-0B.png
│   ├── evidencia-0C.png
│   ├── Evidencia-RetoA.png
│   ├── Evidencia-RetoB.png
│   ├── Evidencia-RetoC.png
│   └── Evidencia-RetoD.png
├── datos_prueba.json               # Datos de prueba para buscar_cliente
├── server.py                       # Servidor MCP con FastMCP (7 tools)
├── PRD.md                          # Documento de requerimientos
├── EVIDENCIAS.md                   # Resultados de pruebas y capturas
└── README.md                       # Este archivo
```

---

## Tools disponibles

| #  | Tool                      | Tipo  | Descripción                               | Parámetros                                      |
|----|---------------------------|-------|-------------------------------------------|-------------------------------------------------|
| 1  | `validar_cliente`         | Base  | Valida y normaliza CIP, teléfono y email  | `cip`, `telefono`, `email`                      |
| 2  | `generar_caso_prueba`     | Base  | Genera un caso de prueba funcional        | `endpoint`, `metodo`, `escenario`               |
| 3  | `calcular_percentil_simple` | Base | Calcula un percentil simple              | `valores`, `percentil`                          |
| 4  | `clasificar_error_http`   | Reto  | Clasifica código HTTP en categoría        | `status_code`                                   |
| 5  | `evaluar_sla`             | Reto  | Evalúa cumplimiento de SLA                | `p95_ms`, `limite_ms`                           |
| 6  | `validar_respuesta_api`   | Reto  | Valida respuesta API contra criterios     | `status_code`, `tiempo_ms`, `limite_ms`, `tiene_token` |
| 7  | `buscar_cliente`          | Reto  | Busca cliente por CIP en JSON             | `cip`                                           |

---

## Configuración en VS Code

### 1. Crear/verificar `.vscode/mcp.json`

Ubicación: `.vscode/mcp.json` (en la raíz del proyecto)

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

> Ajusta la ruta en `cwd` según tu máquina.

### 2. Iniciar el servidor

1. Abrir VS Code en la raíz del proyecto.
2. `Ctrl+Shift+P` → `MCP: List Servers`.
3. Seleccionar `qaLabMcp` → `Start Server`.

**Importante**: No ejecutes `python server.py` en otra terminal. VS Code maneja el proceso stdio automáticamente.

---

## Pruebas desde Copilot (modo Agent)

Una vez que el servidor esté activo, abre GitHub Copilot Chat, cambia a modo **Agent** y ejecuta estos prompts **exactos**:

### Tools Base

| Prueba | Prompt | Esperado |
|--------|--------|----------|
| **A** — `validar_cliente` | "Usando el MCP server qaLabMcp, valida el cliente con CIP 12345, teléfono 6677-8899, correo prueba@demo.com." | `{"valido": true, "cip": "12345", ...}` |
| **B** — `generar_caso_prueba` | "Usando el MCP server qaLabMcp, genera un caso de prueba para POST /api/login con credenciales inválidas." | Caso estructurado con ID, pasos y criterio |
| **C** — `calcular_percentil_simple` | "Usando el MCP server qaLabMcp, calcula el percentil 95 de [120, 130, 150, 300, 90, 100, 500, 220]." | `318.0` |

### Retos

| Reto  | Prompt | Esperado |
|-------|--------|----------|
| **A** — `clasificar_error_http` | "Usando el MCP server qaLabMcp, clasifica el código HTTP 500." | `"Error del servidor"` |
| **B** — `evaluar_sla` | "Usando el MCP server qaLabMcp, evalúa el SLA con p95=480ms y límite=500ms." | `{"cumple": true, "diferencia_ms": 20}` |
| **C** — `validar_respuesta_api` | "Usando el MCP server qaLabMcp, valida la respuesta API con status 200, tiempo 350ms, límite 500ms y token true." | `{"valido": true, "razon": "..."}` |
| **D** — `buscar_cliente` | "Usando el MCP server qaLabMcp, busca el cliente con CIP CIP001 en datos_prueba.json." | `{"cip": "CIP001", "nombre": "Juan Perez", ...}` |

---

## Evidencias

Las capturas de cada prueba, los prompts exactos y los resultados obtenidos están documentados en **[EVIDENCIAS.md](./EVIDENCIAS.md)**.

---

## Verificación de compilación

```bash
python -m py_compile server.py
```

Si no muestra errores, el servidor compila correctamente.

---

*Laboratorio "MCP Local — qaLabMcp" — Desarrollo de Software IX.*
