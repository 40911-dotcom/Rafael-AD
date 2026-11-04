# Importa a função jsonify do Flask, que serve para transformar um dicionário em JSON
from flask import jsonify, send_from_directory  

# Define uma variável chamada UPLOAD_FOLDER que guarda o nome da pasta onde os arquivos ficam guardados
UPLOAD_FOLDER = 'uploads'  

# Cria uma classe chamada DownloadController (é tipo uma "caixinha" que guarda funções)
class DownloadController:  

    # Diz que a função abaixo é estática, ou seja, pode ser usada sem precisar criar um objeto da classe  
    @staticmethod  
    def download_file(filename):  # Define uma função chamada download_file que recebe um nome de arquivo (filename)
        try:  # Tenta fazer algo dentro desse bloco
            # Envia o arquivo da pasta UPLOAD_FOLDER com o nome que foi passado para a função
            # O as_attachment=True faz com que o arquivo seja baixado em vez de ser só exibido
            return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)  
        except FileNotFoundError:  # Se der erro porque o arquivo não foi achado...
            # Retorna uma mensagem dizendo "Arquivo não encontrado" no formato JSON e o código de erro 404
            return jsonify({"error": "Arquivo não encontrado"}), 404  
