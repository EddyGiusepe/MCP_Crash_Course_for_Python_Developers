#! /usr/bin/env python3
"""
Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro

Script server.py
================
Este script é um servidor MCP (Model Context Protocol) que implementa
uma ferramenta simples de calculadora.

Run
---
* Executando só o server.py ---> mcp dev server.py

ou

* uv run server.py

NOTA:
Não esqueça de deixar rodando este script, pois ele é o servidor MCP.
Ao executar este script você terá a seguinte endpoint:
http://localhost:8050/
"""
from mcp.server.fastmcp import FastMCP


# Cria um servidor MCP:
mcp = FastMCP(
    name="Calculator",
    host="0.0.0.0",  # Apenas usado para transporte SSE (localhost)
    port=8050,  # Apenas usado para transporte SSE (defina qualquer porta)
    stateless_http=True,
)


# Adiciona uma ferramenta simples de calculadora:
@mcp.tool()
def add(a: int, b: int) -> int:
    """Soma dois números"""
    return a + b


# Executa o servidor:
if __name__ == "__main__":
    # transport = "sse"
    # transport = "stdio"
    transport = "streamable-http"
    if transport == "stdio":
        print("Executando servidor com transporte stdio")
        mcp.run(transport="stdio")
    elif transport == "sse":
        print("Executando servidor com transporte SSE")
        mcp.run(transport="sse")
    elif transport == "streamable-http":
        print("Executando servidor com transporte Streamable HTTP")
        mcp.run(transport="streamable-http")
    else:
        raise ValueError(f"Transporte desconhecido: {transport}")
