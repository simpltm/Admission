# Система приёма заявлений в университет

Современное веб-приложение для управления процессом приёма заявлений в университет.

## Функциональность

- 📊 Панель администратора с аналитикой и управлением
- 📝 Форма подачи заявлений для абитуриентов
- 📚 Управление направлениями подготовки
- 📈 Система отчётов и аналитики
- 📄 Генерация PDF-документов
- 🔍 Поиск и фильтрация данных

## Технологии

- Python 3.11+
- Django 5.0
- Bootstrap 5
- PostgreSQL
- ReportLab (для PDF)
- Pillow (для работы с изображениями)

## Установка

1. Клонировать репозиторий:
```bash
git clone [url-репозитория]
cd DjangoAdmission
```

2. Создать виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # для Linux/Mac
venv\Scripts\activate     # для Windows
```

3. Установить зависимости:
```bash
pip install -r requirements.txt
```

4. Создать файл .env в корневой директории:
```
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
```

5. Применить миграции:
```bash
python manage.py migrate
```

6. Создать суперпользователя:
```bash
python manage.py createsuperuser
```

7. Запустить сервер разработки:
```bash
python manage.py runserver
```

## Структура проекта

- `home_app` - главная страница
- `applications_app` - управление заявлениями абитуриентов
- `programs_app` - управление направлениями подготовки
- `dashboard_app` - панель администратора
- `reports_app` - система отчётов

## Лицензия

MIT 