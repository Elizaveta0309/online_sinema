from clickhouse_driver import Client

client = Client(host='localhost')

client.execute('SHOW DATABASES')
[('_temporary_and_external_tables',),
 ('analysis',),
 ('default',),
 ('replica',),
 ('shard',),
 ('system',)]

## Измерения
clickhouse-node1 :) SELECT count() FROM analysis.viewed_progress

SELECT count()
FROM analysis.viewed_progress

┌──count()─┐
│ 10000000 │
└──────────┘

1 rows in set. Elapsed: 0.019 sec. 

clickhouse-node1 :) SELECT uniqExact(movie_id) FROM analysis.viewed_progress

SELECT uniqExact(movie_id)
FROM analysis.viewed_progress

┌─uniqExact(movie_id)─┐
│               10000 │
└─────────────────────┘

1 rows in set. Elapsed: 0.366 sec. Processed 10.00 million rows, 128.89 MB (27.31 million rows/s., 352.01 MB/s.) 

clickhouse-node1 :) SELECT uniqExact(user_id) FROM analysis.viewed_progress

SELECT uniqExact(user_id)
FROM analysis.viewed_progress

┌─uniqExact(user_id)─┐
│              10000 │
└────────────────────┘

1 rows in set. Elapsed: 0.239 sec. Processed 10.00 million rows, 128.89 MB (41.76 million rows/s., 538.29 MB/s.)

clickhouse-node1 :)