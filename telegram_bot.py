import random
from enum import Enum

import redis
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (Updater,
                          CallbackContext,
                          MessageHandler,
                          Filters,
                          CommandHandler,
                          ConversationHandler)

import config
from file_workers import load_quizzes_from_directory


class QuizStates(Enum):
    START = 0


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

    return QuizStates.START


def handle_new_question(update: Update, context: CallbackContext):
    questions = context.bot_data['questions']

    question = random.choice(list(questions.keys()))
    chat_id = update.effective_chat.id

    context.bot_data['redis'].set(chat_id, question)

    context.bot.send_message(
        chat_id=chat_id,
        text=question
    )


if __name__ == '__main__':
    updater = Updater(config.telegram_token)

    dispatcher = updater.dispatcher

    dispatcher.bot_data['questions'] = load_quizzes_from_directory(
        config.quizzes_directory,
        config.quizzes_encoding
    )

    dispatcher.bot_data['redis'] = redis.Redis(
        host=config.redis_host,
        port=config.redis_port,
        password=config.redis_password
    )

    dispatcher.add_handler(
        ConversationHandler(
            entry_points=[CommandHandler('start', start)],
            states={
               QuizStates.START: [MessageHandler(
                   Filters.regex(r'^Новый вопрос$'),
                   handle_new_question
               )]
            },
            fallbacks=[CommandHandler('start', start)]
        )
    )

    updater.start_polling()
    updater.idle()
