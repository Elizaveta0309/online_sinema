from clickhouse_driver import Client
from pre_start import check_clickhouse_inited

c = Client(host='localhost')

check_clickhouse_inited(c)
print(c.execute("SELECT * FROM viewed_progress"))
c.disconnect()