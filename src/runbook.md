How to run locally:
docker-compose -f docker-compose-local.yml up

How to deploy to production:
Look into deployContainer.sh


How to make migrations on the local db:
docker-compose -f docker-compose-local.yml run web python3 manage.py makemigrations --settings=chillbet.localhost
docker-compose -f docker-compose-local.yml run web python3 manage.py migrate --settings=chillbet.localhost

How to make migrations in production:


Commands to run on first deployment
