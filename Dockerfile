# Python 3.11 asosiy image
FROM python:3.11-slim

# Ishchi papka
WORKDIR /app

# Kerakli paketlarni o'rnatish
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Kerakli Python paketlarini o'rnatish
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Loyiha fayllarini nusxalash
COPY . .

# Statik fayllarni yig'ish
RUN python manage.py collectstatic --noinput

# Port
EXPOSE 8000

# Ishga tushirish buyrug'i
CMD ["gunicorn", "university_admission.wsgi:application", "--bind", "0.0.0.0:8000"] 