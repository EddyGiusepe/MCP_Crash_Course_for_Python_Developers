#! /usr/bin/env python3
"""
Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro
"""
import asyncio
import json
from contextlib import AsyncExitStack
from typing import Any, Dict, List
import nest_asyncio
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from openai import AsyncOpenAI

# Aplica nest_asyncio para permitir loops de eventos aninhados (necessário para Jupyter/IPython):
nest_asyncio.apply()

# Carrega variáveis de ambiente:
load_dotenv("../.env")

# Variáveis globais para armazenar o estado da sessão:
session = None
exit_stack = AsyncExitStack()
openai_client = AsyncOpenAI()
model = "gpt-4o"
stdio = None
write = None


async def connect_to_server(server_script_path: str = "server.py"):
    """Conectar a um servidor MCP.

    Args:
        server_script_path: Caminho para o script do servidor.
    """
    global session, stdio, write, exit_stack

    # Configuração do servidor:
    server_params = StdioServerParameters(
        command="python",
        args=[server_script_path],
    )

    # Conectar ao servidor:
    stdio_transport = await exit_stack.enter_async_context(stdio_client(server_params))
    stdio, write = stdio_transport
    session = await exit_stack.enter_async_context(ClientSession(stdio, write))

    # Inicializa a conexão:
    await session.initialize()

    # Lista as ferramentas disponíveis:
    tools_result = await session.list_tools()
    print("\nConectado ao servidor com ferramentas:")
    for tool in tools_result.tools:
        print(f"  - {tool.name}: {tool.description}")


async def get_mcp_tools() -> List[Dict[str, Any]]:
    """Recupera as ferramentas disponíveis do servidor MCP no formato OpenAI.

    Returns:
        Uma lista de ferramentas no formato OpenAI.
    """
    global session

    tools_result = await session.list_tools()
    return [
        {
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.inputSchema,
            },
        }
        for tool in tools_result.tools
    ]


async def process_query(query: str) -> str:
    """Processa uma consulta usando OpenAI e ferramentas MCP disponíveis.

    Args:
        query: A consulta do usuário.

    Returns:
        A resposta da OpenAI.
    """
    global session, openai_client, model

    # Recupera as ferramentas disponíveis:
    tools = await get_mcp_tools()

    # Chama a API OpenAI:
    response = await openai_client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": query}],
        tools=tools,
        tool_choice="auto",
    )

    # Recupera a resposta do assistente:
    assistant_message = response.choices[0].message

    # Inicializa a conversa com a consulta do usuário e a resposta do assistente:
    messages = [
        {"role": "user", "content": query},
        assistant_message,
    ]

    # Gerencia chamadas de ferramenta se presentes:
    if assistant_message.tool_calls:
        # Processa cada chamada de ferramenta:
        for tool_call in assistant_message.tool_calls:
            # Executa a chamada de ferramenta:
            result = await session.call_tool(
                tool_call.function.name,
                arguments=json.loads(tool_call.function.arguments),
            )

            # Adiciona a resposta da ferramenta à conversa:
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result.content[0].text,
                }
            )

        # Recupera a resposta final da OpenAI com os resultados das ferramentas:
        final_response = await openai_client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            tool_choice="none",  # Não permite mais chamadas de ferramenta
        )

        return final_response.choices[0].message.content

    # Sem chamadas de ferramenta, apenas retorna a resposta direta:
    return assistant_message.content


async def cleanup():
    """Limpa os recursos."""
    global exit_stack
    await exit_stack.aclose()


async def main():
    """Ponto de entrada principal para o cliente."""
    print("🤖 Cliente MCP Interativo - Digite suas consultas sobre a base de conhecimento da Empresa!")
    print("Digite 'sair' ou 'quit' para encerrar a sessão.\n")
    
    try:
        await connect_to_server("server.py")
        
        while True:
            # Solicita entrada do usuário:
            query = input("\n💬 Sua consulta: ").strip()
            
            # Verifica se o usuário quer sair:
            if query.lower() in ['sair', 'quit', 'exit', 'q']:
                print("\n👋 Encerrando sessão. Até logo!")
                break
            
            # Verifica se a entrada não está vazia:
            if not query:
                print("⚠️  Por favor, digite uma consulta válida.")
                continue
            
            print(f"\n🔍 Processando: {query}")
            print("⏳ Aguarde...")
            
            try:
                response = await process_query(query)
                print(f"\n✅ Resposta:\n{response}")
            except Exception as e:
                print(f"\n❌ Erro ao processar a consulta: {e}")
                
    except KeyboardInterrupt:
        print("\n\n⚡ Interrompido pelo usuário.")
    except Exception as e:
        print(f"\n❌ Erro na conexão: {e}")
    finally:
        await cleanup()


if __name__ == "__main__":
    asyncio.run(main())
    