# <h1 align="center"><font color="gree">MCP Crash Course for Python Developers</font></h1>

<font color="pink">Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro</font>

Este estudo foi baseado no tutorial de [Dave Ebbelaar]()

## <font color="red">`Parte 4:` Comparando o MCP com abordagens tradicionais</font>

### <font color="blue">Comparação lado a lado</font>
Vamos comparar nossa implementação de MCP com uma abordagem tradicional de chamada de função em `function-calling.py`.

Nesta pequena escala, a abordagem tradicional é mais simples. As principais diferenças tornam-se aparentes quando:

``1.`` Aumento de escala (``Scale increases``): Com dezenas de ferramentas, a abordagem MCP proporciona melhor organização

``2.`` A reutilização é importante (``Reuse matters``): o servidor MCP pode ser usado por vários clientes e aplicativos

``3.`` A distribuição é necessária (``Distribution is required``): o MCP fornece mecanismos padrão para operação remota

### <font color="blue">Quando usar MCP em comparação com abordagens tradicionais</font>

#### <font color="yellow">Considere MCP quando:</font>

* Você precisa compartilhar implementações de ferramentas em vários aplicativos
* Você está construindo um sistema distribuído com componentes em diferentes máquinas
* Você deseja aproveitar os servidores MCP existentes do ecossistema
* Você está construindo um produto onde a padronização oferece benefícios ao usuário

#### <font color="yellow">As abordagens tradicionais podem ser melhores quando:</font>

* Você tem um aplicativo mais simples e independente
* O desempenho é crítico (chamadas de função diretas têm menos sobrecarga)
* Você está no início do desenvolvimento e a iteração rápida é mais importante do que a padronizaçã





Thank God 🤓!
