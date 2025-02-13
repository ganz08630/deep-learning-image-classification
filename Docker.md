🔥 Основні команди Docker

📌 Запуск та зупинка контейнерів

docker-compose up --build   # Запустити контейнер з пересозданням образу
docker-compose up -d        # Запустити у фоновому режимі
docker-compose down         # Зупинити та видалити контейнери
docker-compose stop         # Зупинити контейнери без видалення
docker-compose restart      # Перезапустити всі контейнери

📌 Перегляд контейнерів та логів

docker ps                  # Показати запущені контейнери
docker ps -a               # Показати всі контейнери (включаючи зупинені)
docker logs image-classifier  # Показати логи конкретного контейнера
docker logs -f image-classifier  # Дивитися логи в реальному часі

📌 Взаємодія з контейнером

docker exec -it image-classifier /bin/sh  # Увійти в контейнер (для налагодження)
docker stop $(docker ps -q)               # Зупинити всі контейнери
docker rm $(docker ps -aq)                # Видалити всі контейнери

📌 Очищення Docker (кеш, образи, контейнери)

docker system prune -a   # Видалити кеш, контейнери, непотрібні образи
docker image prune -a    # Видалити всі непотрібні образи
docker volume prune      # Видалити всі зайві Docker-томи
docker network prune     # Видалити всі непотрібні мережі
