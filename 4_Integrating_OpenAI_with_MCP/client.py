#! /usr/bin/env python3
"""
Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro

Run
===
uv run client.py

NOTA:
-----
Aqui construi um cliente para interagir com o modelo OpenAI usando ferramentas MCP.
Basicamente, o cliente é responsável por enviar consultas ao servidor e receber respostas.
É como se for um sistema RAG (Retrieval-Augmented Generation), já que a base de conhecimento 
é fornecida através de ferramentas MCP. Ademais, foi necessário adicionar "system_message"
para que o modelo OpenAI possa responder apenas sobre a base de conhecimento fornecida.
"""
import asyncio
import json
from contextlib import AsyncExitStack
from typing import Any, Dict, List, Optional
import nest_asyncio
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from openai import AsyncOpenAI

# Aplica nest_asyncio para permitir loops de eventos aninhados (necessário para Jupyter/IPython):
nest_asyncio.apply()

# Carrega variáveis de ambiente:
load_dotenv("../.env")


class MCPOpenAIClient:
    """Cliente para interagir com modelos OpenAI usando ferramentas MCP."""

    def __init__(self, model: str = "gpt-4o"):
        """Inicializa o cliente OpenAI MCP.

        Args:
            model: O modelo OpenAI a ser usado.
        """
        # Inicializa objetos de sessão e cliente:
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.openai_client = AsyncOpenAI()
        self.model = model
        self.stdio: Optional[Any] = None
        self.write: Optional[Any] = None

    async def connect_to_server(self, server_script_path: str = "server.py"):
        """Conecta a um servidor MCP.

        Args:
            server_script_path: Caminho para o script do servidor.
        """
        # Configuração do servidor:
        server_params = StdioServerParameters(
            command="python",
            args=[server_script_path],
        )

        # Conecta ao servidor:
        stdio_transport = await self.exit_stack.enter_async_context(
            stdio_client(server_params)
        )
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(
            ClientSession(self.stdio, self.write)
        )

        # Inicializa a conexão:
        await self.session.initialize()

        # Lista ferramentas disponíveis:
        tools_result = await self.session.list_tools()
        print("\nConectado ao servidor com ferramentas:")
        for tool in tools_result.tools:
            print(f"  - {tool.name}: {tool.description}")

    async def get_mcp_tools(self) -> List[Dict[str, Any]]:
        """Recupera ferramentas disponíveis do servidor MCP no formato OpenAI.

        Returns:
            Uma lista de ferramentas no formato OpenAI.
        """
        tools_result = await self.session.list_tools()
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

    async def process_query(self, query: str) -> str:
        """Processa uma consulta usando OpenAI e ferramentas MCP disponíveis.

        Args:
            query: A consulta do usuário.

        Returns:
            A resposta da OpenAI.
        """
        # Recupera ferramentas disponíveis:
        tools = await self.get_mcp_tools()

        # Define o prompt de sistema para restringir às ferramentas MCP:
        system_message = {"role": "system", 
                          "content": """Você é um assistente especializado que APENAS responde 
                                        com base na base de conhecimento fornecida através das ferramentas disponíveis.

                            REGRAS IMPORTANTES:
                            1. SEMPRE use as ferramentas disponíveis para buscar informações antes de responder
                            2. Se as ferramentas NÃO retornarem informações relevantes para a pergunta, responda: "Desculpe, não encontrei informações sobre isso na minha base de conhecimento."
                            3. NUNCA use seu conhecimento geral - responda APENAS com base ao conhecimento fornecido pelas ferramentas
                            4. Seja preciso e cite apenas as informações encontradas nas ferramentas
                            5. Se uma pergunta estiver fora do escopo da base de conhecimento, seja honesto sobre isso

                            Sua base de conhecimento é limitada aos dados disponíveis através das ferramentas MCP."""
                         }

        # Chama a API OpenAI com o system message:
        response = await self.openai_client.chat.completions.create(
            model=self.model,
            messages=[system_message,
                      {"role": "user", "content": query}
                     ],
            tools=tools,
            tool_choice="auto",  # MUDANÇA 1: "None" → "auto"
        )

        # Recupera a resposta do assistente:
        assistant_message = response.choices[0].message

        # MUDANÇA 2: Incluir system_message na conversa:
        messages = [
            system_message,  # ← ADICIONADO
            {"role": "user", "content": query},
            assistant_message,
        ]

        # Trata chamadas de ferramenta se presentes:
        if assistant_message.tool_calls:
            # Processa cada chamada de ferramenta:
            for tool_call in assistant_message.tool_calls:
                # Executa chamada de ferramenta:
                result = await self.session.call_tool(
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
            final_response = await self.openai_client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=tools,
                tool_choice="none",  # Não permite mais chamadas de ferramenta
            )

            return final_response.choices[0].message.content

        # Sem chamadas de ferramenta, retorna a resposta direta:
        return assistant_message.content

    async def cleanup(self):
        """Limpa recursos."""
        await self.exit_stack.aclose()


async def main():
    """Ponto de entrada principal para o cliente."""
    client = MCPOpenAIClient()
    await client.connect_to_server("server.py")

    print("\n🤖 Cliente MCP-OpenAI está pronto!")
    print("Digite suas consultas ou 'sair' para encerrar.\n")

    try:
        while True:
            # Solicita entrada do usuário:
            query = input("💬 Sua consulta: ").strip()
            
            # Verifica se o usuário quer sair:
            if query.lower() in ['sair', 'exit', 'quit', 'q']:
                print("👋 Encerrando...")
                break
                
            # Ignora entradas vazias:
            if not query:
                continue
                
            print(f"\n🔍 Processando: {query}")
            
            try:
                response = await client.process_query(query)
                print(f"\n✅ Resposta: {response}\n")
            except Exception as e:
                print(f"\n❌ Erro ao processar consulta: {e}\n")
                
    except KeyboardInterrupt:
        print("\n👋 Interrompido pelo usuário. Encerrando...")
    finally:
        await client.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
