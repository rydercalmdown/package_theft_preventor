RTSP_URL=rtsp://username:password@10.0.0.1/live
SLEEP_SECONDS=10
GCS_BASE=gs://your-bucket-here


.PHONY: no-package-images
no-package-images:
	@echo "Taking photos with camera"
	@echo "There should be no packages at your front door"
	@source env/bin/activate \
		&& export PACKAGE_PRESENT=false \
		&& export RTSP_URL=$(RTSP_URL) \
		&& export SLEEP_SECONDS=$(SLEEP_SECONDS) \
		&& python get_images_from_camera.py

.PHONY: package-images
npackage-images:
	@echo "Taking photos with camera"
	@echo "There should be some sort of package at your front door"
	@source env/bin/activate \
		&& export PACKAGE_PRESENT=false \
		&& export RTSP_URL=$(RTSP_URL) \
		&& export SLEEP_SECONDS=$(SLEEP_SECONDS) \
		&& python get_images_from_camera.py

.PHONY: generate-csv
generate-csv:
	@echo "Generating CSV"
	@source env/bin/activate \
	&& export GCS_BASE=$(GCS_BASE) \
	&& python create_automl_csv.py
