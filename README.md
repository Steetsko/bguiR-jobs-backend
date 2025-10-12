# bguiR-jobs-backend
Репозиторий бэк

# BSUIR Jobs Backend

## Запуск локально
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

## Переменные окружения
DJANGO_SECRET_KEY=change-me
DJANGO_DEBUG=1
ALLOWED_HOSTS=127.0.0.1,localhost
DATABASE_URL=sqlite:///db.sqlite3
