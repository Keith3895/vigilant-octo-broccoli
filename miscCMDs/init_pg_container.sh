docker pull postgres

docker run -d \
    --name some-postgres \
    -e POSTGRES_PASSWORD=mysecretpassword \
    -e PGDATA=/var/lib/postgresql/data/pgdata \
    -v /Users/keithfranklin/Documents/Exploring\ Programming/identity-service/dbdata:/var/lib/postgresql/data \
    -p 5432:5432 \
    postgres
