# Панель администратора для добавления запланированных рассылок и шаблонов для рассылок

> Заполнить переменные для .env

| Переменная | Описание | Значение по умолчанию |
| --- | --- | --- |
| POSTGRES_USER | имя пользователя (владельца) PostgreSQL |  |
| POSTGRES_PASSWORD | пароль пользователя (владельца) PostgreSQL |  |
| SECRET_KEY | используется для криптографической подписи (для генерации хэшей и токенов), длина ключа - 50 символов Генератор ключей Django: https://djecrety.ir |  |
| DB_HOST| ip-адрес или имя хоста PostgreSQL |  |
| DB_PORT | порт, который слушает PostgreSQL |  |
| SUPERUSER_USERNAME |  |  |
| SUPERUSER_PASSWORD |  |  |
| SUPERUSER_EMAIL |  |  |

### Запуск:

> Установить зависимости
 ```
 pip install requirements.txt
 ```
> Создать файл .env (по аналогии с .env.example)
> Собрать статические файлы
```
python3 manage.py collectstatic --no-input
```
> Применить миграции
```
python3 manage.py makemigrations notifications
python3 manage.py migrate notifications
```
> Создать пользователя
```
python3 manage.py createsuperuser
```
> Запустить приложение
```
python3 manage.py runserver
```
#### Стек
![](https://img.shields.io/badge/Python%20-3-informational) ![](https://img.shields.io/badge/django-project-yellow)  ![](https://img.shields.io/badge/Docker-Container-success) ![](https://img.shields.io/badge/Postgre-SQL-blueviolet)  ![](https://img.shields.io/badge/gunicorn-org-green)

- Backend фреймворк: [Django](https://www.djangoproject.com)
- База данных: [PostgreSQL](https://www.postgresql.org)
