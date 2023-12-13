import os
import logging
from telegram.ext import Updater, MessageHandler, Filters

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

# Manipulador de mensagens
def handle_messages(update, context):
    message_text = update.message.text
    
    if 'http' in message_text:
        url_redirecionamento = obter_url_redirecionamento(message_text)
        if url_redirecionamento:
            context.bot.send_message(chat_id=update.message.chat_id, text=f"⚽  ULTRON - LINK DA PARTIDA:  ⚽\n{url_redirecionamento}")
        else:
            context.bot.send_message(chat_id=update.message.chat_id, text="Erro ao obter URL de redirecionamento.")

# Obter a porta do ambiente Heroku
PORT = int(os.environ.get('PORT', 5000))

# Substitua 'SEU_TOKEN' pelo token fornecido pelo BotFather
updater = Updater(token='6854755484:AAG-jgENE7UorXuH9I_UdxyttivBQrncG20', use_context=True)
dp = updater.dispatcher

# Adicionar um manipulador de mensagens ao dispatcher
dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_messages))

# Iniciar o bot com a porta definida pelo ambiente Heroku
updater.start_webhook(listen="0.0.0.0", port=PORT, url_path='SEU_TOKEN')
updater.bot.setWebhook(f"https://turingx-691575dd13e5.herokuapp.com/{SEU_TOKEN}")

# Aguardar o bot ser encerrado manualmente ou por algum erro
updater.idle()
