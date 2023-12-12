import logging
import re
from telegram.ext import Updater, MessageHandler, CallbackContext
import requests

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def obter_url_redirecionamento(link_encurtado):
    try:
        response = requests.head(link_encurtado, allow_redirects=True)
        url_redirecionamento = response.url
        return url_redirecionamento
    except Exception as e:
        logger.error(f"Erro ao obter URL de redirecionamento: {e}")
        return link_encurtado

def handle_messages(update, context):
    if update.message and update.message.text:
        texto_original = update.message.text
        links_encurtados = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', texto_original)
        for link_encurtado in links_encurtados:
            url_redirecionamento = obter_url_redirecionamento(link_encurtado)
            mensagem_personalizada = "LINK DA PARTIDA:"
            texto_original = texto_original.replace(link_encurtado, f"{mensagem_personalizada}\n{url_redirecionamento}")
        context.bot.send_message(chat_id=update.message.chat_id, text=texto_original)

def main():
    updater = Updater(token='6854755484:AAG-jgENE7UorXuH9I_UdxyttivBQrncG20', use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(callback=handle_messages, filters=None))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
