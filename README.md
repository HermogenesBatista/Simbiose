# Simbiose

O Funcionamento do programa é baseado em 3 classes, sendo 2 para gerenciar as conexões (ConectCassandra, ConnectElasticsearch), e outra para gerenciar as funcionalidades básicas de manipulação de data, tempo e existência dos IDs (Sincronizar).

No arquivo syncdb.py, é gerenciado as configurações, ele executa um loop infinito, caso seja digitado um tempo (em segundos) errado ou apenas teclado "ENTER", ele configura o tempo para 5 segundos entre uma execução e outra.
Inicialmente, é feita uma consulta em ambos os bancos, caso um deles esteja vazio, os dados vão ser primeiramente clonados para o outro. Se existir dados em ambos os bancos, o processo se inicia:

0 - Os dados do Elasticsearch são previamente preparados para a inserção no Cassandra (ConnectElasticsearch.prepare_to_cassandra())

1 - É preparado uma lista iterável com os Ids de ambos os bancos, sendo possível assim, verificar a existência de mesmos IDs, sem a necessidade de uma nova consulta;

2 - Inicia o processo pela comparação dos IDs, vindo do Cassandra com o Elasticsearch;

3 - Caso o ID exista, a data é convertida para um objeto datetime, adaptando especialmente a data vinda do Elasticsearch que trata-se de um datetime serializado.

4 - Prevalecendo a maior data, os dados são importados para o outro banco, atenção especial aos métodos:

    4.1 - ConectCassandra.received_to_elasticsearch(dados), que recebe o dado tratado do Elasticsearch, em seguida, aplica a chamada do método ConectCassandra.create_query(type_query='INSERT', table, dados), gerando um comando CQL, para inserir dados, levando em consideração as colunas recebidas na query do Elasticsearch, transformando a data e serializando o UUID recebido, antes de inserir no banco;
    
    4.2 - ConnectElasticsearch.received_to_cassandra(type, dados), transformando os dados em um array, com o primeiro índice para o ID, evitando assim que ele faça parte das colunas do registro no Elasticsearch.
    
5 - Inicia o processo de inserção dos dados não encontrados no estado atual da query no Elasticsearch, ignorando os Ids já inseridos.

6 - É exibido o tempo final, aguarda expirar o prazo estipulado no ínico da execução e retorna a verificar os dados

Descrição das Classes e métodos:

Class ConectCassandra

A Classe não foi preparada para receber os hosts que possam estar rodando, inicialmente, ela foi criada para rodar numa aplicação local, sendo necessário um melhoramento posterior.

ConectCassandra.conect()
- Estabelece uma conexão, setando o keyspace que será executada as consultas.

ConectCassandra.exect(self, consulta, user='')
- Executa uma consulta, caso o parâmetro "user" não seja passado, irá executar a query passada no parâmetro "consulta" sem fazer atribuição de valores;

ConectCassandra.create_queryself, type_query='SELECT', table='', dados=''):
- Cria um comando CQL, default é a criação de um "SELECT" levando em consideração unicamente o ID, sendo necessário passar uma lista com 2 índices. Onde [0] será a(s) Primary Key (PK), neste "Case" somente temos o ID, mas está preparada para outros indices.
- Caso o parâmetro seja um "INSERT", é criado um INSERT, seguindo a lógica acima citada, mas levando em consideração os dados existentes nos 2 índices.

ConectCassandra.received_to_elasticsearch(self, dados):
- Prepara os dados recebidos do Elasticsearch para que possam ser inseridos no Cassandra sem grandes problemas, como citado mais acima nesta documentação.

ConectCassandra.formata_datetime(self, data):
- Semelhante a classe Sincronizar, ele trata a data, para que possa transformar num objeto datetime e posteriormente ser adicionado no Cassandra, chamado no método "ConectCassandra.received_to_elasticsearch".


Class ConnectElasticsearch
A Classe não foi preparada para receber os hosts que possam estar rodando, inicialmente, ela foi criada para rodar numa aplicação local, sendo necessário um melhoramento posterior.

ConnectElasticsearch.insert_dados(self, type, values, key=uuid.uuid4()):
- Insere os dados e retorna se o dado foi inserido, caso a key não seja passada, ele gera um UUID e insere como chave.

ConnectElasticsearch.get_dados(self, type, values='', key='', sizes=1000):
- Obs: Default de retorno dos dados está configurado para 1000 registros, ainda não identifiquei uma forma de trazer todos os dados do banco, necessário mais pesquisas.
- Se a chave não for passada, ele busca todos os dados do banco, validando se existe dados.
- Busca por um filtro específico, exceto ID, não foi implementado.

ConnectElasticsearch.prepare_to_cassandra(self, row={}):
- Retorna uma lista de dados preparada para a inserção no Cassandra, sendo necessário poucos ajustes para a inserção dos mesmo, ao agir em conjunto com o método ConectCassandra.received_to_elasticsearch.


class Sincronizar:
- Classe crada para efetuar algumas operações básicas e armazenar o tempo que o script executará o novo ciclo da sincronização.

Sincronizar.verifica_data(self, data1, data2):
- Avalia as datas passadas, 1 = data2 é maior, 2 = são datas iguais, 3 = data1 é maior;

Sincronizar.transf_datetime(self, data):
- Metodo criado para tratar as datas serializadas vindas do Elasticsearch;

Sincronizar.iterable_resources(self, dados):
- Criar uma lista isolando os IDs, com os dados previamente tratados para o formato Cassandra. Desta forma permitindo fazer uma busca pelo ID diretamente da consulta, sendo desnecessario fazer uma consulta no outro banco verificando a existência.

Sincronizar.exist_id(self, search, lista):
- Complementar a lista criada acima, verifica se o ID existe e retorna o índice do mesmo, para que possa ser usado na recuperação dos dados.


Diretório Exemples:

- Arquivos criados para experimentação do código e geração de dados nos bancos, em especial os arquivos:
    - "main2.py" para inserir os dados de modo aleatório, sendo possível duplicar os dados, de forma randomica nos 2 bancos.
    - "createKeyspace.py" criar o keyspace e a tabela no Cassandra.
    - "doc.txt" usado para saber quais foram os IDs duplicados e assim verificar com mais clareza se o programa está realmente sincronizando os bancos.
- 

