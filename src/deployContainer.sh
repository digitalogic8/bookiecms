#python3 manage.py makemigrations --settings=chillbet.production
#python3 manage.py migrate --settings=chillbet.production
docker build -t chillbet .
docker tag chillbet:latest 923516984695.dkr.ecr.us-east-1.amazonaws.com/chillbet:latest
eval "$(aws ecr get-login --no-include-email --region us-east-1)"
docker push 923516984695.dkr.ecr.us-east-1.amazonaws.com/chillbet:latest
#ecs-cli compose --file docker-compose-production.yml --project-name chill-bet service up