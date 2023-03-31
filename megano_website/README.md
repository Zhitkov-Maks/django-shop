# Интернет магазин MEGANO.

---

## Инструкция по установке:
1. Создать виртуальное окружение
```
python -m venv venv
```
2Установить зависимости:  
```
pip install -r requirements.txt
```

3. Настроить базу данных PostgreSQL

4. Выполнить миграции.

```
python manage.py migrate
```

5. Загрузить тестовые данные в базу:

```
python manage.py loaddata settings.json
python manage.py loaddata user.json
python manage.py loaddata profile.json
python manage.py loaddata megano_tags.json
python manage.py loaddata megano_category.json
python manage.py loaddata megano_detail.json
python manage.py loaddata megano_goods.json
python manage.py loaddata megano_gallery.json
python manage.py loaddata megano_comment.json
python manage.py loaddata megano_discount.json
python manage.py loaddata megano_purchases.json
python manage.py loaddata megano_viewed_product.json
python manage.py loaddata order_status.json
python manage.py loaddata order.json
python manage.py loaddata order_detail.json
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