# Evidencias — Laboratorio MCP Local

> **Proyecto**: Lab-Mcp_Local_Github
> **Servidor**: `server.py` — FastMCP("qaLabMcp") sobre stdio
> **Cliente MCP**: GitHub Copilot (modo Agent) en VS Code
> **Tools**: 3 tools base — `validar_cliente`, `generar_caso_prueba`, `calcular_percentil_simple`

---

## Índice

1. [Tools disponibles](#1-tools-disponibles)
2. [Configuración VS Code](#2-configuración-vs-code)
3. [Prueba A — `validar_cliente`](#3-prueba-a--validar_cliente)
4. [Prueba B — `generar_caso_prueba`](#4-prueba-b--generar_caso_prueba)
5. [Prueba C — `calcular_percentil_simple`](#5-prueba-c--calcular_percentil_simple)
6. [Resultados](#6-resultados)

---

## 1. Tools disponibles

| #  | Tool                      | Descripción                                               |
|----|---------------------------|-----------------------------------------------------------|
| 1  | `validar_cliente`         | Valida y normaliza CIP, teléfono y email.                 |
| 2  | `generar_caso_prueba`     | Genera un caso de prueba funcional.                       |
| 3  | `calcular_percentil_simple` | Calcula un percentil simple.                            |

---

## 2. Configuración VS Code

### `.vscode/mcp.json`

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

### Verificar servidor activo

1. Abrir VS Code en la raíz del proyecto.
2. `Ctrl+Shift+P` → `MCP: List Servers`.
3. Seleccionar `qaLabMcp` → `Start Server`.

**Captura — Servidor listado en VS Code**:

![MCP: List Servers](./capturas/evidencia-00-list-servers.png)

> 📸 **Tomar captura**: Pantallazo de `Ctrl+Shift+P` → `MCP: List Servers` mostrando `qaLabMcp` como servidor disponible.

---

## 3. Prueba A — `validar_cliente`

**Tool**: `validar_cliente(cip: str, telefono: str, email: str) -> dict`

**Prompt para Copilot (modo Agent)**:

> Usando el MCP server qaLabMcp, valida el cliente con CIP 12345, teléfono 6677-8899, correo prueba@demo.com.

**Resultado esperado**:
```json
{
  "valido": true,
  "cip": "12345",
  "telefono": "66778899",
  "email": "prueba@demo.com"
}
```

**Captura — Prueba A desde Copilot Agent**:

![Prueba A: validar_cliente](./capturas/evidencia-0A.png)

> 📸 **Tomar captura**: Pantallazo de Copilot Chat en modo Agent con el prompt y la respuesta devuelta.

### Casos adicionales

| #  | CIP     | Teléfono     | Email               | Resultado esperado                                       | Estado |
|----|---------|-------------|---------------------|----------------------------------------------------------|--------|
| 1  | `12345` | `6677-8899` | `prueba@demo.com`   | `{"valido": true, "cip": "12345", "telefono": "66778899", "email": "prueba@demo.com"}` | ⏳ |
| 2  | `""`    | `1234`      | `invalido`          | `{"valido": false, "errores": {"cip": "...", "telefono": "...", "email": "..."}}` | ⏳ |
| 3  | `ABC01` | `5555-1234` | `USER@Example.COM`  | `{"valido": true, "cip": "ABC01", "telefono": "55551234", "email": "user@example.com"}` | ⏳ |

---

## 4. Prueba B — `generar_caso_prueba`

**Tool**: `generar_caso_prueba(endpoint: str, metodo: str, escenario: str) -> dict`

**Prompt para Copilot (modo Agent)**:

> Usando el MCP server qaLabMcp, genera un caso de prueba para POST /api/login con credenciales inválidas.

**Resultado esperado** (estructura):
```json
{
  "id": "CP-POST-XXXX",
  "endpoint": "/api/login",
  "metodo": "POST",
  "escenario": "Credenciales inválidas",
  "pasos": [
    "Configurar solicitud POST a /api/login",
    "Establecer headers (Content-Type, Authorization si aplica)",
    "Ejecutar la solicitud y capturar la respuesta",
    "Validar código de estado HTTP",
    "Validar estructura y contenido del cuerpo de la respuesta"
  ],
  "criterio_aceptacion": "La respuesta debe ser consistente con el escenario descrito"
}
```

**Captura — Prueba B desde Copilot Agent**:

![Prueba B: generar_caso_prueba](./capturas/evidencia-0B.png)

> 📸 **Tomar captura**: Pantallazo de Copilot Chat en modo Agent con el prompt y la respuesta devuelta.

### Casos adicionales

| #  | Endpoint       | Método | Escenario                          | Resultado esperado | Estado |
|----|---------------|--------|------------------------------------|--------------------|--------|
| 1  | `/api/login`  | POST   | Credenciales inválidas             | Caso estructurado  | ⏳ |
| 2  | `/api/users`  | GET    | Listar usuarios sin autenticación  | Caso estructurado  | ⏳ |

---

## 5. Prueba C — `calcular_percentil_simple`

**Tool**: `calcular_percentil_simple(valores: list[float], percentil: float) -> float`

**Prompt para Copilot (modo Agent)**:

> Usando el MCP server qaLabMcp, calcula el percentil 95 de [120, 130, 150, 300, 90, 100, 500, 220].

**Resultado esperado**: `318.0`

**Cálculo manual**:
- Valores originales: `[120, 130, 150, 300, 90, 100, 500, 220]`
- `r = 0.95 * (8 - 1) = 6.65`
- `k = 6`, `delta = 0.65`
- `valores[6] = 500`, `valores[7] = 220`
- `P95 = 500 + 0.65 * (220 - 500) = 500 - 182 = 318.0`

**Captura — Prueba C desde Copilot Agent**:

![Prueba C: calcular_percentil_simple](./capturas/evidencia-0C.png)

> 📸 **Tomar captura**: Pantallazo de Copilot Chat en modo Agent con el prompt y la respuesta devuelta.

### Casos adicionales

| #  | Valores                                              | Percentil | Resultado esperado | Estado |
|----|------------------------------------------------------|-----------|-------------------|--------|
| 1  | `[120, 130, 150, 300, 90, 100, 500, 220]`           | 95        | `318.0`           | ⏳ |
| 2  | `[10, 20, 30, 40, 50]`                               | 50        | `30.0`            | ⏳ |
| 3  | `[100]`                                              | 50        | `100.0`           | ⏳ |

---

## 6. Resultados

| #  | Tool                      | Pruebas | Pass | Fail | Captura |
|----|---------------------------|---------|------|------|---------|
| 1  | `validar_cliente`         | 3       | 0    | 0    | `evidencia-0A.png` |
| 2  | `generar_caso_prueba`     | 2       | 0    | 0    | `evidencia-0B.png` |
| 3  | `calcular_percentil_simple` | 3     | 0    | 0    | `evidencia-0C.png` |
|    | **Total**                 | **8**   | **0**| **0** | — |

> ⏳ Pendiente de ejecución desde GitHub Copilot en modo Agent.

### Lista de capturas requeridas

| #  | Archivo                          | Contenido                                          |
|----|----------------------------------|----------------------------------------------------|
| 00 | `evidencia-00-list-servers.png`  | MCP: List Servers mostrando `qaLabMcp` disponible  |
| 01 | `evidencia-0A.png` | Copilot Agent + resultado de `validar_cliente`   |
| 02 | `evidencia-0B.png` | Copilot Agent + resultado de `generar_caso_prueba` |
| 03 | `evidencia-0C.png` | Copilot Agent + resultado de `calcular_percentil_simple` |

---

*Documento generado como evidencia del laboratorio "MCP Local — qaLabMcp" — Desarrollo de Software IX.*
