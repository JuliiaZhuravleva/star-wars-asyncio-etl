# Домашнее задание: Asyncio и Star Wars API

Этот проект является выполнением домашнего задания по теме "Asyncio" курса по Python-разработке.

[Описание домашнего задания](https://github.com/netology-code/py-homeworks-web/tree/new/2.2-asyncio)

## Описание проекта

Данный проект представляет собой асинхронный скрипт на Python, который выгружает информацию о персонажах из Star Wars API (SWAPI) и сохраняет её в базу данных PostgreSQL.

## Требования

- Python 3.8+
- Docker Compose
- Pip (менеджер пакетов Python)

## Инструкция по запуску

1. Клонируйте репозиторий:
   ```
   git clone https://github.com/JuliiaZhuravleva/star-wars-asyncio-etl.git
   cd star-wars-asyncio-etl
   ```

2. Создайте виртуальное окружение и активируйте его:
   ```
   python -m venv venv
   source venv/bin/activate  # Для Unix-подобных систем
   # или
   venv\Scripts\activate  # Для Windows
   ```

3. Установите зависимости:
   ```
   pip install -r requirements.txt
   ```

4. Создайте файл `.env` в корневой директории проекта и заполните его следующим содержимым:
   ```
   POSTGRES_USER=your_username
   POSTGRES_PASSWORD=your_password
   POSTGRES_DB=your_database_name
   POSTGRES_HOST=localhost
   POSTGRES_PORT=5431
   ```
   Замените `your_username`, `your_password` и `your_database_name` на требуемые значения.

5. Запустите PostgreSQL с помощью Docker Compose:
   ```
   docker-compose up -d
   ```

6. Запустите скрипт:
   ```
   python async_requests.py
   ```

7. После завершения работы скрипта, вы можете остановить и удалить Docker-контейнер:
   ```
   docker-compose down
   ```

## Структура проекта

- `async_requests.py`: основной скрипт для асинхронной загрузки данных
- `models.py`: определение моделей данных и настройка подключения к базе данных
- `docker-compose.yaml`: конфигурация Docker для запуска PostgreSQL
- `requirements.txt`: список зависимостей проекта