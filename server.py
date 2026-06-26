from fastmcp import FastMCP
import json
import re
import math

mcp = FastMCP("qaLabMcp")


@mcp.tool()
def validar_cliente(cip: str, telefono: str, email: str) -> dict:
    """Valida y normaliza datos de un cliente.

    Args:
        cip: Identificador del cliente (CIP).
        telefono: Número de teléfono del cliente.
        email: Correo electrónico del cliente.

    Returns:
        Diccionario con resultado de validación y datos normalizados.
    """
    errores = {}
    resultado = {}

    # Validar CIP
    cip = cip.strip() if cip else ""
    if not cip:
        errores["cip"] = "El CIP no puede estar vacío"
    else:
        resultado["cip"] = cip

    # Validar y normalizar teléfono
    telefono = telefono.strip() if telefono else ""
    if not telefono:
        errores["telefono"] = "El teléfono no puede estar vacío"
    else:
        digitos = re.sub(r"\D", "", telefono)
        if len(digitos) < 8:
            errores["telefono"] = "El teléfono debe tener al menos 8 dígitos"
        else:
            resultado["telefono"] = digitos

    # Validar y normalizar email
    email = email.strip().lower() if email else ""
    if not email:
        errores["email"] = "El email no puede estar vacío"
    else:
        patron = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(patron, email):
            errores["email"] = "El email no tiene un formato válido"
        else:
            resultado["email"] = email

    if errores:
        return {"valido": False, "errores": errores}

    return {"valido": True, **resultado}


@mcp.tool()
def generar_caso_prueba(endpoint: str, metodo: str, escenario: str) -> dict:
    """Genera un caso de prueba funcional.

    Args:
        endpoint: Ruta del endpoint (ej. /api/login).
        metodo: Método HTTP (GET, POST, PUT, PATCH, DELETE).
        escenario: Descripción del escenario a probar.

    Returns:
        Diccionario con el caso de prueba estructurado.
    """
    metodo = metodo.upper().strip()
    metodos_validos = ["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"]

    if metodo not in metodos_validos:
        return {
            "error": f"Método HTTP no válido. Válidos: {', '.join(metodos_validos)}"
        }

    if not endpoint or not endpoint.strip():
        return {"error": "El endpoint no puede estar vacío"}

    if not escenario or not escenario.strip():
        return {"error": "El escenario no puede estar vacío"}

    endpoint_limpio = endpoint.strip()
    escenario_limpio = escenario.strip()

    caso = {
        "id": f"CP-{metodo}-{abs(hash(endpoint_limpio + escenario_limpio)) % 10000:04d}",
        "endpoint": endpoint_limpio,
        "metodo": metodo,
        "escenario": escenario_limpio,
        "pasos": [
            f"Configurar solicitud {metodo} a {endpoint_limpio}",
            "Establecer headers (Content-Type, Authorization si aplica)",
            f"Ejecutar la solicitud y capturar la respuesta",
            "Validar código de estado HTTP",
            "Validar estructura y contenido del cuerpo de la respuesta",
        ],
        "criterio_aceptacion": (
            "La respuesta debe ser consistente con el escenario descrito"
        ),
    }

    return caso


@mcp.tool()
def calcular_percentil_simple(valores: list[float], percentil: float) -> float:
    """Calcula un percentil simple usando interpolación lineal
    sobre los valores en su orden original (0-indexado).

    Fórmula: posición = (percentil / 100) * (len(valores) - 1)
    Luego interpola linealmente entre los valores adyacentes.

    Args:
        valores: Lista de valores numéricos en cualquier orden.
        percentil: Percentil a calcular (0-100).

    Returns:
        Valor del percentil calculado.
    """
    if not valores:
        return 0.0

    if percentil < 0 or percentil > 100:
        raise ValueError("El percentil debe estar entre 0 y 100")

    n = len(valores)

    # Método: posición 0-indexada sobre los valores en su orden original
    r = (percentil / 100) * (n - 1)
    k = int(r)
    delta = r - k

    if k >= n - 1:
        return float(valores[-1])
    if k < 0:
        return float(valores[0])

    return round(float(valores[k] + delta * (valores[k + 1] - valores[k])), 10)


