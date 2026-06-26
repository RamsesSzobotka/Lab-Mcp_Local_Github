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
│   └── evidencia-0C.png
├── server.py                       # Servidor MCP con FastMCP (3 tools)
├── PRD.md                          # Documento de requerimientos
├── EVIDENCIAS.md                   # Resultados de pruebas y capturas
└── README.md                       # Este archivo
```

---

## Tools disponibles

| Tool                      | Descripción                                               | Parámetros                                      |
|---------------------------|-----------------------------------------------------------|-------------------------------------------------|
| `validar_cliente`         | Valida y normaliza CIP, teléfono y email                  | `cip`, `telefono`, `email`                      |
| `generar_caso_prueba`     | Genera un caso de prueba funcional                        | `endpoint`, `metodo`, `escenario`               |
| `calcular_percentil_simple` | Calcula un percentil simple                             | `valores`, `percentil`                          |

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

### Prueba A — `validar_cliente`

**Prompt**:
> Usando el MCP server qaLabMcp, valida el cliente con CIP 12345, teléfono 6677-8899, correo prueba@demo.com.

**Resultado esperado**:
```json
{"valido": true, "cip": "12345", "telefono": "66778899", "email": "prueba@demo.com"}
```

**Captura sugerida**: `capturas/evidencia-0A.png`

---

### Prueba B — `generar_caso_prueba`

**Prompt**:
> Usando el MCP server qaLabMcp, genera un caso de prueba para POST /api/login con credenciales inválidas.

**Resultado esperado**: Caso de prueba estructurado con ID, 5 pasos y criterio de aceptación.

**Captura sugerida**: `capturas/evidencia-0B.png`

---

### Prueba C — `calcular_percentil_simple`

**Prompt**:
> Usando el MCP server qaLabMcp, calcula el percentil 95 de [120, 130, 150, 300, 90, 100, 500, 220].

**Resultado esperado**: `318.0`

**Captura sugerida**: `capturas/evidencia-0C.png`

---

## Guía rápida para tomar evidencias

| #  | Qué capturar                                      | Prompt exacto | Archivo |
|----|---------------------------------------------------|---------------|---------|
| 00 | `MCP: List Servers` mostrando `qaLabMcp` activo   | — |
| 01 | Copilot Agent respondiendo `validar_cliente`      | "Usando el MCP server qaLabMcp, valida el cliente con CIP 12345, teléfono 6677-8899, correo prueba@demo.com." | `evidencia-0A.png` |
| 02 | Copilot Agent respondiendo `generar_caso_prueba`  | "Usando el MCP server qaLabMcp, genera un caso de prueba para POST /api/login con credenciales inválidas." | `evidencia-0B.png` |
| 03 | Copilot Agent respondiendo `calcular_percentil_simple` | "Usando el MCP server qaLabMcp, calcula el percentil 95 de [120, 130, 150, 300, 90, 100, 500, 220]." | `evidencia-0C.png` |

---

## Verificación de compilación

```bash
python -m py_compile server.py
```

Si no muestra errores, el servidor compila correctamente.

---

*Laboratorio "MCP Local — qaLabMcp" — Desarrollo de Software IX.*
