### Проект для ознакомления с платежной системой Stripe

#### Эндпойнты:
-  /item/<item_id>/ — страница с информацией о товаре и кнопками купить/добавить в заказ
- buy/<item_id>/ — возвращает session_id для работы платежной системы
- order/ — страница с информацией о заказе
- order/buy/ — возвращает session_id для работы платежной системы и оплаты нескольких товаров одновременно

#### Запуск проекта в контейнерах

- Клонирование удаленного репозитория
```bash
git clone git@github.com:viator3m/payment_stripe.git
cd payment_server
```
- В директории /payment_server создайте файл .env, с переменными окружения, используя образец [.env.example](payment_server/payment_server/.env.example)
- Сборка и развертывание контейнеров
```bash
docker-compose up -d --build
```
- Выполните миграции, соберите статику, создайте суперпользователя
```bash
docker-compose exec backend python manage.py makemigrations
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py collectstatic --no-input
docker-compose exec backend python manage.py createsuperuser
```
- Стандартная админ-панель Django доступна по адресу [`https://localhost/admin/`](https://localhost/admin/)

#### Запуск API проекта в dev-режиме

- Клонирование удаленного репозитория (см. выше)
- Создание виртуального окружения и установка зависимостей
```bash
python -m venv venv
. venv/Scripts/activate (windows)
. venv/bin/activate (linux)
pip install --upgade pip
pip install -r -requirements.txt
```
- Примените миграции и соберите статику
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
```
- в файле [payment_server/setting.py](payment_server/payment_server/settings.py) замените БД на встроенную SQLite
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
```

- Запуск сервера
```bash
python manage.py runserver 
```
