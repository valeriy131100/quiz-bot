import vk_api as vk
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id

import config


def echo(event, vk_api):
    vk_api.messages.send(
        user_id=event.message.from_id,
        message=event.message.text,
        random_id=get_random_id()
    )


if __name__ == "__main__":
    vk_session = vk.VkApi(token=config.vk_token, api_version='5.131')
    vk_api = vk_session.get_api()
    longpoll = VkBotLongPoll(vk_session, group_id=config.vk_group_id)

    while True:
        try:
            for event in longpoll.listen():
                if (event.type == VkBotEventType.MESSAGE_NEW
                        and event.from_user):
                    echo(event, vk_api)
        except Exception as error:
            continue
