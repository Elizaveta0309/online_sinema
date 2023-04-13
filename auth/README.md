### Создание суперпользователя:

Войти в контейнер auth

```
docker exec -it auth bash
```

Запустить команду и ввести логин и пароль для суперпользователя

```
python manage.py createsuperuser
```