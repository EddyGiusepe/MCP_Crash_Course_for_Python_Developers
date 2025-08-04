# <h1 align="center"><font color="gree">MCP Crash Course for Python Developers</font></h1>

<font color="pink">Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro</font>

Este estudo foi baseado no tutorial de [Dave Ebbelaar]()


## <font color="red">`Parte 3:` Configuração simples do servidor com o Python SDK</font>


### <font color="blue">Construindo nosso primeiro servidor MCP</font>

Vamos criar um servidor de demonstração simples com uma tool:

```python
# server.py
from mcp.server.fastmcp import FastMCP

# Criando um servidor MCP:
mcp = FastMCP("DemoServer")

# Ferramenta simples:
@mcp.tool()
def say_hello(name: str) -> str:
    """Diz oi para alguém

    Args:
        name: O nome da pessoa a ser cumprimentada
    """
    return f"Olá, {name}! É um prazer te conhecer."

# Executando o servidor:
if __name__ == "__main__":
    mcp.run()
```

### <font color="blue">Executando o servidor</font>
Existem várias maneiras de executar seu servidor MCP:

#### <font color="yellow">`1.` Modo de desenvolvimento com MCP Inspector</font>

A maneira mais fácil de testar seu servidor é usando o MCP Inspector:

```bash
mcp dev server.py
```
Isso executa seu servidor localmente e o conecta ao `MCP Inspector`, uma ferramenta web que permite interagir diretamente com as ferramentas e recursos do seu servidor. Isso é ótimo para testes. A imagem abaixo mostra o MCP Inspector em ação.

![](./running_only_server_DEV.png)


#### <font color="yellow">`2.` Integração com o Claude Desktop</font>
Se você tiver o `Claude Desktop` instalado, poderá instalar seu servidor para usar com o `Claude`:

```bash
mcp install server.py
```
Isso adicionará seu servidor à configuração do `Claude Desktop`, tornando-o disponível para Claude.


#### <font color="yellow">`3.` Execução Direta (somente necessária ou SSE)</font>
Você também pode executar o servidor diretamente:

```bash
# Método 1: Executando como um script Python
python server.py

# Método 2: Usando UV (recomendado)
uv run server.py
```

### <font color="blue">O que acontece quando você executa um servidor MCP?</font>
Quando você executa um servidor MCP:

``1.`` O servidor é inicializado com as capacidades que você definiu (ferramentas, recursos, etc.)

``2.`` Ele começa a escutar conexões em um transporte específico

Por padrão, os servidores MCP não usam uma porta de servidor web tradicional. Em vez disso, eles usam:

- ``stdio transport``: O servidor se comunica por meio de entrada e saída padrão (o padrão para ``mcp run`` e integração com o Claude Desktop)

- ``SSE transport``: para comunicação baseada em ``HTTP`` (usado quando configurado explicitamente)

Se você quiser expor seu servidor via ``HTTP`` com uma porta específica, você precisa modificar seu servidor para usar o transporte SSE:

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("MyServer", host="127.0.0.1", port=8050)

# Adicione suas ferramentas e recursos aqui...

if __name__ == "__main__":
    # Executar com o transporte SSE na porta 8050
    mcp.run(transport="sse")
```	

Então você pode executá-lo com:

```bash
python server.py     ou     uv run server.py
```
Isso iniciará seu servidor em ``http://127.0.0.1:8050``.


### <font color="blue">Implementação do lado do cliente (com Standard I/O)</font>
Agora, vamos ver como criar um cliente que utiliza nosso servidor:

```python
import asyncio
import nest_asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    # Define os parâmetros do server:
    server_params = StdioServerParameters(
        command="python",  # O comando para executar seu servidor
        args=["server.py"],  # Argumentos para o comando
    )

    # Conectando ao servidor:
    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            # Inicializando a conexão:
            await session.initialize()

            # Listando as ferramentas disponíveis:
            tools_result = await session.list_tools()
            print("Ferramentas disponíveis:")
            for tool in tools_result.tools:
                print(f"  - {tool.name}: {tool.description}")

            # Chamando a ferramenta de calculadora:
            result = await session.call_tool("add", arguments={"a": 2, "b": 3})
            print(f"2 + 3 = {result.content[0].text}")


if __name__ == "__main__":
    asyncio.run(main())
