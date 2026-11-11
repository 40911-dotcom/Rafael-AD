API de Upload e Download de Arquivos
API REST desenvolvida em Python com Flask para receber arquivos enviados por requisições HTTP e disponibilizá-los para download. Os arquivos aceitos são armazenados localmente no diretório uploads/.
Funcionalidades
- Receber arquivos por meio de requisições POST usando multipart/form-data.
- Validar a extensão do arquivo enviado.
- Aplicar uma verificação de tamanho da requisição.
- Sanitizar o nome do arquivo antes de salvá-lo.
- Registrar tentativas de upload e o IP de origem em uploads.log.
- Disponibilizar os arquivos armazenados por meio de uma rota de download.
- Inicializar uma estrutura SQLite para metadados de uploads.
Tecnologias utilizadas
- Python
- Flask
- Werkzeug
- SQLite
Estrutura do projeto
Rafael-AD/
├── app.py
├── controllers/
│   ├── download_controller.py
│   └── upload_controller.py
├── database/
│   └── db.py
├── models/
│   └── download_model.py
├── routes/
│   ├── download_route.py
│   └── upload_route.py
├── uploads/
├── database.db
└── uploads.log
Responsabilidades dos diretórios e arquivos:
- app.py: cria a aplicação Flask, configura a pasta de uploads, inicializa o banco de dados e registra as rotas.
- routes/: define os endpoints da API e direciona as requisições aos controllers.
- controllers/: implementa as operações de upload e download.
- models/: contém a consulta find_by_filename, usada para pesquisar um arquivo pelo nome no banco de dados.
- database/: estabelece a conexão SQLite e cria a tabela uploads.
- uploads/: armazena os arquivos enviados.
- database.db: banco de dados SQLite criado pela aplicação.
- uploads.log: arquivo de registro das operações de upload.
Requisitos
- Python 3 instalado.
- Flask instalado.
O Werkzeug é instalado como dependência do Flask. O projeto não inclui um arquivo requirements.txt.
Instalação e execução
1. Abra um terminal na pasta do projeto, onde está localizado o arquivo app.py.
2. (Recomendado) Crie e ative um ambiente virtual:
   Windows:
   python -m venv .venv
   .venv\Scripts\activate
   Linux/macOS:
   python3 -m venv .venv
   source .venv/bin/activate
3. Instale o Flask:
   pip install Flask
4. Inicie a aplicação:
   python app.py
Por padrão, o Flask disponibiliza a aplicação em:
http://127.0.0.1:5000
A aplicação cria o diretório uploads/, caso ele ainda não exista, e inicializa a tabela SQLite ao iniciar. Execute o comando a partir da pasta do projeto para que os caminhos relativos dos arquivos sejam resolvidos conforme esperado.
Endpoints
1. Enviar arquivo
Envia um arquivo para a API e salva o arquivo aprovado no diretório uploads/.
Informação	Valor
Método	POST
Caminho	/uploads/upload
URL local	http://127.0.0.1:5000/uploads/upload
Tipo de conteúdo	multipart/form-data
Campo do arquivo	file
Sucesso	200 OK
Falha de validação	400 Bad Request


Exemplo com cURL:
curl -X POST \
  -F "file=@./documento.pdf" \
  http://127.0.0.1:5000/uploads/upload
O campo enviado deve se chamar file.

Resposta de sucesso — 200 OK:
{
  "mensagem": "Arquivo salvo com sucesso!",
  "arquivo": "documento.pdf"
}
Possíveis respostas de erro — 400 Bad Request:

Arquivo não enviado:
{
  "erro": "Nenhum arquivo enviado"
}
Nome do arquivo vazio:
{
  "erro": "Nome do arquivo vazio"
}
Arquivo acima do limite verificado:
{
  "erro": "Arquivo excede o tamanho máximo permitido (15 KB)"
}
Extensão não permitida:
{
  "erro": "Tipo de arquivo não permitido!",
  "tipos_permitidos": ["png", "jpg", "jpeg", "gif", "pdf", "txt"]
}
A ordem dos itens em tipos_permitidos pode variar, pois a lista é construída a partir de um conjunto (set).

