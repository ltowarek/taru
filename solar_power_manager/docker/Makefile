default: build

build:
	docker build -t rpi_mosquitto .

remove_image:
	docker rmi -f rpi_mosquitto

prune_all:
	docker system prune -a -f
	
rebuild: remove_image build

