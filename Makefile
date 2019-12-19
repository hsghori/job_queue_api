all:
	@pip install -r requirements.txt
	@python manage.py makemigrations
	@python manage.py migrate

shell:
	@docker exec -ti queue_api bash

start:
	docker-compose up

build:
	docker-compose build

flush:
	python manage.py flush
