# Интернет магазин MEGANO.

---

## Инструкция по установке:
1. Создать виртуальное окружение
```
python -m venv venv
```
2. Установить зависимости:  
```
pip install -r requirements.txt
```

3. Установить и настроить PostgreSQL

4. Выполнить миграции.

```
python manage.py migrate
```

5. Загрузить тестовые данные в базу:

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

6. Запустить тестовый сервер:
```
python manage.py runserver
```

7. Перейдите по ссылке: [localhost](http://127.0.0.1:8000)

Тестовый суперпользователь:    
```
Логин: admin@inbox.ru Пароль: admin
```
