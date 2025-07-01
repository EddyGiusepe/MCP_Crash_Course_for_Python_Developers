# <h1 align="center"><font color="gree">MCP Crash Course for Python Developers</font></h1>

<font color="pink">Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro</font>

Este estudo foi baseado no tutorial de [Dave Ebbelaar]()


## <font color="red">`Parte 2:` Compreendendo o MCP em um nível técnico</font>

### <font color="blue">Visão geral da arquitetura do MCP</font>

O Protocolo de Contexto do Modelo segue uma arquitetura cliente-host-servidor: essa separação de preocupações permite sistemas modulares e combináveis, onde cada servidor pode se concentrar em um domínio específico (como acesso a arquivos, pesquisa na web ou operações de banco de dados).

Hosts MCP : programas como Claude Desktop, IDEs ou seu aplicativo Python que desejam acessar dados por meio do MCP
Clientes MCP : clientes de protocolo que mantêm conexões 1:1 com servidores
Servidores MCP : programas leves que expõem recursos específicos por meio do Protocolo de Contexto do Modelo padronizado (ferramentas, recursos, prompts)
Fontes de dados locais : arquivos, bancos de dados e serviços do seu computador que os servidores MCP podem acessar com segurança
Serviços remotos : sistemas externos disponíveis pela Internet (por exemplo, por meio de APIs) aos quais os servidores MCP podem se conectar
Essa separação de preocupações permite sistemas modulares e combináveis, onde cada servidor pode se concentrar em um domínio específico (como acesso a arquivos, pesquisa na web ou operações de banco de dados).




Thank God!
