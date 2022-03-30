from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (Updater,
                          CallbackContext,
                          MessageHandler,
                          Filters,
                          CommandHandler)

import config


DEFAULT_KEYBOARD = ReplyKeyboardMarkup(
    [
        [
            'Новый вопрос', 'Сдаться'
        ],
        [
            'Мой счёт'
        ]
    ],
    resize_keyboard=True
)


def start(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Привет! Я бот для викторин!',
        reply_markup=DEFAULT_KEYBOARD,
    )


if __name__ == '__main__':
    updater = Updater(config.telegram_token)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(
        CommandHandler('start', start)
    )

    updater.start_polling()
    updater.idle()
