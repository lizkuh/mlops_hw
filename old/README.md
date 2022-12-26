# mlops_hw (hw1 и hw2)
### Домашнее задание 1
### Кухарева Лиза
#### HW1
Дз 1
Реализовать API (REST либо процедуры gRPC), которое умеет:
+ 1. Обучать ML-модель с возможностью настройки
гиперпараметров. При этом гиперпараметры для разных
моделей могут быть разные. Минимальное количество классов
моделей доступных для обучения == 2.
2. Возвращать список доступных для обучения классов моделей
3. Возвращать предсказание конкретной модели (как следствие,
система должна уметь хранить несколько обученных моделей)
4. Обучать заново и удалять уже обученные модели

P.S
Я не совсем правильно прочитала задание, поэтому сделала на FastAPI 
небольшоай сайт. Методы сайта можно дергать и как REST API. 

Дз 2
Дз 3


# Docker commands
Создать образ docker
~
sudo docker build . -t mlops_hw
~

Запустить докер образ
~
sudo docker run -it --rm -v docker_temp:/app/docker_temp -p 8888:8888 -p 8080:8080 --name=fastapi_microservice mlops_hw

~

jupyter notebook --allow-root --ip 0.0.0.0
~

Запустить образ docker c postgress
~
sudo docker run -it --rm -v docker_temp:/app/docker_temp --name=postgres -e POSTGRES_PASSWORD=password postgres

~

Настроить для них общую сеть
~
docker network connect somenet fastapi_microservice
docker network connect somenet postgres
~
# # Build docker
# sudo docker build . -t mlops_hw

# # Run image
# sudo docker run -it mlops_hw

# # Send image to docker hub