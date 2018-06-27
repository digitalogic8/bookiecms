How to deploy to production:



How to make migrations on a container:
docker-compose -f docker-compose-local.yml run web python3 manage.py makemigrations --settings=chillbet.localhost
docker-compose -f docker-compose-local.yml run web python3 manage.py migrate --settings=chillbet.localhost