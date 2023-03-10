create schema if not exists content;

create table if not exists content.film_work
(
    id            uuid default gen_random_uuid() not null
        primary key,
    title         text                           not null,
    description   text,
    creation_date date,
    rating        double precision,
    type          text                           not null,
    created_at       timestamp with time zone,
    updated_at      timestamp with time zone,
    file_path     text
);

create index film_work_creation_date_idx on content.film_work(creation_date);

create table if not exists content.person
(
    id        uuid default gen_random_uuid() not null
        primary key,
    full_name text                           not null,
    created_at   timestamp with time zone       not null,
    updated_at  timestamp with time zone       not null
);

create table if not exists content.person_film_work
(
    id           uuid      default gen_random_uuid() not null
        constraint person_film_work_pk
            primary key,
    person_id    uuid                                not null
        constraint person_id_fk
            references content.person
            on delete cascade,
    film_work_id uuid                                not null
        constraint film_work_id_fk
            references content.film_work
            on delete cascade,
    role         text,
    created_at      timestamp default CURRENT_DATE
);

create unique index film_work_person_idx on content.person_film_work (film_work_id, person_id, role);

create table if not exists content.genre
(
    id          uuid      default gen_random_uuid() not null
        constraint genre_pk
            primary key,
    name        text                                not null,
    description text,
    created_at     timestamp default CURRENT_DATE,
    updated_at    timestamp default CURRENT_DATE
);

create table if not exists content.genre_film_work
(
    id           uuid      default gen_random_uuid() not null
        constraint genre_film_work_pk
            primary key,
    genre_id     uuid                                not null
        constraint genre_id_fk
            references content.genre
            on delete cascade,
    film_work_id uuid                                not null
        constraint film_work_id_fk
            references content.film_work
            on delete cascade,
    created_at      timestamp default CURRENT_DATE
);


