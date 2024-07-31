# Интернет магазин MEGANO.

---

## Инструкция по установке:

- В настройках в ALLOWED_HOSTS нужно добавить адреса вашего сервера.
- Так же у вас должен быть .env файл в котором нужно указать все нужные
переменные окружения.

- Сгенерировать статические файлы, для чего предварительно
должен быть установлен django.

```
python3 manage.py collectstatic
```

Для запуска приложения должен быть установлен 
[docker](https://docs.docker.com/engine/install/ubuntu/)

- Запуск 

```
docker compose up -d
```

- Далее нужно выполнить миграции, для этого нужно перейти в контейнер с самим
приложением.
```
docker exec -ti <container_id> sh
python3 manage.py migrations
```

- И загрузить данные из фикстур.
```
python3 manage.py loaddata settings.json
```

```
python3 manage.py loaddata users.json
```

```
python3 manage.py loaddata megano.json
```

```
python3 manage.py loaddata orders.json
```

Тестовый суперпользователь:    
```
Логин: admin@inbox.ru Пароль: admin
```
