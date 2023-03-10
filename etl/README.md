# ETL

## Подготовка

Для работы ETL требуются переменные среды:

`POSTGRES_HOST `- Хост Postgres

`POSTGRES_PORT` - Порт Postgres

`POSTGRES_DB` - Название БД

`POSTGRES_USER` - Имя пользователя

`POSTGRES_PASSWORD` - Пароль пользователя


`ES_HOST` - Хост Elasticsearch

`ES_PORT` - Порт Elasticsearch

`REDIS_HOST` - Хост Redis

`REDIS_PORT` - Порт Redis

`ETL_DEBUG` - Режим debug. Определяет уровень логирования

`ETL_SLEEP_TIME` - Время в секундах между попытками выгрузки данных

Для удобства, можно заранее записать все переменные в файл `.env` и экспортировать переменные командой

```shell
source .env
```

##  Запуск

Запуск ETL-процесса происходит командой:

```shell
python3 load_data.py
```

Процесс будет продолжать выгружать данные с перерывом в 10 секунд.