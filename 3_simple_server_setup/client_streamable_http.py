#! /usr/bin/env python3
"""
Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro

Run
---
uv run client_streamable_http.py

NOTA: Não esqueça de estar rodando o script server.py em outro terminal.
"""
import asyncio
import nest_asyncio
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client


async def main():
    # Conectando ao servidor usando Streamable HTTP:
    async with streamablehttp_client("http://localhost:8050/mcp") as (
        read_stream,
        write_stream,
        get_session_id,
    ):
        async with ClientSession(read_stream, write_stream) as session:
            # Inicializando a conexão:
            await session.initialize()

            # Listando as ferramentas disponíveis:
            tools_result = await session.list_tools()
            print("Ferramentas disponíveis:")
            for tool in tools_result.tools:
                print(f"  - {tool.name}: {tool.description}")

            # Chamando a ferramenta de calculadora:
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
