# mlops_hw (hw1, hw2, hw3)
### Домашнее задание 1
### Кухарева Лиза


### Описание
Что сделала

        Дз1:
        + Dсе работает, провела серьзеный рефакторигн всего
        + Swagger: http://localhost:8080/redoc
        - Переделать requirements.txt (взять другой докер образ)

        Дз2:
        + Работа с базой postgress и ORM подо
        + Docker для микросервиса
        - Сделать docker compose и залить в dockerhub

        Дз3:
        + Есть тесты (но не в правильном формате)
        - Оформить из в pytest 
        - Настроить CI/CD

        - Дописать ReadMe

#### Что надо было сделать
Дз 1 (12)
Реализовать API (REST либо процедуры gRPC), которое умеет:
1. Обучать ML-модель с возможностью настройки
гиперпараметров. При этом гиперпараметры для разных
моделей могут быть разные. Минимальное количество классов
моделей доступных для обучения == 2.
2. Возвращать список доступных для обучения классов моделей
3. Возвращать предсказание конкретной модели (как следствие,
система должна уметь хранить несколько обученных моделей)
4. Обучать заново и удалять уже обученные модели

Оценка
+• [4 балла] Работоспособность программы - то что ее можно запустить и
она выполняет задачи, перечисленные в требованиях.
+• [3 балла] Корректность и адекватность программы - корректная
обработка ошибок, адекватный выбор структур классов, понятная
документация (docstring-и адекатные здесь обязательны)
-+• [2 балла] Стиль кода - соблюдение стайлгайда. Буду проверять flake8
(не все ошибки на самом деле являются таковыми, но какие можно
оставить – решать вам, насколько они критичны, списка нет )
+• [1 балл] Swagger – Есть документация API (Swagger) с помощью flask-
restx или аналога
• [2 балла] – Реализация и REST API, и gRPC

Дз 2 (11)
К приложению из первого дз нужно добавить:
1. Работу с базой данной Postgresql.
2. Сборку самого вашего микросервиса в docker образ (образ
нужно запушить в docker hub)
3. Запуск вашего сервиса и БД через docker-compose
4. [полуопционально] Запуск вашего сервиса в кубере
5. [на будущее] Написать тесты

Оценка
+• [3 балла] В приложение добавлена работа с БД
-+• [3 балла] Получившееся приложение собрано в Docker-образ и он
опубликован в DockerHub
-• [3 балла] Приложение можно запустить утилитой docker-compose
• [2 балла] Приложение запускается на Kubernetes (требуется
приложить скрипт поднятия кластера minikube и деплоймент,
либо Mak

Дз 3 ()
К приложению из второго дз нужно добавить:
1. Unit тесты. Работу с БД/S3 замокать
2. CI пайплайн:
1. Запуск тестов
2. Сборка образа и пуш ее в докерхаб

Оценка
-+• [10 баллов] Есть тесты, они достаточно полные.
• [5 баллов] Есть CI Pipeline, который запускается при Merge
Request-ах

# Docker commands
Создать образ docker
~
sudo docker build . -t mlops_hw
~

Запустить докер образ
~
sudo docker run -it --rm -v docker_temp:/app/docker_temp -p 8888:8888 -p 8080:8080 --name=fastapi_microservice mlops_hw



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