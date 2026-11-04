import os  # Permite mexer com arquivos e pastas do sistema (criar a pasta uploads)
import logging  # Permite registrar mensagens de log (sucesso, aviso, erro) num arquivo
from flask import jsonify, request  # jsonify: devolve respostas em JSON | request: acessa os dados que o cliente enviou (arquivo, IP, tamanho)
from werkzeug.utils import secure_filename  # Limpa o nome do arquivo, removendo caracteres perigosos (ex: ../../)

# Configuração de logs
LOG_FILE = "uploads.log"
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(message)s")

# Configuração de upload
PASTA_UPLOAD = 'uploads'
EXTENSOES_PERMITIDAS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'txt'}
TAMANHO_MAXIMO_ARQUIVO = 30 * 1024  # 30 KB

# Cria o diretório de upload se não existir
if not os.path.exists(PASTA_UPLOAD):
    os.makedirs(PASTA_UPLOAD)

class UploadController:

    @staticmethod
    def arquivo_permitido(nome_arquivo):
        """Verifica se a extensão do arquivo é permitida."""
        return '.' in nome_arquivo and nome_arquivo.rsplit('.', 1)[1].lower() in EXTENSOES_PERMITIDAS

    @staticmethod
    def upload_file():
        """Recebe e processa o upload do arquivo."""

        # Verifica se um arquivo foi enviado
        if 'file' not in request.files:
            logging.warning("Falha no upload: Nenhum arquivo enviado")
            return jsonify({"erro": "Nenhum arquivo enviado"}), 400

        arquivo = request.files['file']

        # Verifica se o nome do arquivo está vazio
        if arquivo.filename == '':
            logging.warning("Falha no upload: Nome do arquivo vazio")
            return jsonify({"erro": "Nome do arquivo vazio"}), 400

        # Verifica o tamanho do arquivo
        if request.content_length > TAMANHO_MAXIMO_ARQUIVO:
            logging.warning(f"Falha no upload: {arquivo.filename} - Tamanho excede 15 KB")
            return jsonify({"erro": "Arquivo excede o tamanho máximo permitido (15 KB)"}), 400

        # Verifica se o arquivo é permitido
        if arquivo and UploadController.arquivo_permitido(arquivo.filename):
            nome_arquivo = secure_filename(arquivo.filename)
            caminho_arquivo = os.path.join(PASTA_UPLOAD, nome_arquivo)
            arquivo.save(caminho_arquivo)

            # Registra o sucesso do upload no log
            ip_usuario = request.remote_addr
            logging.info(f"Upload bem-sucedido: {nome_arquivo} | IP: {ip_usuario}")

            return jsonify({
                "mensagem": "Arquivo salvo com sucesso!",
                "arquivo": nome_arquivo
            }), 200
        else:
            logging.warning(f"Falha no upload: {arquivo.filename} - Tipo de arquivo não permitido")
            return jsonify({
                "erro": "Tipo de arquivo não permitido!",
                "tipos_permitidos": list(EXTENSOES_PERMITIDAS)
            }), 400
