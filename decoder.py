import logging
import re
import requests
from telegram.ext import Updater, MessageHandler, Filters

# Configurar o logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Função para obter a URL de redirecionamento a partir de um link encurtado
def obter_url_redirecionamento(link_encurtado):
    try:
        logger.info(f"Tentando desencurtar: {link_encurtado}")

        # Utilizar timeout para evitar bloqueios prolongados
        response = requests.get(link_encurtado, timeout=10)
        response.raise_for_status()  # Lançar exceção para códigos de status HTTP de erro

        url_redirecionamento = response.url

        logger.info(f"URL desencurtada: {url_redirecionamento}")

        return url_redirecionamento

    except requests.exceptions.RequestException as e:
        logger.error(f"Erro ao obter URL de redirecionamento: {e}")
        return link_encurtado

# Manipulador de mensagens
def handle_messages(update, context):
    message_text = update.message.text
    
    # Usar expressão regular para encontrar links no meio do texto
    links = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message_text)
    
    for link in links:
        url_redirecionamento = obter_url_redirecionamento(link)
        # Substituir o link na mensagem original pelo link desencurtado
        message_text = message_text.replace(link, url_redirecionamento)
    
    context.bot.send_message(chat_id=update.message.chat_id, text=f"⚽  ULTRON - LINK DA PARTIDA:  ⚽\n{message_text}")

# Substitua 'SEU_TOKEN' pelo token fornecido pelo BotFather
updater = Updater(token='6854755484:AAG-jgENE7UorXuH9I_UdxyttivBQrncG20', use_context=True)
dp = updater.dispatcher

# Adicionar um manipulador de mensagens ao dispatcher
dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_messages))

# Iniciar o bot
updater.start_polling()

# Aguardar o bot ser encerrado manualmente ou por algum erro
updater.idle()
