import os
import re

def load_quizzes_from_directory(directory, encoding):
    quizzes = dict()

    for quiz_filename in os.listdir(directory):
        quiz_path = os.path.join(directory, quiz_filename)
        with open(quiz_path, mode='r', encoding=encoding) as quiz_file:
            last_question = None
            quiz_parts = map(
                lambda part: part.replace('\n', ' '),
                quiz_file.read().split('\n\n')
            )
            for quiz_part in quiz_parts:
                if match := re.match(r'\s*Вопрос \d*:\s*', quiz_part):
                    question = quiz_part.replace(match[0], '')
                    quizzes[question] = None
                    last_question = question
                elif match := re.match(r'\s*Ответ:\s*', quiz_part):
                    answer = quiz_part.replace(match[0], '')
                    quizzes[last_question] = answer

    return quizzes
