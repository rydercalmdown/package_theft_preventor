PI_IP_ADDRESS=10.0.0.1
PI_USERNAME=pi
STREAM_URL=rtsp://username:password@camera_host/endpoint

.PHONY: run
run:
	@. env/bin/activate && cd src && export STREAM_URL=$(STREAM_URL) && python app.py

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
