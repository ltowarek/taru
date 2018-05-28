default: build

build:
	docker build -t rpi_mosquitto_broker .

remove_image:
	docker rmi -f rpi_mosquitto_broker
	
rebuild: remove_image build

