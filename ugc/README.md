##UGC

###Установка
 Из текущего каталога
 ```shell
docker-compose up -d
```
###Создание topic
После установки войти в контейнер и создать topic для kafka
 ```shell
sudo docker exec broker kafka-topics --bootstrap-server broker:9092 --create --topic views
```
