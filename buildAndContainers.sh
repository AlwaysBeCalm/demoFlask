docker build -t simple_python . # --network host

title=abdullah
POSTGRES=postgres
NETWORK=simple_python

docker stop simple_python $POSTGRES
docker rm simple_python $POSTGRES
docker network rm $NETWORK
docker network create $NETWORK


docker run -id --name $POSTGRES --network $NETWORK \
  --hostname $POSTGRES \
  -e POSTGRES_DB=$title \
  -e POSTGRES_USER=$title \
  -e POSTGRES_PASSWORD=$title \
  -p 5432:5432 \
  $POSTGRES

docker run -it --name simple_python --network $NETWORK \
  --hostname simple_python \
  -e db_user=$title \
  -e db_pass=$title \
  -e db_name=$title \
  -e db_host=$POSTGRES \
  -p 5000:5000 simple_python
