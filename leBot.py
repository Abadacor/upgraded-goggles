"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

from icecream import ic 
import json
import logging
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

shopping_list = []

def get_api_key():
    with open("very_secret_secret.json", "r") as jsonfile:
        data = json.load(jsonfile)
    return data["api-key"]

def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('/add ingrédient1, ingrédient2 - ajoute ingrédients 1 et 2 à la liste de courses.\n/rm ingrédient1 - supprime ingrédient1 de la liste de courses.\n /get - renvoie la lite de courses en l\'état.\n /clear - reset la liste de courses.')

def add_command(update: Update, context: CallbackContext):
    """
    Adds one or more item(s) to the current shopping list.
    """
    to_add = [item.strip() for item in (update.message.text[5:]).split(',')]
    ic(to_add)
    global shopping_list ; shopping_list += to_add

def rm_command(update: Update, context: CallbackContext):
    """
    Deletes one or more item(s) from the current shopping list.
    """
    to_rm = [item.strip() for item in (update.message.text[4:]).split(',')]
    global shopping_list ; shopping_list = [shopping_list.remove(item) for item in to_rm]
    

def get_command(update: Update, context: CallbackContext) -> None:
    """
    Sends back the current shopping list.
    """
    global shopping_list
    if not shopping_list:
        update.message.reply_text("Nothing to see here.")
    else:   
        update.message.reply_text(shopping_list)

def clear_command(update: Update, context: CallbackContext) -> None:
    """
    Clears the current shopping list.
    """
    shopping_list.clear()
    update.message.reply_text("J'espère que t'avais rien oublié !")

def main() -> None:
    """Start the bot."""
    #API key
    api_key = get_api_key()

    # Create the Updater and pass it your bot's token.
    updater = Updater(api_key)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("get", get_command))
    dispatcher.add_handler(CommandHandler("clear", clear_command))
    dispatcher.add_handler(CommandHandler("add", add_command))
    dispatcher.add_handler(CommandHandler("rm", rm_command))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
