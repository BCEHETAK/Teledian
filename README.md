# Teledian
Телеграм-бот для заметок

# Деплой

## Через докер
1. Переименовать `.env.example` в `.env` и заполнить нужными данными
2. Выполнить команды `make app-build` и `make app-run`

## Через systemd
1. Поставить [venv](https://docs.python.org/3/library/venv.html) и установить зависимости (`pip install -r requirements.txt`)
2. Установить и настроить [Redis](https://redis.io/docs/install/install-redis/))
3. Переименовать `.env.example` в `.env` и заполнить нужными данными
4. Запустить миграции бд с помощью команды `make migrate`
5. Настроить и запустить `telegram-bot.service`
