# Client Order System (CRM)

Современная веб-система управления клиентами и заказами на базе Django с REST API и Swagger документацией.

## 🚀 Возможности

### Основные функции
- **Управление клиентами**: создание, редактирование, просмотр профилей клиентов
- **Заказы**: полное управление жизненным циклом заказов
- **Аутентификация**: регистрация и авторизация пользователей
- **Изоляция данных**: каждый пользователь видит только свои данные
- **REST API**: полнофункциональный API для интеграции
- **Swagger документация**: интерактивная документация API

### Расширенные возможности
- **Обогащенные профили клиентов**:
  - Основной и дополнительный телефон
  - Email и адрес
  - Теги для категоризации
  - Заметки и история взаимодействий
- **Фильтрация и поиск**:
  - Фильтр заказов по статусу и дате
  - Поиск клиентов по имени и телефону
- **Экспорт данных**: CSV экспорт клиентов и заказов
- **Дашборд**: статистика и аналитика
- **Быстрые действия**: изменение статуса заказа прямо из списка
- **Автозаполнение**: удобный поиск клиентов при создании заказа

## 🛠 Технологии

- **Backend**: Django 6.0.4
- **REST API**: Django REST Framework 3.14+
- **API Documentation**: drf-spectacular (Swagger/OpenAPI)
- **Database**: SQLite3
- **Frontend**: HTML5, CSS3, JavaScript
- **Authentication**: Django Auth
- **Charts**: Chart.js
- **Server**: Gunicorn + Nginx (production)

## 📋 Установка и запуск

### Предварительные требования
- Python 3.8+
- Git

### 1. Клонирование репозитория
```bash
git clone <repository-url>
cd Client_Order_System
```

### 2. Создание виртуального окружения
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows
```

### 3. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 4. Применение миграций
```bash
python manage.py migrate
```

### 5. Создание суперпользователя (для доступа в админку)
```bash
python manage.py createsuperuser
```

### 6. Запуск сервера разработки
```bash
python manage.py runserver
```

Приложение будет доступно по адресу: **http://127.0.0.1:8000/**

## 🌐 Доступ к приложению

### Web Interface
- **Главная страница**: http://127.0.0.1:8000/
- **Админка**: http://127.0.0.1:8000/admin/
- **Регистрация**: http://127.0.0.1:8000/accounts/register/

### API Documentation
- **Swagger UI**: http://127.0.0.1:8000/api/docs/
- **ReDoc**: http://127.0.0.1:8000/api/redoc/
- **OpenAPI Schema**: http://127.0.0.1:8000/api/schema/

## 📚 API Документация

### Swagger UI
Интерактивная документация доступна по адресу: **http://127.0.0.1:8000/api/docs/**

Здесь вы можете:
- Просматривать все доступные API endpoints
- Тестировать API запросы прямо в браузере
- Видеть примеры запросов и ответов
- Просматривать параметры и типы данных

### REST API Endpoints

#### Клиенты
```
GET    /crm/api/clients/                    # Список клиентов с пагинацией
POST   /crm/api/clients/                    # Создание клиента
GET    /crm/api/clients/{id}/               # Получить клиента
PUT    /crm/api/clients/{id}/               # Обновить клиента
PATCH  /crm/api/clients/{id}/               # Частичное обновление
DELETE /crm/api/clients/{id}/               # Удалить клиента
```

#### Заказы
```
GET    /crm/api/orders/                     # Список заказов с пагинацией
POST   /crm/api/orders/                     # Создание заказа
GET    /crm/api/orders/{id}/                # Получить заказ
PUT    /crm/api/orders/{id}/                # Обновить заказ
PATCH  /crm/api/orders/{id}/                # Частичное обновление
DELETE /crm/api/orders/{id}/                # Удалить заказ
```

### Примеры API запросов

#### Получить список клиентов
```bash
curl -X GET http://127.0.0.1:8000/crm/api/clients/ \
  -H "Authorization: Token YOUR_TOKEN"
```

#### Создать нового клиента
```bash
curl -X POST http://127.0.0.1:8000/crm/api/clients/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token YOUR_TOKEN" \
  -d '{
    "name": "Иван Петров",
    "phone": "+7-999-123-45-67",
    "email": "ivan@example.com",
    "address": "ул. Пушкина, д. 1"
  }'
```

#### Получить конкретного клиента
```bash
curl -X GET http://127.0.0.1:8000/crm/api/clients/1/ \
  -H "Authorization: Token YOUR_TOKEN"
```

#### Создать заказ для клиента
```bash
curl -X POST http://127.0.0.1:8000/crm/api/orders/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token YOUR_TOKEN" \
  -d '{
    "client": 1,
    "total_price": "5000.00",
    "status": "New"
  }'
