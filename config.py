import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:

    # Configurações gerais
    DEBUG = False

    # Configuração de upload
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')

    ALLOWED_EXTENSIONS = {
        'png', 'jpg', 'jpeg', 'gif', 'pdf', 'txt'
    }

    MAX_CONTENT_LENGTH = 30 * 1024  # 30 KB

    # Configuração de logs
    LOG_FILE = os.path.join(BASE_DIR, 'uploads.log')

    # Configuração do banco de dados
    DATABASE = os.path.join(BASE_DIR, 'database.db')
