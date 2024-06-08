mkdir -p data-postgres

docker run -d -ti --rm --name postgres-server \
    -e POSTGRES_PASSWORD='Networking@123' \
    -v ./data-postgres:/var/lib/postgresql/data:rw \
    -p 5432:5432 \
    postgres