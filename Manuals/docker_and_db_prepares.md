# 1. Подготовка

**How To Install and Use Docker Compose on Ubuntu 24.04**

[Docker install manual](https://docs.docker.com/engine/install/ubuntu/)

1. Установка `docker`  

```
sudo apt install docker.io -y
```
2. Установка `docker compose`
```
sudo apt install docker-compose-v2
``` 


**Добавить программу `just`**  
[Just a command runner](https://github.com/casey/just)

```
sudo apt install just
```


## Запуск Postgres DB используя `docker compose`

`.env` файл: 

```
POSTGRES_USER=buser
POSTGRES_PASSWORD=pswd
POSTGRES_DB=booksdb
```


`docker-compose.yml` файл: 

```
services:
  db:
    container_name: postgresdb
    image: postgres:17.2
    environment:
      POSTGRES_DB: "${POSTGRES_DB}"
      POSTGRES_USER: "${POSTGRES_USER}"
      POSTGRES_PASSWORD: "${POSTGRES_PASSWORD}"
    volumes:
      - booksdb-data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U app_user -d ${POSTGRES_USER}"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 10s

volumes:
  booksdb-data:
```

## Запуск `docker контейнера`
```
docker compose up -d
```

## Остановка `docker контейнера`
С удалением контейнера
```
docker compose down
```
Без удаления
```
docker compose stop
```


### Check container

```
docker ps
```

*Если возникнет ошибка доступа к сокету:*
- [либо добавить текущего пользователя в группу docker](https://www.digitalocean.com/community/questions/how-to-fix-docker-got-permission-denied-while-trying-to-connect-to-the-docker-daemon-socket)
- либо изменить права доступа `sudo chmod 666 /var/run/docker.sock`
- либо добавить `sudo` вначале каждой команды


### Check database 

Docker compose command
```
docker compose exec -it db psql -U buser -d booksdb
```
Check existing database
```
postgres=# \l
```

Check new table in DB
```
postgres=# \c booksdb
```
