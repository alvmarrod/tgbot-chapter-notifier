IMAGE_NAME="tgbot-chaptnotifier"
IMAGE_VERSION?=$(shell cat version.txt)
BOT_CONTAINER_ALIAS=rogerbot

NOW_DATE_HOUR=$(shell date '+%Y_%m_%d_%H')
NOW_DATE_DAY=$(shell date '+%Y_%m_%d')
HOUR?=$(shell date '+%H')

docker-clean-image:
	-docker rmi `docker images -q --filter=reference=${IMAGE_NAME}:${IMAGE_VERSION}`

docker-build: docker-clean-image
	docker build -t ${IMAGE_NAME}:${IMAGE_VERSION} .

docker-run: docker-stop docker-remove
	docker run \
	--restart unless-stopped \
	--name ${BOT_CONTAINER_ALIAS}_${IMAGE_VERSION} \
	-d \
	--env-file ./src/.env \
	-v `pwd`/app/data:/app/data \
	${IMAGE_NAME}:${IMAGE_VERSION}

docker-stop:
	-docker stop `docker ps -q --filter name=${BOT_CONTAINER_ALIAS}_${IMAGE_VERSION}`

docker-resume:
	-docker start `docker ps -a -q --filter name=${BOT_CONTAINER_ALIAS}_${IMAGE_VERSION}`

docker-remove:
	-docker rm `docker ps -a -q --filter name=${BOT_CONTAINER_ALIAS}_${IMAGE_VERSION}`

docker-deploy: docker-build docker-run

docker-redeploy: docker-build docker-stop docker-remove docker-run

docker-logs:
	docker logs -f `docker ps -q --filter name=${BOT_CONTAINER_ALIAS}_${IMAGE_VERSION}`

test:
	( \
		test -d env || python3 -m venv env; \
		. env/bin/activate; \
		pip install -r dev-requirements.txt; \
		python -m coverage run -m unittest discover -s tests -p "*_test.py"; \
		python -m coverage html; \
		rm coverage_percentage.txt; \
		coverage report | tail -n 1 | tr -s " " | cut -d " " -f 4 >> coverage_percentage.txt; \
	)

run:
	( \
		test -d env || python3 -m venv env; \
		. env/bin/activate; \
		pip install -r requirements.txt; \
		python -m src.main; \
	)

docker-stats:
	docker stats

backup:
	mkdir -p /home/pi/ChapterNotifierBackup/data/${NOW_DATE_HOUR}
	cp `pwd`/app/data/* /home/pi/ChapterNotifierBackup/data/${NOW_DATE_HOUR}/

restoreback:
	cp /home/pi/ChapterNotifierBackup/data/${NOW_DATE_DAY}_${HOUR}/* `pwd`/app/data/