# Python 3.11 asosiy image
FROM python:3.11-slim

# Ishchi papka
WORKDIR /app

# PostgreSQL client kerak bo‘lsa
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Python paketlar
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Loyihani ko‘chirish
COPY . .

# Environment o‘zgaruvchini sozlash (statik uchun)
ENV DJANGO_SETTINGS_MODULE=university_admission.settings

# Statik fayllarni yig‘ish
RUN python manage.py collectstatic --noinput

# Port
EXPOSE 8000

# Gunicorn orqali ishga tushirish
CMD ["gunicorn", "university_admission.wsgi:application", "--bind", "0.0.0.0:8000"]
