FROM python:3
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . ./

#CMD python manage.py runserver 127.0.0.1:8000
CMD exec gunicorn account.wsgi:application --bind 0.0.0.0:8000 --workers 10 --threads 1