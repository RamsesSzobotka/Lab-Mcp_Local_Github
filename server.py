from fastmcp import FastMCP
import json

mcp = FastMCP("lab-mcp-local")


# ── Tools Base ────────────────────────────────────────────────


@mcp.tool()
def saludar(nombre: str) -> str:
    """Saluda a una persona por su nombre."""
    return f"¡Hola, {nombre}!"


@mcp.tool()
def sumar(a: int, b: int) -> int:
    """Suma dos números enteros."""
    return a + b


@mcp.tool()
def contar_palabras(texto: str) -> int:
    """Cuenta la cantidad de palabras en un texto."""
    return len(texto.split())


# ── Tools Reto ─────────────────────────────────────────────────


@mcp.tool()
def buscar_cliente(id: int) -> dict:
    """Busca un cliente por su ID en data_prueba.json."""
    try:
        with open("data_prueba.json", encoding="utf-8") as f:
            clientes = json.load(f)
    except FileNotFoundError:
        return {"error": "El archivo data_prueba.json no existe"}
    except json.JSONDecodeError:
        return {"error": "Error al leer data_prueba.json: formato inválido"}

    for cliente in clientes:
        if cliente["id"] == id:
            return {"nombre": cliente["nombre"], "email": cliente["email"]}

    return {"error": f"Cliente con id {id} no encontrado"}


@mcp.tool()
def calcular_promedio(calificaciones: list[float]) -> float:
    """Calcula el promedio de una lista de calificaciones."""
    if not calificaciones:
        return 0.0
    return sum(calificaciones) / len(calificaciones)


@mcp.tool()
def analizar_texto(texto: str) -> dict:
    """Analiza un texto y retorna cantidad de caracteres, palabras y vocales."""
    caracteres = len(texto)
    palabras = len(texto.split())
    vocales = sum(1 for c in texto.lower() if c in "aeiouáéíóúü")
    return {
        "caracteres": caracteres,
        "palabras": palabras,
        "vocales": vocales,
    }


@mcp.tool()
def generar_resumen(texto: str, n_oraciones: int = 2) -> str:
    """Genera un resumen con las primeras n oraciones del texto."""
    oraciones = [o.strip() for o in texto.split(".") if o.strip()]
    if not oraciones:
        return ""
    resumen = ". ".join(oraciones[:n_oraciones]) + "."
    return resumen


if __name__ == "__main__":
    mcp.run(transport="stdio")
