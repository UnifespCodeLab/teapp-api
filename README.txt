docker network create --driver bridge docker-network

docker build -t flask-api .
docker run --name ibeac-flask --network=docker-network -p 7777:7777 -v /home/mmagueta/docker-flask-postgres/app:/app -d flask-api
docker exec -it flask-api-container bash

docker run --name ibeac-postgres --network=docker-network -e "POSTGRES_PASSWORD=ziviani123" -p 5432:5432 -v /home/mmagueta/postgresql/:/var/lib/postgresql/data -d postgres

docker run --name ibeac-pgadmin --network=docker-network -p 15432:80 -e "PGADMIN_DEFAULT_EMAIL=codelab.unifesp@gmail.com" -e "PGADMIN_DEFAULT_PASSWORD=ziviani123" -d dpage/pgadmin4