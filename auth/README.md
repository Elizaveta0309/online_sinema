# Auth

После установки войти в контейнер

```
docker exec -it auth bash
```

Запустить создание таблиц базы данных

```
alembic revision --autogenerate
alembic upgrade head
```

### Создание суперпользователя:


Войти в контейнер auth

```
docker exec -it auth bash
```

Запустить команду и ввести логин и пароль для суперпользователя

```
python manage.py createsuperuser
```