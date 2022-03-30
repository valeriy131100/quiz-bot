from telegram import Update
from telegram.ext import Updater, CallbackContext, MessageHandler, Filters

import config


def echo(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=update.message.text
    )


if __name__ == '__main__':
    updater = Updater(config.telegram_token)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(
        MessageHandler(
            Filters.text & (~Filters.command), echo
        )
    )

    updater.start_polling()
    updater.idle()
