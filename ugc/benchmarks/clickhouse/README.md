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

## ClickHouse

| Command | Time |
| ------ | ------ |
| SELECT count() FROM analysis.viewed_progress | Elapsed: 0.019 sec. |
| SELECT uniqExact(movie_id) FROM analysis.viewed_progress | Elapsed: 0.366 sec. Processed 10.00 million rows, 128.89 MB (27.31 million rows/s., 352.01 MB/s.)|
|SELECT uniqExact(user_id) FROM analysis.viewed_progress | Elapsed: 0.239 sec. Processed 10.00 million rows, 128.89 MB (41.76 million rows/s., 538.29 MB/s.) |
