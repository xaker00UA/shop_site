FROM python:3.12.6-slim

WORKDIR /app


COPY . /app/


RUN pip install  -r requirements.txt
CMD python manage.py migrate && \
 python manage.py makemigrations && \   
 python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(name='root').exists() or User.objects.create_superuser(name='root',email='root@gmail.com',password='root');"&&\
 python manage.py collectstatic --noinput &&\
 python -m parser.main  &\
 gunicorn shop.wsgi:application --bind 0.0.0.0:8000 --timeout 120 --workers 6 --worker-class gthread --threads 4