# ── Reto 1: Clasificar error HTTP ─────────────────────────────


@mcp.tool()
def clasificar_error_http(status_code: int) -> str:
    """Clasifica un código de estado HTTP en su categoría.

    Args:
        status_code: Código de estado HTTP (100-599).

    Returns:
        Categoría del código: Éxito, Redirección, Error del cliente,
        Error del servidor, o Código desconocido.
    """
    if 200 <= status_code <= 299:
        return "Éxito"
    elif 300 <= status_code <= 399:
        return "Redirección"
    elif 400 <= status_code <= 499:
        return "Error del cliente"
    elif 500 <= status_code <= 599:
        return "Error del servidor"
    else:
        return "Código desconocido"


# ── Reto 2: Evaluar SLA ───────────────────────────────────────


@mcp.tool()
def evaluar_sla(p95_ms: float, limite_ms: float) -> dict:
    """Evalúa si el percentil 95 cumple con el límite de SLA.

    Args:
        p95_ms: Valor del percentil 95 en milisegundos.
        limite_ms: Límite máximo permitido en milisegundos.

    Returns:
        Diccionario con cumplimiento y diferencia en ms.
    """
    diferencia = round(abs(p95_ms - limite_ms), 2)
    cumple = p95_ms <= limite_ms
    return {"cumple": cumple, "diferencia_ms": diferencia}


# ── Reto 3: Validar respuesta API ──────────────────────────────


@mcp.tool()
def validar_respuesta_api(
    status_code: int,
    tiempo_ms: float,
    limite_ms: float,
    tiene_token: bool,
) -> dict:
    """Valida una respuesta API contra criterios de calidad.

    Args:
        status_code: Código de estado HTTP.
        tiempo_ms: Tiempo de respuesta en milisegundos.
        limite_ms: Límite máximo de tiempo permitido.
        tiene_token: Indica si la respuesta incluye token de autenticación.

    Returns:
        Diccionario con resultado de validación y razón.
    """
    codigo_valido = 200 <= status_code <= 299
    tiempo_valido = tiempo_ms <= limite_ms

    if codigo_valido and tiempo_valido and tiene_token:
        return {
            "valido": True,
            "razon": "La respuesta cumple con todos los criterios",
        }
    else:
        errores = []
        if not codigo_valido:
            errores.append(f"Código HTTP {status_code} no es 2xx")
        if not tiempo_valido:
            errores.append(
                f"Tiempo {tiempo_ms}ms excede el límite de {limite_ms}ms"
            )
        if not tiene_token:
            errores.append("No incluye token de autenticación")
        return {"valido": False, "razon": "; ".join(errores)}


# ── Reto 4: Buscar cliente por CIP ──────────────────────────────


@mcp.tool()
def buscar_cliente(cip: str) -> dict:
    """Busca un cliente por su CIP en datos_prueba.json.

    Args:
        cip: Código de identificación del cliente (ej. CIP001).

    Returns:
        Datos del cliente o mensaje de no encontrado.
    """
    import os

    ruta = os.path.join(os.path.dirname(__file__), "datos_prueba.json")
    try:
        with open(ruta, encoding="utf-8") as f:
            clientes = json.load(f)
    except FileNotFoundError:
        return {"error": "El archivo datos_prueba.json no existe"}
    except json.JSONDecodeError:
        return {"error": "Error al leer datos_prueba.json: formato inválido"}

    cip_buscado = cip.strip().upper()
    for cliente in clientes:
        if cliente.get("cip", "").strip().upper() == cip_buscado:
            return {
                "cip": cliente["cip"],
                "nombre": cliente["nombre"],
                "email": cliente["email"],
            }

    return {"error": f"Cliente con CIP '{cip}' no encontrado"}


if __name__ == "__main__":
    mcp.run(transport="stdio")
