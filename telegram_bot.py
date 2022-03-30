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
    AWAIT_ANSWER = 1


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
    update.message.reply_text(
        text='Привет! Я бот для викторин!',
        reply_markup=DEFAULT_KEYBOARD,
    )

    return QuizStates.START


def handle_new_question(update: Update, context: CallbackContext):
    questions = context.bot_data['questions']

    question = random.choice(list(questions.keys()))
    chat_id = update.effective_chat.id

    context.bot_data['redis'].set(chat_id, question)

    update.message.reply_text(
        text=question
    )

    return QuizStates.AWAIT_ANSWER


def handle_answer(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    question = context.bot_data['redis'].get(chat_id).decode('utf-8')
    answer = context.bot_data['questions'].get(question)

    cleared_answer = answer[:answer.find('.')]

    if cleared_answer.lower() in update.message.text.lower():
        update.message.reply_text(
            text='Правильно! Поздравляю! '
                 'Для следующего вопроса нажми «Новый вопрос»'
        )
        return QuizStates.START

    update.message.reply_text(text='Неправильно… Попробуешь ещё раз?')
    return QuizStates.AWAIT_ANSWER


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
               )],
               QuizStates.AWAIT_ANSWER: [MessageHandler(
                   Filters.text & ~Filters.command,
                   handle_answer
               )]
            },
            fallbacks=[CommandHandler('start', start)]
        )
    )

    updater.start_polling()
    updater.idle()
