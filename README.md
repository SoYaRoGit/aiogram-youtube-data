# aiogram-youtube-data

## Описание
Этот проект представляет собой Telegram бота, который позволяет получить данные с API Google о видео, плейлистах и каналах на YouTube, а также сделать выгрузку базы данных в удобный Excel файл.

## Мотивация
Моя мотивация для создания этого проекта заключалась в решении вопросов тайм-менеджмента, связанных с определением продолжительности плейлиста на YouTube. Я заметил, что многие пользователи тратят много времени на просмотр плейлистов, не имея четкого представления о том, сколько времени это займет. Поэтому я решил разработать Telegram бота, который бы позволил пользователям быстро получать продолжительность плейлиста на YouTube, а также дополнительную информацию о запрашиваемом ресурсе.

## Проблема
Проблема, которую решает этот бот, состоит в том, что многие пользователи тратят время на просмотр плейлиста, не имея представления о его общей продолжительности. Это может привести к нежелательным ситуациям, когда пользователь начинает просмотр, не имея достаточно времени, чтобы досмотреть плейлист целиком. Бот позволяет быстро получить информацию о продолжительности плейлиста на YouTube, помогая пользователям лучше планировать своё время и избегать недооценки продолжительности просмотра.

## Возможности
1. Получение информации о продолжительности плейлистов на YouTube.
2. Выгрузка базы данных в удобный Excel файл для дальнейшего анализа.
3. Просмотр логов для отслеживания действий бота и пользователей.
4. Использование базы данных sqlite3 для хранения информации о запрашиваемых ресурсах и других сведений.


## Используемые библиотеки
- python (версия 3.11)
- ruff (версия 0.3.2) - Чрезвычайно быстрый линтер и форматировщик кода Python, написанный на Rust.
- google API Python Client (версия 2.121.0) - Клиент для взаимодействия с API Google.
- environs (версия 11.0.0) - Библиотека для работы с переменными окружения.
- isodate (версия 0.6.1) - Библиотека для работы с форматом даты и времени ISO 8601.
- aiogram (версия 3.4.1) - Библиотека для создания Telegram ботов на Python.
- openpyxl (версия 3.1.2) - Библиотека для работы с файлами Excel в формате xlsx.


## Установка

```bash
git clone https://github.com/YaSoRoP/aiogram-youtube-data.git
```

Проверьте, установлен ли у вас Poetry, в случае если нет выполните установку
```bash
pip install poetry
```

Зайдите в только что скаченный репозиторий
(пример ниже)
> C:\Users\your_name\Desktop\aiogram-youtube-data>

Активируйте виртуальное окружение 
```bash
poetry shell 
```

Установите библиотеки
```bash
poetry install
```

Проверьте используемые библиотеки
```bash
poetry show --tree
```

