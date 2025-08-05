# <h1 align="center"><font color="gree">MCP Crash Course for Python Developers</font></h1>

<font color="pink">Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro</font>

Este estudo foi baseado no tutorial de [Dave Ebbelaar]()


## <font color="red">Integração OpenAI com MCP</font>

Esta seção demonstra como integrar o ``Model Context Protocol (MCP)`` com a API do ``OpenAI`` para criar um sistema onde a ``OpenAI`` pode acessar e usar ferramentas fornecidas pelo seu ``servidor MCP``.

### <font color="blue">Visão geral</font>

Este exemplo mostra como:

``1.`` Criar um ``servidor MCP`` que exponha uma ferramenta de base de conhecimento

``2.`` Conectar a ``OpenAI`` ao ``servidor MCP``

``3.`` Permitir que a ``OpenAI`` use as ferramentas dinamicamente ao responder às consultas dos usuários

### <font color="blue">Métodos de conexão</font>

Este exemplo usa o ``transporte stdio`` para comunicação entre o ``cliente`` e o ``servidor``, o que significa:

* O ``cliente`` e o ``servidor`` são executados no mesmo processo

* O ``cliente`` inicia diretamente o ``servidor`` como um subprocesso

* Nenhum processo de ``servidor`` separado é necessário

Se você quiser dividir o ``cliente`` e o ``servidor`` em aplicativos separados (por exemplo, executando o ``servidor`` em uma máquina diferente), precisará usar o ``transporte SSE`` (Eventos Enviados pelo Servidor) . Para obter detalhes sobre como configurar uma conexão ``SSE``, consulte a seção [Configuração Simples do Servidor](https://github.com/daveebbelaar/ai-cookbook/tree/main/mcp/crash-course/3-simple-server-setup).

### <font color="blue">Explicação do fluxo de dados</font>

``1.`` ``Consulta do usuário`` (User Query): O usuário envia uma consulta ao sistema (por exemplo, ``"Qual é a política de férias da nossa empresa?"``)

``2.`` ``API OpenAI`` (OpenAI API): ``OpenAI`` recebe a consulta e as ferramentas disponíveis do ``servidor MCP``

``3.`` ``Seleção de ferramentas`` (Tool Selection): ``OpenAI`` decide quais ferramentas usar com base na consulta

``4.`` ``Cliente MCP`` (MCP Client): O ``cliente`` recebe a solicitação de chamada da ferramenta da ``OpenAI`` e a encaminha para o ``servidor MCP``

``5.`` ``Servidor MCP`` (MCP Server): O ``servidor`` executa a ferramenta solicitada (por exemplo, ``recuperando dados da base de conhecimento``)

``6.`` ``Fluxo de resposta`` (Response Flow): o resultado da ferramenta flui de volta através do ``cliente MCP`` para a ``OpenAI``

``7.`` ``Resposta final`` (Final Response): ``OpenAI`` gera uma resposta final incorporando os dados da ferramenta



## <font color="red">Como a OpenAI executa as ferramentas (Tools)</font>

O mecanismo de chamada de função da ``OpenAI`` funciona com ferramentas MCP por meio destas etapas:

``1.`` ``Registro de ferramentas`` (Tool Registration): o ``cliente MCP`` converte ferramentas MCP para o formato de função da ``OpenAI``

``2.`` ``Escolha de ferramentas`` (Tool Choice): a ``OpenAI`` decide quais ferramentas usar com base na consulta do usuário

``3.`` ``Execução da ferramenta`` (Tool Execution): o ``cliente MCP`` executa as ferramentas selecionadas e retorna os resultados

``4.`` ``Integração de contexto`` (Context Integration): a ``OpenAI`` incorpora os resultados da ferramenta em sua resposta

## <font color="red">O papel do MCP</font>

O ``MCP`` serve como uma ponte padronizada entre os modelos de ``IA`` e seus sistemas de backend:

* ``Padronização`` (Standardization): O MCP fornece uma interface consistente para modelos de IA interagirem com ferramentas

* ``Abstração`` (Abstraction): O MCP abstrai a complexidade dos seus sistemas de backend

* ``Segurança`` (Security): O MCP permite que você controle exatamente quais ferramentas e dados são expostos aos modelos de IA

* ``Flexibilidade`` (Flexibility): você pode alterar sua implementação de backend sem alterar a integração de IA

## <font color="red">Detalhes de implementação</font>

### <font color="blue">Servidor (``server.py``)</font>

O ``servidor MCP`` expõe uma ferramenta ``get_knowledge_base`` que recupera pares de ``Q&A`` de um arquivo ``JSON``.

### <font color="blue">Cliente (``client.py``)</font>

O ``cliente``:

``1.`` Conecta-se ao ``servidor MCP``

``2.`` Converte ferramentas MCP para o formato de função da ``OpenAI``

``3.`` Gerencia a comunicação entre a ``OpenAI`` e o ``servidor MCP``

``4.`` Processa os resultados das ferramentas e gera respostas finais

### <font color="blue">Base de 	Conhecimento ``(data/kb.json``)</font>

Contém pares de ``Q&A`` sobre políticas da empresa que podem ser consultadas por meio do ``servidor MCP``.

## <font color="red">Executando o Exemplo</font>

``1.`` Certifique-se de ter as dependências necessárias instaladas

``2.`` Configure sua chave de ``API OpenAI`` no arquivo ``.env``

``3.`` Execute o cliente: ``	python client.p``y

``Observação:`` com o ``transporte stdio`` usado neste exemplo, você não precisa executar o servidor separadamente, pois o cliente o iniciará automaticamente.





Thank God 🤓!
