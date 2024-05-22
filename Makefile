build:
	docker build . -t sep/funda:develop

run:
	docker run sep/funda:develop

develop:
	python src/main.py

yeet: build
	docker tag sep/funda:develop europe-west4-docker.pkg.dev/funda-424117/prod/fundascraper
	docker push europe-west4-docker.pkg.dev/funda-424117/prod/fundascraper

gcloud-init:
	gcloud init

gcloud-auth:
	gcloud auth configure-docker europe-west4-docker.pkg.dev

deploy:
	gcloud run services replace gcloud_service.yaml