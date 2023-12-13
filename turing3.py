import logging
import re
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from telegram.ext import Updater, MessageHandler, CallbackContext

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Configurações do ChromeDriver para o Heroku
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")

# Configuração do ChromeDriver com path local no seu repositório
chrome_bin = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.binary_location = chrome_bin
driver = webdriver.Chrome(options=chrome_options)


def obter_url_redirecionamento(link_encurtado):
    try:
        driver.get(link_encurtado)
        url_redirecionamento = driver.current_url
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
