FROM python:3.12-alpine

COPY . ./shop/
RUN pip install -r ./shop/requirements.txt

WORKDIR ./shop

CMD ["uvicorn", "megano_website.asgi:application", "--host", "0.0.0.0", "--port", "8000"]
