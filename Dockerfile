FROM python:3.12-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . ./shop/
RUN pip install -r ./shop/requirements.txt

WORKDIR ./shop

CMD ["gunicorn", "megano_website.wsgi:application", "--bind", "0.0.0.0:8000"]