```

## 📖 Web Interface

### Регистрация и вход
1. Перейдите на главную страницу
2. Зарегистрируйтесь или войдите в систему

### Работа с клиентами
- **Просмотр списка**: `/clients/`
- **Добавление клиента**: `/clients/add/`
- **Редактирование**: `/clients/<id>/edit/`
- **Просмотр профиля**: `/clients/<id>/`

### Работа с заказами
- **Просмотр списка**: `/orders/`
- **Добавление заказа**: `/orders/add/`
- **Редактирование**: `/orders/<id>/edit/`
- **Изменение статуса**: `/orders/<id>/status/<status>/`

### Дашборд
Главная страница (`/`) содержит:
- Общую статистику (клиенты, заказы, выручка)
- Распределение заказов по статусам
- Графики динамики заказов и выручки по месяцам

## 📊 Модели данных

### Client (Клиент)
```python
- id: int (первичный ключ)
- name: string (не более 255 символов)
- phone: string (телефон)
- secondary_phone: string (дополнительный телефон, опционально)
- email: string (email, опционально)
- address: text (адрес, опционально)
- tags: string (теги через запятую, опционально)
- notes: text (заметки, опционально)
- user: ForeignKey (User) # Владелец записи
- created_at: datetime
- updated_at: datetime
```

### Order (Заказ)
```python
- id: int (первичный ключ)
- client: ForeignKey (Client)
- total_price: decimal (сумма заказа)
- status: CharField (New, In Progress, Done, Canceled)
- user: ForeignKey (User) # Владелец записи
- created_at: datetime
- updated_at: datetime
```

### Interaction (Взаимодействие)
```python
- id: int (первичный ключ)
- client: ForeignKey (Client)
- contact_type: CharField (Call, Email, Meeting, Note)
- note: text (заметка об взаимодействии)
- user: ForeignKey (User) # Владелец записи
- created_at: datetime
```

## 🔧 Конфигурация

### Переменные окружения
Создайте файл `.env` в корне проекта на основе `.env.example`.

Пример `.env` для разработки:
```env
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DJANGO_DB_ENGINE=django.db.backends.sqlite3
DJANGO_DB_NAME=db.sqlite3

# CORS (для frontend на другом хосте)
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

Пример `.env` для production:
```env
DJANGO_SECRET_KEY=your-production-secret-key
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database (PostgreSQL)
DJANGO_DB_ENGINE=django.db.backends.postgresql
DJANGO_DB_NAME=crm_db
DJANGO_DB_USER=postgres
DJANGO_DB_PASSWORD=your-password
DJANGO_DB_HOST=db.yourdomain.com
DJANGO_DB_PORT=5432

# Security
DJANGO_SECURE_SSL_REDIRECT=True
DJANGO_SESSION_COOKIE_SECURE=True
DJANGO_CSRF_COOKIE_SECURE=True

# CORS
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

### Статические файлы
Для продакшена выполните:
```bash
python manage.py collectstatic --noinput
```

### Docker запуск

#### Соберите и запустите контейнеры:
```bash
docker-compose build
docker-compose up -d
```

#### Применить миграции в контейнере:
```bash
docker-compose exec web python manage.py migrate
```

#### Создать суперпользователя в контейнере:
```bash
docker-compose exec web python manage.py createsuperuser
```

Приложение будет доступно на порту, указанном в `docker-compose.yml` (обычно http://localhost:8080).

## 🔄 REST Framework Configuration

В `settings.py` настроены:

```python
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': [
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Client Order System API',
    'DESCRIPTION': 'API документация для системы управления клиентами и заказами',
    'VERSION': '1.0.0',
    'SERVE_PERMISSIONS': ['rest_framework.permissions.IsAuthenticated'],
}
```

## 🛡️ Безопасность

- **Аутентификация**: Token-based authentication в API
- **Разрешения**: Каждый пользователь видит только свои данные
- **CORS**: Настроенная защита от кросс-доменных запросов
- **HTTPS**: Поддержка SSL/TLS в production
- **CSRF Protection**: Защита от CSRF атак
- **XSS Protection**: Заголовки безопасности

## 📝 Структура проекта

```
.
├── clientordersystem/       # Основные настройки Django
│   ├── settings.py         # Конфигурация проекта
│   ├── urls.py             # URL маршруты
│   ├── wsgi.py             # WSGI приложение
│   └── asgi.py             # ASGI приложение
│
├── crm/                    # Основное приложение
│   ├── models.py           # Модели данных
│   ├── views.py            # View функции/классы
│   ├── api.py              # REST API ViewSets
│   ├── serializers.py      # DRF сериализаторы
│   ├── forms.py            # Django формы
│   ├── urls.py             # URL маршруты приложения
│   ├── admin.py            # Администраторская панель
│   ├── management/
│   │   └── commands/
│   │       └── seed_data.py # Команда заполнения тестовых данных
│   ├── migrations/         # Миграции базы данных
│   └── templates/          # HTML шаблоны
│
├── nginx/                  # Конфигурация Nginx
│   └── nginx.conf
│
├── requirements.txt        # Python зависимости
├── Dockerfile             # Docker конфигурация
├── docker-compose.yml     # Docker Compose конфигурация
├── manage.py              # Django управление
├── db.sqlite3             # SQLite база данных
└── README.md              # Этот файл
```

## 🤝 Вклад в проект

1. Форкните репозиторий
2. Создайте ветку для вашей фичи (`git checkout -b feature/AmazingFeature`)
3. Зафиксируйте изменения (`git commit -m 'Add some AmazingFeature'`)
4. Отправьте в ветку (`git push origin feature/AmazingFeature`)
5. Создайте Pull Request

## 🐛 Известные проблемы

- Нет известных проблем на данный момент. Пожалуйста, откройте Issue если вы найдете ошибку.

## 📄 Лицензия

Этот проект распространяется под лицензией MIT. Подробности в файле `LICENSE`.

## 📞 Контакты

Если у вас есть вопросы или предложения:
- Создайте Issue в репозитории
- Свяжитесь с командой разработки

---

**Последнее обновление**: 16 апреля 2026
**Версия**: 1.0.0
**Статус**: В разработке