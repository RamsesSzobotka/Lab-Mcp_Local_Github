# Laboratorio MCP Local GitHub — Desarrollo de Software IX

Servidor MCP (*Model Context Protocol*) local construido con Python y FastMCP. Expone herramientas (tools) que pueden ser descubiertas y ejecutadas desde cualquier cliente MCP compatible.

## Requisitos

| Requerimiento | Especificación |
|---------------|----------------|
| Lenguaje | Python 3.10+ |
| SDK | FastMCP (`pip install fastmcp`) |
| SO | Windows 10/11 |
| Editor | VS Code (opcional, con extensión GitHub Copilot) |
| Gestor de paquetes | `pip` |

## Instalación

```bash
# Clonar el repositorio
git clone https://github.com/RamsesSzobotka/Lab-Mcp_Local_Github.git
cd Lab-Mcp_Local_Github

# (Opcional) Crear y activar entorno virtual
python -m venv venv
.\venv\Scripts\activate

# Instalar dependencias
pip install fastmcp
```

## Estructura del proyecto

```
Lab-Mcp_Local_Github/
├── .vscode/
│   └── mcp.json              # Configuración del servidor MCP para VS Code
├── server.py                  # Servidor MCP con FastMCP
├── data_prueba.json           # Archivo de datos para retos prácticos
├── PRD.md                     # Documento de requerimientos del laboratorio
├── EVIDENCIAS.md              # Resultados de pruebas y evidencias
└── README.md                  # Este archivo
```

## Tools disponibles

### Tools Base

| Tool | Descripción | Ejemplo |
|------|-------------|---------|
| `saludar` | Saluda a una persona por su nombre | `saludar("Juan")` → `¡Hola, Juan!` |
| `sumar` | Suma dos números enteros | `sumar(15, 27)` → `42` |
| `contar_palabras` | Cuenta palabras en un texto | `contar_palabras("Hola mundo")` → `2` |

### Tools de Reto

| Tool | Descripción | Ejemplo |
|------|-------------|---------|
| `buscar_cliente` | Busca cliente por ID en `data_prueba.json` | `buscar_cliente(1)` → datos de Juan Perez |
| `calcular_promedio` | Calcula promedio de calificaciones | `calcular_promedio([85,90,78])` → `84.33` |
| `analizar_texto` | Analiza caracteres, palabras y vocales | `analizar_texto("Hola")` → stats del texto |
| `generar_resumen` | Genera resumen de primeras N oraciones | `generar_resumen(texto, 2)` → primeras 2 oraciones |

## Configuración en VS Code

El servidor se registra automáticamente en VS Code mediante el archivo `.vscode/mcp.json`:

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

Para verificar que el servidor está activo:
1. Abrir VS Code en la raíz del proyecto
2. Abrir la paleta de comandos (`Ctrl+Shift+P`)
3. Ejecutar `MCP: List Servers`
4. Debería aparecer `lab-mcp-local` como servidor disponible

## Ejecución directa (sin VS Code)

```bash
python server.py
```

El servidor se inicia en modo `stdio` y queda a la espera de conexiones del cliente MCP.

## Pruebas

Las pruebas se documentan en [EVIDENCIAS.md](./EVIDENCIAS.md) e incluyen:

- **Prueba A**: `sumar(15, 27)` → resultado esperado: `42`
- **Prueba B**: `contar_palabras("Hola mundo, este es un laboratorio de MCP.")` → resultado esperado: `8`
- **Prueba C**: `buscar_cliente(1)` → resultado esperado: datos de cliente ID 1
- **Retos**: `calcular_promedio`, `analizar_texto`, `generar_resumen`
