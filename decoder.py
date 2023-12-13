import logging
import re
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
import pyshorteners
from telegram.ext import Updater, MessageHandler, filters

# Configurar o logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Função para obter a URL de redirecionamento a partir de um link encurtado
def obter_url_redirecionamento(link_encurtado):
    try:
        logger.info(f"Tentando desencurtar: {link_encurtado}")

        # Configurar o driver do Chrome para o Selenium em modo headless
        chrome_options = ChromeOptions()
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(options=chrome_options)

        # Navegar para a página e obter a URL final
        driver.get(link_encurtado)
        url_redirecionamento = driver.current_url

        # Fechar o navegador
        driver.quit()

        logger.info(f"URL desencurtada: {url_redirecionamento}")

        return url_redirecionamento

    except Exception as e:
        logger.error(f"Erro ao obter URL de redirecionamento: {e}")
        return link_encurtado

# Função para encurtar um link
def encurtar_link(link):
    s = pyshorteners.Shortener()
    return s.tinyurl.short(link)

# Manipulador de mensagens
def handle_messages(update, context):
    message_text = update.message.text

    # Encontrar todos os links na mensagem
    links = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message_text)

    for link in links:
        # Encurtar cada link
        link_encurtado = encurtar_link(link)

        # Adicionar uma mensagem antes do link encurtado
        mensagem = f"Link: {link_encurtado}"

        # Substituir o link original pela mensagem na mensagem
        message_text = message_text.replace(link, mensagem)

    # Enviar a mensagem atualizada
    context.bot.send_message(chat_id=update.message.chat_id, text=message_text)

# Substitua 'SEU_TOKEN' pelo token fornecido pelo BotFather
updater = Updater('6854755484:AAG-jgENE7UorXuH9I_UdxyttivBQrncG20', use_context=True)
dp = updater.dispatcher

# Adicionar um manipulador de mensagens ao dispatcher
dp.add_handler(MessageHandler(filters.Filters.text & ~filters.Filters.command, handle_messages))

# Iniciar o bot
updater.start_polling()

# Aguardar o bot ser encerrado manualmente ou por algum erro
updater.idle()
