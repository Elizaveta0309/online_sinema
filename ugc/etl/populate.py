from uuid import uuid4
from confluent_kafka import Producer
from random import randint
from datetime import datetime
import json

p = Producer({'bootstrap.servers': 'localhost:9092'})

for _ in range(10):
    data = {
        'user_id': uuid4().hex,
        'film_id': uuid4().hex,
        'viewed_frame': randint(0,500),
        'created_at': datetime.now().isoformat()
    }
    p.produce('views', json.dumps(data).encode('utf-8'))

p.flush()