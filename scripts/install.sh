#!/bin/bash
# install.sh

cd ../

echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | sudo tee /etc/apt/sources.list.d/coral-edgetpu.list
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
sudo apt-get update
sudo apt-get install -y python3-tflite-runtime ffmpeg git \
    libsm6 libxext6 python-pip python3-pip git \
    libatlas-base-dev python3-h5py libgtk2.0-dev libgtk-3-0 \
    libilmbase-dev libopenexr-dev libgstreamer1.0-dev \
    espeak gnustep-gui-runtime libsm6 \
    libhdf5-dev libc-ares-dev libeigen3-dev

sudo apt-get install -y openmpi-bin libopenmpi-dev
sudo apt-get install -y libatlas-base-dev


python3 -m pip install virtualenv
python3 -m virtualenv -p python3 env
. env/bin/activate

python3 -m pip install keras_applications==1.0.8 --no-deps
python3 -m pip install keras_preprocessing==1.1.0 --no-deps
python3 -m pip install h5py==2.9.0
python3 -m pip install -U six wheel mock RPi.GPIO==0.7.0

wget https://github.com/lhelontra/tensorflow-on-arm/releases/download/v2.4.0/tensorflow-2.4.0-cp37-none-linux_armv7l.whl
python3 -m pip uninstall -y tensorflow
python3 -m pip install tensorflow-2.4.0-cp37-none-linux_armv7l.whl


cd src && pip install -r requirements.txt