Extensões aceitas: .png, .jpg, .jpeg, .gif, .pdf e .txt. A comparação da extensão não diferencia letras maiúsculas de minúsculas.
2. Baixar arquivo
Retorna um arquivo armazenado no diretório uploads/ como anexo para download.
Informação	Valor
Método	GET
Caminho	/downloads/download/<filename>
Exemplo local	http://127.0.0.1:5000/downloads/download/documento.pdf
Sucesso	200 OK
Arquivo inexistente	404 Not Found


Substitua <filename> pelo nome do arquivo que foi salvo no upload.

Exemplo com cURL:
curl -X GET \
  http://127.0.0.1:5000/downloads/download/documento.pdf \
  --output documento.pdf
Em caso de sucesso, a resposta contém o arquivo, e não um objeto JSON. O controller utiliza send_from_directory com as_attachment=True.

O controller tenta tratar FileNotFoundError e retornar:
{
  "error": "Arquivo não encontrado"
}
Observação sobre o erro 404: o send_from_directory do Werkzeug normalmente sinaliza arquivo inexistente com uma exceção HTTP NotFound, que não é a mesma exceção FileNotFoundError capturada no controller. Assim, dependendo do tratamento padrão do Flask, o corpo da resposta 404 pode não ser o JSON mostrado acima.
Regras e validações do upload
- A requisição precisa conter um arquivo no campo file.
- O nome do arquivo não pode estar vazio.
- A extensão precisa pertencer à lista de extensões permitidas.
- O nome é processado por secure_filename antes de ser usado no caminho de armazenamento.
- O controller define TAMANHO_MAXIMO_ARQUIVO como 30 * 1024 bytes (30 KiB) e compara esse valor com request.content_length.
Atenção ao limite de tamanho: a verificação utiliza o tamanho total informado para a requisição HTTP, que inclui os dados de multipart/form-data, e não mede diretamente apenas o conteúdo do arquivo. Além disso, o código retorna uma mensagem que menciona 15 KB, embora a constante esteja configurada para 30 KiB. Esta documentação registra o comportamento encontrado no código; não altera essa configuração.
Banco de dados
Na inicialização, database/db.py cria a tabela uploads, caso ela ainda não exista:
CREATE TABLE IF NOT EXISTS uploads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT UNIQUE NOT NULL,
    filepath TEXT NOT NULL
);
O arquivo models/download_model.py contém o método DownloadModel.find_by_filename(filename), que consulta essa tabela pelo nome do arquivo.

Estado atual da implementação: a rotina de upload não insere registros na tabela, e o controller de download não utiliza o model para localizar os arquivos. Portanto, o fluxo atual trabalha diretamente com os arquivos no diretório uploads/; a tabela e o método de consulta estão presentes, mas não participam do fluxo principal implementado.
Logs
As operações de upload são registradas em uploads.log. O código registra tentativas com falha e uploads concluídos. Nos uploads bem-sucedidos, o log inclui o nome do arquivo e o endereço IP identificado pela requisição.
Observações técnicas e limitações identificadas
Esta seção descreve pontos observados na implementação atual, sem aplicar modificações:
- Sem autenticação: os endpoints não exigem login, token ou chave de API.
- Modo de depuração: app.py inicia o Flask com debug=True. Esse modo é destinado ao desenvolvimento e não deve ser exposto em produção.
- Sobrescrita de nomes: não há geração de nomes únicos. Um novo arquivo com o mesmo nome pode substituir o arquivo já existente.
- Validação por extensão: a aceitação considera a extensão do nome, sem verificar o conteúdo real ou o MIME type do arquivo.
- Limite de tamanho: a checagem considera request.content_length, e há divergência entre o valor configurado e a mensagem de erro.
- Persistência incompleta: a tabela SQLite é criada, mas não recebe registros durante o upload.
- Pasta de armazenamento: os caminhos uploads/, database.db e uploads.log são relativos ao diretório de execução.
Para uso em produção, seria necessário avaliar especialmente autenticação, configuração segura do servidor, validação do conteúdo dos arquivos, controle de tamanho e política de nomes. Esses itens são recomendações de evolução, não funcionalidades já implementadas.
