# Ссылка на дипломный проект:
https://github.com/Adedal513/graduate_work/
---
## Async API first sprint
Проект реализует асинхронный REST API для кинотеатра.

### Используемые технологии
- API написан на Python при помощи фреймворка FastAPI
- В качестве БД используется Elasticsearch
- Для кеширования запросов и работы ETL процесса используется Redis
- В качестве веб-сервера используется Nginx
- Проект запускается в Docker
### Установка

Клонируйте проект и перейдите в корневой каталог

```shell
git clone git@github.com:Elizaveta0309/Async_API_first_sprint.git
cd Async_API_first_sprint/
```

### Запуск

Разверните проект в Docker при помощи команды `docker-compose`:
```shell
docker-compose up -d
```

Документация станет доступна по адресу http://localhost/api/openapi

### Запуск тестов

В терминале войдите в контейнер с тестами

```
docker exec -it tests bash
```

Запустите тесты

```
pytest
```
