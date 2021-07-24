# Package Theft Prevention Device
An AI-powered device to stop people from stealing my packages.

## Installation
To install on a raspberry pi, clone the repository and run:
```bash
make install
```

## Running
To run the system on the raspberry pi entirely, make sure self.server_mode is set to False in app.py, then use the following command.

```bash
make run
```

For more performance, you can run just the relay components on your Pi, and the inference/processing on a more powerful machine. To do this, run the following on the pi:

```bash
make server
```

Then set self.server_mode = True in app.py, and set the environment variable ALARM_ENDPOINT to the alarm endpoint of your raspberry pi, which will look something like:

```bash
export ALARM_ENDPOINT="http://your_pis_ip_address:8000/alarm/"
```

Then run the following on the more powerful system

```bash
make run
```

## Notes
The training dir doesn't actually contain code for training the model; I used GCP's vision AutoML. That dir has code for gathering images from an RTSP cam, and putting them in the format GCP needs.

My trained model is included as a .tflite file, though it probably won't work with your front door, you're best to train your own. Good luck!
