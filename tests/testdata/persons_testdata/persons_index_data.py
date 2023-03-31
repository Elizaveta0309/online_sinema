import uuid

PERSON = {
    'uuid': '186d9a8e-392a-4e20-8353-8216edfc3f6d',
    'full_name': "Jim Kerry",
    'film_ids': [str(uuid.uuid4()), str(uuid.uuid4())]
}

PERSONS_DATA = [PERSON] + [
    {'uuid': str(uuid.uuid4()),
     'full_name': "Jim Kerry",
     'film_ids': [str(uuid.uuid4()), str(uuid.uuid4())]
     } for _ in range(60)
]
