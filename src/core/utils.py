def get_items_source(data):
    return list(map(lambda x: x['_source'], data['hits']['hits']))


def build_cache_key(f, args, obj) -> str:
    query = ':'.join(map(str, obj.__dict__.values()))

    return (
            f.__name__
            + ':'
            + str(args.index)
            + ':'
            + query
    )
