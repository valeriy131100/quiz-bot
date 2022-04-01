from environs import Env

env = Env()
env.read_env()

quizzes_directory = env.str('QUIZZES_DIRECTORY', 'quizzes')
quizzes_encoding = env.str('QUIZZES_ENCODING', 'koi8_r')

telegram_token = env.str('TELEGRAM_TOKEN')

redis_host = env.str('REDIS_HOST', 'localhost')
redis_port = env.int('REDIS_PORT', 6379)
redis_password = env.str('REDIS_PASSWORD', None)

vk_token = env.str('VK_TOKEN')
vk_group_id = env.str('VK_GROUP_ID')
