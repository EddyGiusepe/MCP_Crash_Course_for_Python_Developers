#! /usr/bin/env python3
"""
Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro

Script client_sse.py
====================

Run
---

"""
import asyncio
import nest_asyncio
from mcp import ClientSession
from mcp.client.sse import sse_client

nest_asyncio.apply()  # Necessário para executar python interativamente

"""
Certifique-se de:
1. O servidor está em execução antes de executar este script.
2. O servidor está configurado para usar o transporte SSE.
3. O servidor está escutando na porta 8050.

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
            print("Available tools:")
            for tool in tools_result.tools:
                print(f"  - {tool.name}: {tool.description}")

            # Chama a ferramenta calculadora:
            result = await session.call_tool("add", arguments={"a": 2, "b": 3})
            print(f"2 + 3 = {result.content[0].text}")


if __name__ == "__main__":
    asyncio.run(main())
    