# Coffee Shop Mini App (Backend)

Это серверная часть Telegram Mini App для заказа кофе с добавками. Бэкенд реализован на Django Rest Framework и предоставляет REST API для взаимодействия с клиентской частью.

## 📌 Репозиторий клиента

[Coffee Shop Frontend](https://github.com/HollowKaeden/CoffeeTimeBot)

## 🧩 Основной функционал

- Авторизация пользователей через Telegram (`initData`).
- Получение списка кофе и добавок.
- Создание и просмотр заказов.
- Админ-панель для управления товарами и заказами.

## ⚙️ Стек технологий

- Django 5.x
- Django REST Framework
- PostgreSQL
- JWT авторизация
- Docker

## 🚀 Быстрый старт

### Клонирование репозитория

```bash
git clone git@github.com:HollowKaeden/CoffeeTimeBotAPI.git
cd CoffeeTimeBotAPI
```

### Настройка окружения

Создайте файл `.env` в корне проекта, пример заполнения представлен в .env.example:

```env
TELEGRAM_BOT_TOKEN=TOKEN
SECRET_KEY="SECRET_KEY"
DEBUG=True_OR_False

DB_NAME=NAME
DB_USER=USER
DB_PASSWORD=PASSWORD
DB_HOST=HOST
DB_PORT=PORT
```

### Создание виртуального окружения
```bash
python -m venv venv
source venv/Scripts/activate
```

### Установка зависимостей

```bash
pip install -r requirements.txt
```

### Применение миграций

```bash
cd CoffeeTimeAPI
python manage.py makemigrations
python manage.py migrate
```

## 🐳 Docker

```bash
docker build -t coffee-backend .
docker run -p 8000:8000 --env-file .env coffee-backend
```

## 📮 API Эндпоинты

- `POST /api/v1/auth/telegram/` — Авторизация через Telegram `initData`
- `GET /api/v1/coffees/` — Получение списка всех доступных кофе
- `GET /api/v1/addons/` — Получение списка всех доступных добавок
- `GET /api/v1/orders/` — Получение истории заказов текущего пользователя
- `POST /api/v1/orders/create/` — Создание нового заказа
- `POST /api/v1/token/refresh/` — Обновление access-токена по refresh-токену
- `GET /api/v1/swagger/` — Swagger UI для документации
- `GET /api/v1/redoc/` — ReDoc UI для документации


## 🔐 Админ-панель

```bash
python manage.py createsuperuser
```

Далее доступно по адресу `/admin`.

