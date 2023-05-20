```sh
from clickhouse_driver import Client

client = Client(host='localhost')

client.execute('SHOW DATABASES')
[('_temporary_and_external_tables',),
 ('analysis',),
 ('default',),
 ('replica',),
 ('shard',),
 ('system',)]
```

## Измерения

## ClickHouse [10 000 000]

| Command | Time |
| ------ | ------ |
|SELECT count() FROM analysis.viewed_progress | 0.015 sec.|
|SELECT uniqExact(user_id) FROM analysis.viewed_progress | 0.239 sec.|
|SELECT user_id, uniqExact(movie_id) FROM analysis.viewed_progress GROUP by user_id| 5.834 sec.|

## Vertica [8 031 452]

| Command                                                                                      | Time |
|----------------------------------------------------------------------------------------------| ------ |
| SELECT COUNT(*) FROM views [8031452]                                                         | 0.079 |
| SELECT count(DISTINCT user_id) FROM views [10000]                                            | 0.214 |
| SELECT user_id, count(distinct movie_id) FROM views GROUP by user_id                         | 9.538 |