```
Este cliente:

``1.`` Cria uma conexão com nosso servidor via ``stdio``

``2.`` Estabelece uma sessão ``MCP``

``3.`` Lista as ferramentas disponíveis

``4.`` Chama a ferramenta ``add`` com argumentos


### <font color="blue">Implementação do lado do cliente (com Server-Sent Events)</font>
Veja como se conectar ao seu servidor com SSE:
```python
import asyncio
import nest_asyncio
from mcp import ClientSession
from mcp.client.sse import sse_client

async def main():
    # Conectando ao servidor usando SSE:
    async with sse_client("http://localhost:8050/sse") as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            # Inicializando a conexão:
            await session.initialize()

            # Listando as ferramentas disponíveis:
            tools_result = await session.list_tools()
            print("Ferramentas disponíveis:")
            for tool in tools_result.tools:
                print(f"  - {tool.name}: {tool.description}")

            # Chamando a ferramenta de calculadora:
            result = await session.call_tool("add", arguments={"a": 2, "b": 3})
            print(f"2 + 3 = {result.content[0].text}")


if __name__ == "__main__":
    asyncio.run(main())
```



### <font color="blue">Implementação do lado do cliente (com HTTP Streamable) - NOVO</font>
>> Observação: o transporte HTTP Streamable foi introduzido em 24 de março de 2025 e agora é a abordagem recomendada para implantações de produção, substituindo o transporte SSE. Saiba mais na [documentação oficial](https://modelcontextprotocol.io/specification/2025-03-26/basic/transports#streamable-http).


#### <font color="yellow">Por que Streamable HTTP?</font>

O ``HTTP Streamable``: Oferece diversas vantagens em relação ao ``SSE``:

- ``Melhor desempenho``: Melhoria de 3 a 5x em alta simultaneidade

- ``Arquitetura simplificada``: Endpoint único em vez de endpoints ``HTTP + SSE`` separados

- ``Escalabilidade aprimorada``: Melhor suporte para implantações de vários nós

- ``Padrões modernos``: Construídos com base nos padrões atuais de streaming ``HTTP``

#### <font color="yellow">Como funciona:</font>

O ``Streamable HTTP`` utiliza uma única endpoint ``HTTP`` (``/mcp``) que suporta ambos os modos de operação com e sem estado. Ao contrário do ``SSE``, que exige a manutenção separada da endpoint, o ``Streamable HTTP`` fornece uma interface unificada para toda a comunicação ``MCP``.

Veja como se conectar usando o novo ``Transport HTTP Streamable``:

```python
import asyncio
import nest_asyncio
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

async def main():
    # Conectando ao servidor usando Streamable HTTP:
    async with streamablehttp_client("http://localhost:8050/mcp") as (read_stream, write_stream, get_session_id):
        async with ClientSession(read_stream, write_stream) as session:
            # Inicializando a conexão:
            await session.initialize()

            # Listando as ferramentas disponíveis:
            tools_result = await session.list_tools()
            print("Ferramentas disponíveis:")
            for tool in tools_result.tools:
                print(f"  - {tool.name}: {tool.description}")

            # Chamando a ferramenta de calculadora:
            result = await session.call_tool("add", arguments={"a": 2, "b": 3})
            print(f"2 + 3 = {result.content[0].text}")


if __name__ == "__main__":
    asyncio.run(main())
```

#### <font color="yellow">Principais diferenças do SSE</font>

| Transport SSE                        | Transport Streamable HTTP |
|--------------------------------------|---------------------------|
| Endpoint `/sse`                      | Endpoint `/mcp`          |
| Retorna 2 valores: (`read`, `write`) | Retorna 3 valores: (`read`, `write`, `get_session_id`) |
| Separate HTTP + SSE streams          | Streaming ``HTTP`` unificado |
| Bom para o Desenvolvimento           | Recomendado para Produção |


### <font color="blue">Qual abordagem você deve escolher?</font>
* ``Use stdio`` se o seu cliente e o servidor forem executados no mesmo processo ou se você estiver iniciando o processo do servidor diretamente do seu cliente.

* Use o ``Streamable HTTP`` para implantações de produção onde você precisa do melhor desempenho e escalabilidade.

* Use o ``SSE`` para desenvolvimento ou ao trabalhar com implementações MCP mais antigas que ainda não oferecem suporte ao ``Streamable HTTP``.


Para a maioria das integrações de ``backend de produção``, a abordagem ``Streamable HTTP`` oferece o melhor desempenho e arquitetura moderna, enquanto ``stdio`` pode ser mais simples para sistemas de desenvolvimento ou fortemente acoplados.
