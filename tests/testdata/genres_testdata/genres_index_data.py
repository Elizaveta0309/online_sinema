from uuid import uuid4

GENRE = {
    'uuid': '186d9a8e-392a-4e20-8353-8216edfc3f6d',
    'name': "Action"
}

GENRES_DATA = [GENRE] + [
    {
        'uuid': str(uuid4()),
        'name': "Action"
    } for _ in range(60)
]

print(GENRE)
