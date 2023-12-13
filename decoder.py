import os
import logging
from telegram.ext import Updater, MessageHandler, Filters
from flask import Flask

# Configurar o logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Função para obter a URL de redirecionamento a partir de um link encurtado
def obter_url_redirecionamento(link_encurtado):
    try:
        logger.info(f"Tentando desencurtar: {link_encurtado}")

        # Realizar uma requisição HTTP GET e seguir os redirecionamentos
        response = requests.get(link_encurtado)
        url_redirecionamento = response.url

        logger.info(f"URL desencurtada: {url_redirecionamento}")

        return url_redirecionamento

    except Exception as e:
        logger.error(f"Erro ao obter URL de redirecionamento: {e}")
        return link_encurtado

# Configurar o Flask
app = Flask(__name__)

# Porta padrão ou porta fornecida pelo Heroku
port = int(os.environ.get('PORT', 5000))

# Adicionar um roteamento simples para evitar o erro de boot
@app.route('/')
def index():
    return "Seu aplicativo está rodando com sucesso!"

# Iniciar o bot
updater = Updater(token='SEU_TOKEN', use_context=True)
dp = updater.dispatcher

# Adicionar um manipulador de mensagens ao dispatcher
dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_messages))

# Iniciar o Flask e o bot simultaneamente
if __name__ == '__main__':
    updater.start_polling()
    app.run(host='0.0.0.0', port=port)
