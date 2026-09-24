# goit-pythonweb-hw-08

REST API для зберігання та управління контактами.
Стек: **FastAPI**, **SQLAlchemy 2.0 (async)**, **PostgreSQL**, **Pydantic**, **Alembic**, пакетний менеджер **uv**.

## Структура

```
├── src
│   ├── api
│   │   ├── contacts.py      # маршрути /api/contacts
│   │   └── utils.py         # /api/healthchecker
│   ├── services
│   │   └── contacts.py      # бізнес-логіка (перевірка унікальності email)
│   ├── repository
│   │   └── contacts.py      # запити до БД
│   ├── database
│   │   ├── models.py        # модель Contact
│   │   └── db.py            # async-сесія SQLAlchemy
│   ├── conf
│   │   └── config.py        # налаштування з .env
│   └── schemas.py           # Pydantic-схеми
├── migrations               # міграції Alembic
├── docker-compose.yml       # PostgreSQL
├── pyproject.toml
└── main.py
```

## Запуск

1. Встановити залежності:
   ```bash
   uv sync
   ```
2. Створити `.env` на основі `.env.example` і вказати свій пароль:
   ```bash
   cp .env.example .env
   ```
3. Запустити PostgreSQL:
   ```bash
   docker compose up -d
   ```
4. Застосувати міграції:
   ```bash
   uv run alembic upgrade head
   ```
5. Запустити сервер:
   ```bash
   uv run python main.py
   ```

Swagger-документація: http://localhost:8000/docs
ReDoc: http://localhost:8000/redoc

## Ендпоінти

| Метод  | Шлях                        | Опис                                              |
|--------|-----------------------------|---------------------------------------------------|
| GET    | `/api/contacts/`            | Список контактів (+ пошук, пагінація)             |
| GET    | `/api/contacts/birthdays`   | Дні народження на найближчі 7 днів (`?days=N`)    |
| GET    | `/api/contacts/{id}`        | Один контакт                                      |
| POST   | `/api/contacts/`            | Створити контакт                                  |
| PUT    | `/api/contacts/{id}`        | Оновити контакт (передаються лише змінені поля)   |
| DELETE | `/api/contacts/{id}`        | Видалити контакт                                  |
| GET    | `/api/healthchecker`        | Перевірка підключення до БД                       |

Query-параметри пошуку для `GET /api/contacts/`: `first_name`, `last_name`, `email`
(частковий збіг без урахування регістру), а також `skip` і `limit`.

### Приклад тіла запиту

```json
{
  "first_name": "Volodymyr",
  "last_name": "Kheroim",
  "email": "volodymyr_kh@example.com",
  "phone": "+380501234567",
  "birthday": "1990-09-27",
  "additional_data": "Bro"
}
```
