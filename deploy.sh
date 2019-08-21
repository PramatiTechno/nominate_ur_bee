#ssh to server
sudo git pull origin master
sudo docker build . -t nominate_ur_bee
sudo docker rm -f nyb
sudo docker run --name nyb -d -p 3003:3003 -e DB_NAME=nominate_ur_bee -e DB_USER=nominate_ur_bee -e CORE_PASSWORD=nominate_ur_bee -e CORE_HOST=34.224.233.43 -e DB_PORT=5432 -e SERVER_NAME="http://34.224.233.43:3003" -e CAS_URL="https://corridor-demo.pramati.com/cas/login" nominate_ur_bee
