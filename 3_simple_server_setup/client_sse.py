#! /usr/bin/env python3
"""
Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro

Script client_sse.py
====================
Este script é o cliente MCP que se conecta ao servidor MCP usando o transporte SSE.

Run
---
uv run client_sse.py
"""
import asyncio
import nest_asyncio
from mcp import ClientSession
from mcp.client.sse import sse_client

nest_asyncio.apply()  # Necessário para executar python interativamente

"""
Certifique-se de:
1. O servidor (server.py) está em execução antes de executar este script.
2. O servidor (server.py) está configurado para usar o transporte SSE.
3. O servidor (server.py) está escutando na porta 8050.

Para executar o servidor:
uv run server.py
"""


async def main():
    # Conecta ao servidor usando SSE:
    async with sse_client("http://localhost:8050/sse") as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            # Inicializa a conexão:
            await session.initialize()

            # Lista as ferramentas disponíveis:
            tools_result = await session.list_tools()
            print("Ferramentas (Tools) disponíveis:")
            for tool in tools_result.tools:
                print(f"  - {tool.name}: {tool.description}")

            # Chama a ferramenta calculadora:
            # result = await session.call_tool("add", arguments={"a": 2, "b": 3})
            # print(f"2 + 3 = {result.content[0].text}")

            # Criamos nosso loop para realizar cálculos:
            while True:
                print("\n--- Calculadora Interativa com MCP ---")
                try:
                    a = int(input("Digite o primeiro número: "))
                    b = int(input("Digite o segundo número: "))

                    # Chama a ferramenta calculadora com os valores fornecidos pelo usuário:
                    result = await session.call_tool("add", arguments={"a": a, "b": b})
                    print(f"{a} + {b} = {result.content[0].text}")

                    # Perguntar se o usuário deseja continuar:
                    continuar = input("Deseja fazer outro cálculo? (s/n): ").lower()
                    if continuar != "s":
                        print("Encerrando a calculadora. Até logo!")
                        break
                except ValueError:
                    print("Erro: Por favor, digite apenas números inteiros.")
                except Exception as e:
                    print(f"Erro ao realizar o cálculo: {e}")


if __name__ == "__main__":
    asyncio.run(main())
