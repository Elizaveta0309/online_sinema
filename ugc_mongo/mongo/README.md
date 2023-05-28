# **MONGO**

> Для запуска необходимо выполнить:
> Установить зависимости
```
pip install -r requirements.txt
```

> Запустить docker-compose
```
docker-compose up -d --build
```

> Выполнить команды инициализации mongo из файла `init.sh`
> Запустить тест
```
python -m test_mongo
```

# Результат


### Patch Likes

| Size  |Time(sec)|
|:-----:|:-------:|
|  200  |  0.723  |
|  1000 |  3.422  |
|  5000 |  22.627|

### Patch Reviws

|  Size |Time(sec)|
|:-----:|:-------:|
|  200  |  0.919  |
|  1000 |  4.906  |
|  5000 |  25.741 |

### Patch Bookmarks

|  Size |Time(sec)|
|:-----:|:-------:|
|  200  |  0.934  |
|  1000 |  5.036  |
|  5000 |  25.281 |

### Reading (500 records)

|   Type   | Time (sec) |
|:--------:|:----------:|
|  likes   |   0.079    |
|  review  |   0.141    |
| bookmark |   0.079    |
