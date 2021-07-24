PI_IP_ADDRESS=10.0.0.1
PI_USERNAME=pi

.PHONY: install-training
install-training:
	@cd training && virtualenv -p python3 env && . env/bin/activate && pip install -r requirements.txt

.PHONY: gather
gather:
	@echo "gathering images"
	@cd training && . env/bin/activate && python get_images_from_camera.py

.PHONY: run
run:
	@. env/bin/activate && cd src && export STREAM_URL=rtsp://username:password@camera_host/endpoint && python app.py

.PHONY: install
install:
	@cd scripts && bash install.sh

.PHONY: copy
copy:
	@rsync -a $(shell pwd) --exclude env --exclude training $(PI_USERNAME)@$(PI_IP_ADDRESS):/home/$(PI_USERNAME)

.PHONY: shell
shell:
	@ssh $(PI_USERNAME)@$(PI_IP_ADDRESS)

.PHONY: server
server:
	@echo "Running in server mode";
	@. env/bin/activate && cd src && python server.py
