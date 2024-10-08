FROM python:3.12.6-slim

WORKDIR /app


COPY . /app/


RUN pip install  -r requirements.txt
CMD python manage.py migrate && \
 python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(name='root').exists() or User.objects.create_superuser(name='root',email='root@gmail.com',password='root');"&&\
 python manage.py collectstatic --noinput &&\
#  python manage.py runserver 0.0.0.0:8000
 gunicorn shop.wsgi:application --bind 0.0.0.0:8000 --timeout 120 --workers 6 \
