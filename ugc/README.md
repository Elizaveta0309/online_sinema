UGC
Установка
docker-compose up -d

После установки войти в контейнер и создать topic для kafka
sudo docker exec broker kafka-topics --bootstrap-server broker:9092 --create --topic views

