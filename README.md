# Client Order System (CRM)

Современная веб-система управления клиентами и заказами на базе Django.

## 🚀 Возможности

### Основные функции
- **Управление клиентами**: создание, редактирование, просмотр профилей клиентов
- **Заказы**: полное управление жизненным циклом заказов
- **Аутентификация**: регистрация и авторизация пользователей
- **Изоляция данных**: каждый пользователь видит только свои данные

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
- **Database**: SQLite3
- **Frontend**: HTML5, CSS3, JavaScript
- **Authentication**: Django Auth
- **Charts**: Chart.js

## 📋 Установка и запуск

### Предварительные требования
- Python 3.8+
- Git

### 1. Клонирование репозитория
```bash
git clone <repository-url>
cd ClientOrderSystem
```

### 2. Создание виртуального окружения
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# или
.venv\Scripts\activate     # Windows
```

### 3. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 4. Применение миграций
```bash
python manage.py migrate
```

### 5. Создание суперпользователя (опционально)
```bash
python manage.py createsuperuser
```

### 6. Запуск сервера разработки
```bash
python manage.py runserver
```

Приложение будет доступно по адресу: http://127.0.0.1:8000/

## 📖 Использование

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

### Дашборд
Главная страница (`/`) содержит:
- Общую статистику (клиенты, заказы, выручка)
- Распределение заказов по статусам
- Графики динамики заказов и выручки по месяцам

## 📊 Модели данных

### Client (Клиент)
- `name` - Имя
- `phone` - Основной телефон
- `secondary_phone` - Дополнительный телефон
- `email` - Email
- `address` - Адрес
- `tags` - Теги (через запятую)
- `notes` - Заметки
- `user` - Владелец (ForeignKey)

### Order (Заказ)
- `client` - Клиент (ForeignKey)
- `total_price` - Сумма
- `status` - Статус (New/In Progress/Done/Canceled)
- `user` - Владелец (ForeignKey)

### Interaction (Взаимодействие)
- `client` - Клиент (ForeignKey)
- `contact_type` - Тип контакта (Call/Email/Meeting/Note)
- `note` - Заметка
- `user` - Владелец (ForeignKey)

## 🔧 Настройка

### Переменные окружения
Создайте файл `.env` в корне проекта на основе `.env.example`.
Файл `.env` загружается автоматически при старте приложения.

Пример `.env.example`:
```env
DJANGO_SECRET_KEY=replace-with-secret
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
DJANGO_DB_ENGINE=django.db.backends.sqlite3
DJANGO_DB_NAME=db.sqlite3
DJANGO_DB_USER=
DJANGO_DB_PASSWORD=
DJANGO_DB_HOST=
DJANGO_DB_PORT=
DJANGO_SECURE_SSL_REDIRECT=False
DJANGO_SESSION_COOKIE_SECURE=False
DJANGO_CSRF_COOKIE_SECURE=False
```

### Статические файлы
Для продакшена выполните:
```bash
python manage.py collectstatic
```

В `settings.py` настроены:
```python
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = '/static/'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

### Docker
Соберите контейнер и запустите стек:
```bash
docker compose build
docker compose up -d
```

Контейнеры:
- `web` — Django + Gunicorn
- `nginx` — прокси и отдача `/static/`

Приложение будет доступно на `http://77.95.206.95:8080`.

Статические файлы собираются автоматически на старте.

### Установка зависимостей
```bash
pip install -r requirements.txt
```

### Дополнительно
- В production обязательно установите `DJANGO_SECRET_KEY`
- Укажите `DJANGO_ALLOWED_HOSTS` для вашего домена
- При использовании HTTPS включите `DJANGO_SECURE_SSL_REDIRECT`, `DJANGO_SESSION_COOKIE_SECURE` и `DJANGO_CSRF_COOKIE_SECURE`

## 📝 API Endpoints

### Клиенты
- `GET /clients/` - Список клиентов
- `POST /clients/add/` - Создание клиента
- `GET /clients/<id>/` - Просмотр клиента
- `POST /clients/<id>/edit/` - Редактирование клиента
- `POST /clients/<id>/delete/` - Удаление клиента
- `GET /clients/export/csv/` - Экспорт в CSV

### Заказы
- `GET /orders/` - Список заказов
- `POST /orders/add/` - Создание заказа
- `GET /orders/<id>/` - Просмотр заказа
- `POST /orders/<id>/edit/` - Редактирование заказа
- `POST /orders/<id>/status/<status>/` - Изменение статуса
- `POST /orders/<id>/delete/` - Удаление заказа
- `GET /orders/export/csv/` - Экспорт в CSV

### Взаимодействия
- `POST /clients/<id>/interactions/add/` - Добавление взаимодействия

## 🤝 Вклад в проект

1. Форкните репозиторий
2. Создайте ветку для вашей фичи (`git checkout -b feature/AmazingFeature`)
3. Зафиксируйте изменения (`git commit -m 'Add some AmazingFeature'`)
4. Отправьте в ветку (`git push origin feature/AmazingFeature`)
5. Создайте Pull Request

## 📄 Лицензия

Этот проект распространяется под лицензией MIT. Подробности в файле `LICENSE`.

## 📞 Контакты

Если у вас есть вопросы или предложения, создайте Issue в репозитории.

---

**Примечание**: Это учебный проект для демонстрации возможностей Django в создании CRM систем.