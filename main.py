import os

from environs import Env

if __name__ == '__main__':
    env = Env()
    env.read_env()

    quiz_directory = env.str('QUIZ_DIRECTORY', 'quizzes')

    for quiz_filename in os.listdir('quizzes'):
        quiz_path = os.path.join(quiz_directory, quiz_filename)
        with open(quiz_path, mode='r', encoding='koi8_r') as quiz_file:
            print(quiz_file.read())
