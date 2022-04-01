from dataclasses import dataclass, field

import vk_api as vk
from redis import Redis
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard
from vk_api.utils import get_random_id
from vk_api.vk_api import VkApiMethod

import config


@dataclass
class Context:
    vk_api: VkApiMethod
    redis: Redis
    current_questions: dict = field(default_factory=dict)


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
    pass


def handle_surrender(event, context):
    pass


def handle_answer(event, context):
    pass


if __name__ == "__main__":
    vk_session = vk.VkApi(token=config.vk_token, api_version='5.131')
    longpoll = VkBotLongPoll(vk_session, group_id=config.vk_group_id)

    bot_context = Context(
        vk_api=vk_session.get_api(),
        redis=Redis(
            host=config.redis_host,
            port=config.redis_port,
            password=config.redis_password
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
