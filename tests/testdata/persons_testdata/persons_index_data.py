import uuid

PERSONS_DATA = [
    {'uuid': str(uuid.uuid4()),
     'full_name': "Jim Kerry",
     'film_ids': [str(uuid.uuid4()), str(uuid.uuid4())]
     } for _ in range(60)
]