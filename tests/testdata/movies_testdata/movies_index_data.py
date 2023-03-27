import uuid

MOVIES_DATA = [{
        'uuid': 'movie_id',
        "imdb_rating": 3.5,
        "genre": [
            {
                "name": "Action",
                "uuid": "3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff"
            },
            {
                "name": "Comedy",
                "uuid": "5373d043-3f41-4ea8-9947-4b746c601bbd"
            },
            {
                "name": "Sci-Fi",
                "uuid": "6c162475-c7ed-4461-9184-001ef3d9f26e"
            }
        ],
        "title": "Star Slammer",
        "description": "Two women who have been unjustly confined to a prison planet plot their escape,"
                       "all the while having to put up with lesbian guards, crazed wardens and mutant rodents.",
        "directors": [
            {
                "uuid": "a2fd6df4-9f3c-4a26-8d59-914470d2aea0",
                "full_name": "Fred Olen Ray"
            }
        ],
        "actors_names": [
            "Marya Gant",
            "Ross Hagen",
            "Sandy Brooke",
            "Suzy Stokey"
        ],
        "writers_names": [
            "Fred Olen Ray",
            "Michael Sonye",
            "Miriam L. Preissel"
        ],
        "directors_names": [
            "Fred Olen Ray"
        ],
        "actors": [
            {
                "uuid": "040147e3-0965-4117-8112-55a2087e0b84",
                "full_name": "Marya Gant"
            },
            {
                "uuid": "a91ff1c9-98a3-46af-a0d0-e9f2a2b4f51e",
                "full_name": "Suzy Stokey"
            },
            {
                "uuid": "b258f144-d771-4fa2-b6a2-42805c13ce4a",
                "full_name": "Sandy Brooke"
            },
            {
                "uuid": "f51f4731-3c26-4a72-9d68-cd0cd3d90a26",
                "full_name": "Ross Hagen"
            }
        ],
        "writers": [
            {
                "uuid": "82416ac7-26fa-40a6-a433-1c756c0fad6e",
                "full_name": "Miriam L. Preissel"
            },
            {
                "uuid": "a2fd6df4-9f3c-4a26-8d59-914470d2aea0",
                "full_name": "Fred Olen Ray"
            },
            {
                "uuid": "dac61d8f-f36e-4351-a4d8-9048b87d00a6",
                "full_name": "Michael Sonye"
            }
        ],
        "age_limit": None,
        "type": "movie",
        "creation_date": None
    } for _ in range(60)]
