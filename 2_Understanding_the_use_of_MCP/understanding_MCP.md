# <h1 align="center"><font color="gree">MCP Crash Course for Python Developers</font></h1>

<font color="pink">Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro</font>

Este estudo foi baseado no tutorial de [Dave Ebbelaar]()


## <font color="red">`Parte 2:` Compreendendo o MCP em um nível técnico</font>

### <font color="blue">Visão geral da arquitetura do MCP</font>

O Protocolo de Contexto do Modelo segue uma arquitetura `cliente-host-servidor`: essa separação de preocupações permite sistemas modulares e combináveis, onde cada servidor pode se concentrar em um domínio específico (como acesso a arquivos, pesquisa na web ou operações de banco de dados).


* `Clientes MCP`: clientes de protocolo que mantêm conexões 1:1 com servidores

* `Hosts MCP`: programas como Claude Desktop, IDEs ou seu aplicativo Python que desejam acessar dados por meio do MCP

* `Servidores MCP`: programas leves que expõem recursos específicos por meio do `Protocolo de Contexto do Modelo` padronizado (Tools, recursos, prompts)

* `Fontes de dados locais`: arquivos, bancos de dados e serviços do seu computador que os servidores MCP podem acessar com segurança

* `Serviços remotos`: sistemas externos disponíveis pela Internet (por exemplo, por meio de APIs) aos quais os servidores MCP podem se conectar

Essa separação de preocupações permite sistemas modulares e combináveis, onde cada servidor pode se concentrar em um domínio específico (como acesso a arquivos, pesquisa na web ou operações de banco de dados).


![](./print_mcp_1.png)


O MCP define três primitivas principais que os servidores podem implementar:

``1.`` [Ferramentas - Tools](https://modelcontextprotocol.io/docs/concepts/tools#python): Funções controladas por modelo que os ``LLMs`` podem invocar (como chamadas de API, cálculos, etc.)

``2.`` [Recursos - Resources](https://modelcontextprotocol.io/docs/concepts/resources#python): Dados controlados pelo aplicativo que fornecem contexto (como conteúdo de arquivo, registros de banco de dados, etc.)

``3.`` [Prompts](https://modelcontextprotocol.io/docs/concepts/prompts#python): Templates controlados pelo usuário para interações ``LLM``

Para ``desenvolvedores Python``, o primitivo mais imediatamente útil são as ferramentas, que permitem que os ``LLMs`` executem ações programaticamente.


### <font color="blue">Mecanismos de Transporte um Mergulho Profundo</font>

O MCP suporta três mecanismos principais de transporte:

`1.` `Stdio - Entrada/Saída Padrão` (Standard IO):

* A comunicação ocorre por meio de fluxos de entrada/saída padrão.
* Melhor para integrações locais quando o servidor e o cliente estão na mesma máquina.
* Configuração simples sem necessidade de configuração de rede.

`2.` `SSE - Server-Sent Events` (Eventos enviados pelo servidor):

* Usa HTTP para comunicação `cliente-servidor` e SSE para comunicação `servidor-cliente`.
* Adequado para conexões remotas entre redes.
* Permite arquiteturas distribuídas.

`3.` `Streamable HTTP` (introduzido em 24 de março de 2025) :

* Transporte de streaming moderno baseado em HTTP que substitui o `SSE`.
* Usa um ponto de extremidade (`endpoint`) unificado para comunicação bidirecional.
* `Recomendado para implantações de produção devido ao melhor desempenho e escalabilidade`.
* Suporta modos de operação com e sem estado.

Entender quando usar cada transporte (`transport`) é crucial para criar implementações eficazes de `MCP`:

* Use `Stdio` ao criar integrações de aplicativos individuais ou durante o desenvolvimento.
* Use o `SSE`  para desenvolvimento ou quando trabalhar com implementações `MCP` mais antigas.
* Use `Streamable HTTP` para implantações de produção onde você precisa do melhor desempenho e escalabilidade.


### `Comparação de Mecanismos de Transporte`


![](./comparando_mecanismos_TRANSPORT.jpeg)


Se você conhece o `FastAPI`, verá que implementar um servidor `MCP` com transportes HTTP (`SSE` e `Streamable HTTP`) é muito semelhante. Ambas as estruturas usam endpoints `HTTP` para receber solicitações e oferecer suporte a respostas em streaming. Ambas permitem definir manipuladores (`handlers`) para `routes/endpoints` específicos e fornecem padrões `async/await` para lidar com solicitações e gerar respostas. Essa similaridade facilita a transição dos desenvolvedores do `FastAPI` para a construção de servidores `MCP`, pois eles podem aproveitar seus conhecimentos existentes em `HTTP`, programação assíncrona e respostas em streaming.


### <font color="blue">Um novo padrão</font>

O verdadeiro poder do `MCP` não está na introdução de novas capacidades, mas na padronização de como essas capacidades são expostas e consumidas. Isso oferece várias vantagens importantes:

* `Reutilização` (Reusability): cria um servidor uma vez e usa-lo com qualquer cliente compatível com `MCP`.

* `Composibilidade` (Composability): combina vários servidores para criar recursos complexos.

* `Crescimento do ecossistema` (Ecosystem Growth): beneficiar-se de servidores criados por outros.


O ecossistema `MCP` já está crescendo rapidamente, com servidores disponíveis e diversas ferramentas. Você pode encontrar uma visão geral aqui: [Servidores oficialmente suportados](https://github.com/modelcontextprotocol/servers).

Isso significa que você pode aproveitar os servidores existentes em vez de reinventar a roda e contribuir com seus próprios servidores para beneficiar a comunidade.


Thank God!
