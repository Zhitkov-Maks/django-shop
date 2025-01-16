FROM python:3.13

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . ./shop/
RUN pip install -r ./shop/requirements.txt

WORKDIR ./shop
RUN chmod +x wait-for-it.sh

CMD ["sh", "-c", "./wait-for-it.sh db:5432 -- python manage.py migrate && gunicorn megano_website.wsgi:application --bind 0.0.0.0:8000"]
