from environs import Env

env = Env()
env.read_env()

quizzes_directory = env.str('QUIZ_DIRECTORY', 'quizzes')
quizzes_encoding = env.str('QUIZ_ENCODING', 'koi8_r')

telegram_token = env.str('TELEGRAM_TOKEN')
