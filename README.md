# quiz-bot

[Telegram](https://telegram.org) и [Vk](https://vk.com)-боты для проведения викторин.

[Пример vk-бота](https://vk.me/public212344075). [Пример telegram-бота](https://t.me/AnotherMuseumQuizBot).

## Установка
Вам понадобится установленный Python 3.6+ и git.

Склонируйте репозиторий:
```bash
$ git clone https://github.com/valeriy131100/quiz-bot
```

Создайте в этой папке виртуальное окружение:
```bash
$ cd quiz-bot
$ python3 -m venv venv
```

Активируйте виртуальное окружение и установите зависимости:
```bash
$ source venv/bin/activate
$ pip install -r requirements.txt
```

## Использование

### Переменные среды
Заполните файл .env.example и переименуйте его в .env или иным образом задайте переменные среды:
* `TELEGRAM_TOKEN` - токен бота Telegram. Можно получить у [@BotFather](https://t.me/BotFather).
* `VK_TOKEN` - токен от группы Вконтакте. Создайте группу [Вконтакте](https://vk.com), затем перейдите в настройки группы и в разделе Сообщения включите сообщения сообщества, а также в подразделе настройки ботов включите Возможности ботов. Далее перейдите в раздел Настройки - Работа с API, включите Longpoll, а также события для сообщений в лонгполле. Желательно указать версию API 5.131. Далее создайте ключ доступа и укажите галочку доступа к сообщениям.
* `VK_GROUP_ID` - id созданной группы Вконтакте. Можно узнать [здесь](https://regvk.com/id/).
* `QUIZZES_DIRECTORY` - путь к папке с файлами викторин. По умолчанию - `quizzes`. Примеры файлов викторин можно найти в репозитории в `example_quizzes`.
* `QUIZZES_ENCODING` - кодировка файлов викторин. По умолчанию - `koi8_r`.
* `REDIS_HOST`, `REDIS_PORT`, `REDIS_PASSWORD` - данные для подключения как базе данных [Redis](https://redis.io/). По умолчанию - `localhost`, `6379` и `None`.

### Запуск vk-бота
Находясь в директории quiz-bot исполните:
```bash
$ venv/bin/python vk_bot.py
```

### Запуск telegram-бота
Находясь в директории quiz-bot исполните:
```bash
$ venv/bin/python telegram_bot.py
```

### Деплой на [Heroku](https://heroku.com/)

1. Зарегистрируйтесь и создайте приложение Heroku.
2. Соедините аккаунт Heroku и GitHub и выберите этот репозиторий.
3. Перейдите в раздел `Settings - Config Vars` и задайте те же переменные среды, что и для запуска локально, за исключением GOOGLE_APPLICATION_CREDENTIALS.
4. Вернитесь к разделу `Deploy`, пролистните до самого конца и нажмите на кнопку `Deploy Branch`.
5. Перейдите в раздел `Resources` и запустите dyno для `vk_bot` и `telegram_bot`.