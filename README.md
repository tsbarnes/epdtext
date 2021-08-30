# epdtext

A simple display manager app for the WaveShare 2.7in e-Paper Display

## Setup on Raspberry Pi OS

* First, enable the SPI inferface on the Pi if you haven't already.
* Then, install the Python requirements

```shell
sudo apt install python3-pip python3-pil python3-numpy python3-gpiozero
```

* Then install the drivers for Python

```shell
git clone https://github.com/waveshare/e-Paper ~/e-Paper
cd ~/e-Paper/RaspberryPi_JetsonNano/python
python3 setup.py install
```

* Check out the code if you haven't already:

```shell
git clone https://github.com/tsbarnes/epdtext.git ~/epdtext
```

* Then (optionally) create local_settings.py and add your settings overrides there.
* Also optional is installing the systemd unit.

```shell
cp ~/epdtext/epdtext.service /etc/systemd/system
sudo systemctl enable epdtext
```

## Usage

To start up the app, run this command:
```shell
cd ~/epdtext
python3 app.py
```
