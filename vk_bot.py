import random
from dataclasses import dataclass, field

import vk_api as vk
from redis import Redis
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard
from vk_api.utils import get_random_id
from vk_api.vk_api import VkApiMethod

import config
from file_workers import load_quizzes_from_directory


@dataclass
class Context:
    vk_api: VkApiMethod
    redis: Redis
    questions: dict = field(default_factory=dict)


def start(event, context):
    keyboard = VkKeyboard()
    keyboard.add_button('Новый вопрос')
    keyboard.add_button('Сдаться')
    keyboard.add_line()
    keyboard.add_button('Мой счёт')

    context.vk_api.messages.send(
        user_id=event.message.from_id,
        message='Привет! Я бот для викторин!',
        random_id=get_random_id(),
        keyboard=keyboard.get_keyboard()
    )


def handle_new_question(event, context):
    from_id = event.message.from_id
    question = random.choice(list(context.questions.keys()))

    context.redis.set(f'vk-{from_id}', question)

    context.vk_api.messages.send(
        user_id=event.message.from_id,
        message=question,
        random_id=get_random_id()
    )


def handle_surrender(event, context):
    from_id = event.message.from_id
    question = context.redis.get(f'vk-{from_id}').decode('utf-8')

    if not question:
        return

    answer = context.questions.get(question)

    context.vk_api.messages.send(
        user_id=event.message.from_id,
        message=answer,
        random_id=get_random_id()
    )

    handle_new_question(event, context)


def handle_answer(event, context):
    from_id = event.message.from_id
    question = context.redis.get(f'vk-{from_id}').decode('utf-8')

    if not question:
        return

    answer = context.questions.get(question)

    cleared_answer = answer[:answer.find('.')]

    if cleared_answer.lower() in event.message.text.lower():
        context.vk_api.messages.send(
            user_id=event.message.from_id,
            message='Правильно! Поздравляю! '
                    'Для следующего вопроса нажми «Новый вопрос»',
            random_id=get_random_id()
        )
    else:
        context.vk_api.messages.send(
            user_id=event.message.from_id,
            message='Неправильно… Попробуешь ещё раз?',
            random_id=get_random_id()
        )


if __name__ == "__main__":
    vk_session = vk.VkApi(token=config.vk_token, api_version='5.131')
    longpoll = VkBotLongPoll(vk_session, group_id=config.vk_group_id)

    bot_context = Context(
        vk_api=vk_session.get_api(),
        redis=Redis(
            host=config.redis_host,
            port=config.redis_port,
            password=config.redis_password
        ),
        questions=load_quizzes_from_directory(
            config.quizzes_directory,
            config.quizzes_encoding
        )
    )

    while True:
        try:
            for event in longpoll.listen():
                if not (event.type == VkBotEventType.MESSAGE_NEW
                        and event.from_user):
                    continue

                command = event.message.text

                if command == 'Начать':
                    start(event, bot_context)
                elif command == 'Новый вопрос':
                    handle_new_question(event, bot_context)
                elif command == 'Сдаться':
                    handle_surrender(event, bot_context)
                else:
                    handle_answer(event, bot_context)

        except Exception as error:
            continue
