test:
	python3 -m unittest discover

lint:
	flake8 --config=flake8.ini --exclude=venv
	pylint monitor_consumer -d too-many-lines

up:
	docker-compose -f docker/docker-compose.yml up -d --build

down:
	docker-compose -f docker/docker-compose.yml down


start_producer:
	python3 -m monitor_producer.start

start_consumer:
	python3 -m monitor_consumer.start