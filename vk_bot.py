import json
import re

import vk_api as vk
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id

import config


def start(event, vk_api):
    keyboard = VkKeyboard()
    keyboard.add_button('Новый вопрос')
    keyboard.add_button('Сдаться')
    keyboard.add_line()
    keyboard.add_button('Мой счёт')

    vk_api.messages.send(
        user_id=event.message.from_id,
        message='Привет! Я бот для викторин!',
        random_id=get_random_id(),
        keyboard=keyboard.get_keyboard()
    )


if __name__ == "__main__":
    vk_session = vk.VkApi(token=config.vk_token, api_version='5.131')
    vk_api = vk_session.get_api()
    longpoll = VkBotLongPoll(vk_session, group_id=config.vk_group_id)

    commands = {
        r'^Начать$': start
    }

    while True:
        try:
            for event in longpoll.listen():
                if not (event.type == VkBotEventType.MESSAGE_NEW
                        and event.from_user):
                    continue

                for command in commands:
                    if not re.match(command, event.message.text):
                        continue

                    commands[command](event, vk_api)
                    break

        except Exception as error:
            continue
