GENRES_QUERY = '''
WITH genres AS (
    SELECT g.*
    FROM content.genre g
    WHERE g.updated_at >= %s
    ORDER BY g.updated_at DESC
)
SELECT
    g.name,
    g.id as uuid,
    g.description,
    g.updated_at as modified,
    ARRAY_AGG(DISTINCT jsonb_build_object('fw_id', gfw.film_work_id)) AS array_id
FROM genres g
LEFT JOIN content.genre_film_work gfw
        ON gfw.genre_id = g.id
GROUP BY
    g.name,
    g.id,
    g.description,
    modified
ORDER BY modified DESC
'''

PERSONS_QUERY = '''
SELECT
    p.id as uuid,
    p.full_name,
    p.updated_at as modified,
   COALESCE (
       json_agg(
           DISTINCT jsonb_build_object(
               'fw_id', fw.id
           )
       ) FILTER (WHERE fw.id is not null),
       '[]'
   ) as array_id,
   array_agg(DISTINCT fw.id)::text[] as film_ids
FROM content.person p
LEFT JOIN content.person_film_work pfw ON pfw.person_id = p.id
LEFT JOIN content.film_work fw ON fw.id = pfw.film_work_id
WHERE p.updated_at > %s
GROUP BY p.id
ORDER BY p.updated_at DESC
'''

FILMWORK_QUERY = '''
WITH movies as (
    SELECT
    fw.id as uuid,
    fw.title,
    fw.description,
    fw.rating as imdb_rating,
    fw.type,
    fw.updated_at as modified,
    ARRAY_AGG(DISTINCT p.full_name) FILTER (WHERE pfw.role = 'actor') as actors_names,
    ARRAY_AGG(DISTINCT p.full_name) FILTER (WHERE pfw.role = 'writer') as writers_names,
    ARRAY_AGG(DISTINCT p.full_name) FILTER (WHERE pfw.role = 'director') as directors_names,
    ARRAY_AGG(DISTINCT jsonb_build_object('uuid', p.id, 'full_name', p.full_name)) FILTER (WHERE pfw.role = 'actor') as actors,
    ARRAY_AGG(DISTINCT jsonb_build_object('uuid', p.id, 'full_name', p.full_name)) FILTER (WHERE pfw.role = 'writer') as writers,
    ARRAY_AGG(DISTINCT jsonb_build_object('uuid', p.id, 'full_name', p.full_name)) FILTER (WHERE pfw.role = 'director') as directors,
    ARRAY_AGG(DISTINCT jsonb_build_object('uuid', g.id, 'name', g.name)) AS genre
    FROM content.film_work as fw
    LEFT JOIN content.person_film_work pfw
        ON pfw.film_work_id = fw.id
    LEFT JOIN content.person p
        ON p.id = pfw.person_id
    LEFT JOIN content.genre_film_work gfw
        ON gfw.film_work_id = fw.id
    LEFT JOIN content.genre g
        ON g.id = gfw.genre_id

    GROUP BY
        fw.id
)

SELECT mv.* FROM (
SELECT m.* FROM movies m
    WHERE m.modified >  %(checkpoint)s
    ORDER BY m.modified DESC
    LIMIT 100) mv
UNION ALL
SELECT mid.* FROM (
SELECT mm.*
    FROM movies mm
    WHERE mm.uuid IN %(movies_ids)s
    ORDER BY mm.modified) mid;
'''
