```mermaid
---
title: Севрис нотификации
---
flowchart
    admin(Админ-панель)
    scheduler(Scheduler)
    api(API)
    worker(Worker)
    config_db[(Database)]
    notif_db[(Database)]
    rabbit[(RabbitMQ)]
    auth(Auth-сервис)
    email(Email Sender)


admin -->|настройка\nшаблонов и\nпериодичности\nрассылок| config_db
config_db -->|получение\nнастроек\nпериодичности| scheduler

scheduler -->|отправка\nпериодичных\nуведомлений| api
api -->|постановка сообщений\nв очередь| rabbit
rabbit -->|получение сообщений\nиз очереди| worker
config_db -->|получение шаблонов\nи URLs| worker
auth -->|получение данных\nо пользователях| worker


worker -->|отправка\nуведомлений| email
worker -->|сохранение истории\nотправки| notif_db

  