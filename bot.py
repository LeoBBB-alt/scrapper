import asyncio
import logging
from telegram import Update, BotCommand
from telegram.ext import Application, CommandHandler, ContextTypes

# Importa a função do scraper avançado
from advanced_scraper import fetch_site_details

# Configuração básica de logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Seu token do Telegram (já preenchido)
TELEGRAM_TOKEN = '7934207024:AAEfJHEze9yU6ArUCuB179WZvXLXHcDZla8'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Envia uma mensagem de boas-vindas."""
    await update.message.reply_text('Olá! Use o comando /buscar <termo> para pesquisar informações no site.')

async def buscar(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Recebe um termo de busca, chama o scraper avançado e envia os resultados.
    """
    if not context.args:
        await update.message.reply_text('Por favor, forneça um termo de busca. Ex: /buscar 12313')
        return

    search_term = " ".join(context.args)
    await update.message.reply_text(f'Buscando informações para: {search_term}...')

    # Chama a função do scraper avançado
    result = await fetch_site_details(search_term)

    if isinstance(result, dict):
        message = (
            f"🔍 *Informações para {search_term}:*\n\n"
            f"*First Name:* {result.get('first_name', 'N/A')}\n"
            f"*Last Name:* {result.get('last_name', 'N/A')}\n\n"
            f"*Original Identifier:* {result.get('original_identifier', 'N/A')}\n"
            f"*Campaign Name:* {result.get('campaign_name', 'N/A')}\n"
            f"*Address 1:* {result.get('address_1', 'N/A')}\n"
            f"*Address 2:* {result.get('address_2', 'N/A')}"
        )
        await update.message.reply_text(message, parse_mode='Markdown')
    else:
        # Se for uma string, é uma mensagem de erro
        await update.message.reply_text(f'Ocorreu um erro ao buscar: {result}')

def main() -> None:
    """
    Inicia o bot.
    """
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Adiciona os handlers de comando
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("buscar", buscar))

    # Define os comandos do menu
    commands = [
        BotCommand("start", "Inicia o bot e mostra a mensagem de boas-vindas"),
        BotCommand("buscar", "Busca informações no site (ex: /buscar 12313)")
    ]
    application.bot.set_my_commands(commands)

    print("Bot iniciado! Pressione Ctrl+C para parar.")
    application.run_polling()

if __name__ == '__main__':
    main()
