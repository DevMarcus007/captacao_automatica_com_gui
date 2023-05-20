# Aplicação de Verificação de Postagem Automática

## Descrição do problema

Com a necessidade de verificar se houve algum objeto que não teve postagem automática, foi desenvolvida essa aplicação. O objetivo era acessar a página de controle de leitura automática do sistema MIS (Management Information System) e verificar os objetos que foram passados em determinada rampa e horário. Em seguida, era necessário consultar o sistema SRO (Sistema de Rastreamento de Objetos) para verificar se houve a efetiva postagem desses objetos. Caso não houvesse a postagem registrada no SRO, era necessário consultar o sistema SVP(Sistema de Validação de Postagem) para obter os dados do cliente e realizar a conferência e conciliação da postagem.

O desafio estava no fato de que nenhum dos três sistemas fornecia relatórios prontos para consulta. Portanto, foi necessário utilizar técnicas de web scraping para obter os dados necessários, além de aplicar tratamento de dados para formatar e relacionar as informações obtidas.

## Solução desenvolvida

Foi desenvolvida uma aplicação desktop utilizando Python e a biblioteca Tkinter para criar a interface gráfica. A aplicação permite ao usuário selecionar a data, horário de início e fim, e as rampas desejadas. Com base nessas informações, a aplicação realiza as consultas nos sistemas MIS, SRO e SVP para verificar as postagens automáticas.

Através do web scraping, a aplicação acessa a página de controle de leitura automática do sistema MIS, coleta os objetos registrados nas rampas e horários selecionados. Em seguida, realiza consultas no sistema SRO para verificar se esses objetos foram postados. Caso não haja postagem registrada, a aplicação acessa o sistema SVP para obter os dados do cliente e realizar a conciliação da postagem.

A aplicação utiliza técnicas de tratamento de dados para formatar as informações obtidas dos sistemas e apresenta os resultados ao usuário de forma clara e organizada. Além disso, a aplicação permite exportar os resultados para um arquivo Excel, facilitando o armazenamento e análise posterior.

Com essa solução, foi possível automatizar o processo de verificação de postagem automática e agilizar a identificação de objetos que não foram corretamente postados. Isso contribui para a melhoria da eficiência e qualidade dos serviços prestados pelo GCCAP.


## Tecnologias utilizadas

- Python: Linguagem de programação utilizada para o desenvolvimento do aplicativo.
- Tkinter: Biblioteca padrão do Python para a criação de interfaces gráficas.
- tkcalendar: Biblioteca que fornece um widget de calendário para seleção de datas.
- PIL (Python Imaging Library): Biblioteca utilizada para manipulação de imagens, utilizada para exibir a logo do aplicativo.
- Selenium: Biblioteca utilizada para automatizar a interação com sistemas web, utilizada para realizar consultas em sistemas externos.
- Openpyxl: Biblioteca utilizada para manipulação de arquivos do Excel, utilizada para exportar os resultados das consultas para um arquivo Excel.
- Xlsxwriter: Biblioteca utilizada para criar arquivos Excel com formatação, utilizada para exportar os resultados das consultas para um arquivo Excel.


**Observação**: Foi criado um executável da aplicação, para utilização outras máquinas. O arquivo `chromedriver.exe` foi incluído no build juntamente com as dependências necessárias.
