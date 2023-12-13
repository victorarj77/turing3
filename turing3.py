import logging
import re
import requests
from telegram.ext import Updater, MessageHandler, Filters

# Configurar o logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Função para obter a URL de redirecionamento a partir de um link encurtado
def obter_url_redirecionamento(message_text):
    try:
        logger.info("Tentando encontrar link na mensagem")

        # Utilizar expressão regular para encontrar o link na mensagem
        match = re.search(r'https?://[^\s]+', message_text)
        
        if match:
            link_encurtado = match.group(0)
            logger.info(f"Link encontrado na mensagem: {link_encurtado}")

            # Realizar uma requisição HTTP GET e seguir os redirecionamentos
            response = requests.get(link_encurtado)
            url_redirecionamento = response.url

            logger.info(f"URL desencurtada: {url_redirecionamento}")

            return url_redirecionamento

    except Exception as e:
        logger.error(f"Erro ao obter URL de redirecionamento: {e}")

    return None

# Manipulador de mensagens
def handle_messages(update, context):
    message_text = update.message.text

    url_redirecionamento = obter_url_redirecionamento(message_text)
    if url_redirecionamento:
        context.bot.send_message(chat_id=update.message.chat_id, text=f"LINK: \n{url_redirecionamento}")
    else:
        context.bot.send_message(chat_id=update.message.chat_id, text="Erro ao obter URL de redirecionamento.")

# Substitua 'SEU_TOKEN' pelo token fornecido pelo BotFather
updater = Updater(token='6854755484:AAG-jgENE7UorXuH9I_UdxyttivBQrncG20', use_context=True)
dp = updater.dispatcher

# Adicionar um manipulador de mensagens ao dispatcher
dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_messages))

# Iniciar o bot
updater.start_polling()

# Aguardar o bot ser encerrado manualmente ou por algum erro
updater.idle()