На вывод должно получиться следующее 
```bash
aiogram 3.4.1 Modern and fully asynchronous framework for Telegram Bot API
├── aiofiles >=23.2.1,<23.3.0
├── aiohttp >=3.9.0,<3.10.0
│   ├── aiosignal >=1.1.2 
│   │   └── frozenlist >=1.1.0 
│   ├── attrs >=17.3.0 
│   ├── frozenlist >=1.1.1 (circular dependency aborted here)
│   ├── multidict >=4.5,<7.0 
│   └── yarl >=1.0,<2.0 
│       ├── idna >=2.0 
│       └── multidict >=4.0 (circular dependency aborted here)
├── certifi >=2023.7.22
├── magic-filter >=1.0.12,<1.1
├── pydantic >=2.4.1,<2.6
│   ├── annotated-types >=0.4.0 
│   ├── pydantic-core 2.14.6 
│   │   └── typing-extensions >=4.6.0,<4.7.0 || >4.7.0 
│   └── typing-extensions >=4.6.1 (circular dependency aborted here)
└── typing-extensions >=4.7.0,<=5.0
environs 11.0.0 simplified environment variable parsing
├── marshmallow >=3.13.0
│   └── packaging >=17.0 
└── python-dotenv *
google-api-python-client 2.121.0 Google API Client Library for Python
├── google-api-core >=1.31.5,<2.0.dev0 || >2.3.0,<3.0.0.dev0
│   ├── google-auth >=2.14.1,<3.0.dev0 
│   │   ├── cachetools >=2.0.0,<6.0 
│   │   ├── pyasn1-modules >=0.2.1
│   │   │   └── pyasn1 >=0.4.6,<0.6.0
│   │   └── rsa >=3.1.4,<5
│   │       └── pyasn1 >=0.1.3 (circular dependency aborted here)
│   ├── googleapis-common-protos >=1.56.2,<2.0.dev0
│   │   └── protobuf >=3.19.5,<3.20.0 || >3.20.0,<3.20.1 || >3.20.1,<4.21.1 || >4.21.1,<4.21.2 || >4.21.2,<4.21.3 || >4.21.3,<4.21.4 || >4.21.4,<4.21.5 || >4.21.5,<5.0.0.dev0
│   ├── protobuf >=3.19.5,<3.20.0 || >3.20.0,<3.20.1 || >3.20.1,<4.21.0 || >4.21.0,<4.21.1 || >4.21.1,<4.21.2 || >4.21.2,<4.21.3 || >4.21.3,<4.21.4 || >4.21.4,<4.21.5 || >4.21.5,<5.0.0.dev0 (circular dependency aborted here)
│   └── requests >=2.18.0,<3.0.0.dev0
│       ├── certifi >=2017.4.17
│       ├── charset-normalizer >=2,<4
│       ├── idna >=2.5,<4
│       └── urllib3 >=1.21.1,<3
├── google-auth >=1.19.0,<3.0.0.dev0
│   ├── cachetools >=2.0.0,<6.0
│   ├── pyasn1-modules >=0.2.1
│   │   └── pyasn1 >=0.4.6,<0.6.0
│   └── rsa >=3.1.4,<5
│       └── pyasn1 >=0.1.3 (circular dependency aborted here)
├── google-auth-httplib2 >=0.1.0
│   ├── google-auth *
│   │   ├── cachetools >=2.0.0,<6.0
│   │   ├── pyasn1-modules >=0.2.1
│   │   │   └── pyasn1 >=0.4.6,<0.6.0
│   │   └── rsa >=3.1.4,<5
│   │       └── pyasn1 >=0.1.3 (circular dependency aborted here)
│   └── httplib2 >=0.19.0
│       └── pyparsing >=2.4.2,<3.0.0 || >3.0.0,<3.0.1 || >3.0.1,<3.0.2 || >3.0.2,<3.0.3 || >3.0.3,<4
├── httplib2 >=0.15.0,<1.dev0
│   └── pyparsing >=2.4.2,<3.0.0 || >3.0.0,<3.0.1 || >3.0.1,<3.0.2 || >3.0.2,<3.0.3 || >3.0.3,<4
└── uritemplate >=3.0.1,<5
isodate 0.6.1 An ISO 8601 date/time/duration parser and formatter
└── six *
openpyxl 3.1.2 A Python library to read/write Excel 2010 xlsx/xlsm files
└── et-xmlfile *
ruff 0.3.2 An extremely fast Python linter and code formatter, written in Rust.
```

В случае, если проект не видит библиотеки явно укажите интерпретатор

В Visual Studio Code
```
CTRL+SHIFT+P -> Select interpreter -> Poetry
```

Переименуйте файл .env.example в .env
```bash
.env.example -> .env
```

## Настройки файла .env

1. API_KEY_TELEGRAM_BOT: Можно получить через отца бота при создании бота - https://t.me/BotFather
2. API_KEY_SERVICE_YOUTUBE: Можно получить API ключ, нужно создать проект и явно указать YouTube Data API v3 	
https://console.cloud.google.com/
![alt text](https://i.imgur.com/UP6aowA.png)
3. PATH_LOG: Оставить по умолчанию
4. PATH_DATABASE: Оставить по умолчанию

```
# API_KEY_TELEGRAM_BOT - ключ API вашего Telegram бота
API_KEY_TELEGRAM_BOT = 'YOUR_SECRET_KEY'

# API_KEY_SERVICE_YOUTUBE - ключ API вашего сервиса YouTube
API_KEY_SERVICE_YOUTUBE = 'YOUR_SECRET_KEY'

# PATH_LOG - путь к файлу журнала для записи логов
PATH_LOG = 'bot.log'

# PATH_DATABASE - путь к файлу базы данных SQLite
PATH_DATABASE = 'db.sqlite3'
```

Запустите bot.py
```
(aiogram-youtube-data-py3.11) C:\Users\your_name\aiogram-youtube-data\aiogram_youtube_data\TelegramBot>python bot.py
```