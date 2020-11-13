docker stop $(docker ps -q)
docker rm $(docker ps -aq)
docker rmi $(docker images -q) -f