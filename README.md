# epdtext

A simple display manager app for the [WaveShare 2.7in e-Paper HAT](https://www.waveshare.com/2.7inch-e-paper-hat.htm)

## Screens

The app provides a number of screens that can be displayed on the e-paper HAT, and allows switching between them with the builtin buttons.

The included screens are:

* `uptime` - a system info viewer
* `affirmations` - display positive affirmations (or whatever kind you want, really)
* `fortune` - shows a random fortune from the fortune database (requires the `fortune-mod` package)
  * Install `fortune-mod` with this command: `sudo apt install fortune-mod`
* `calendar` and `tasks` - shows a list of upcoming events or todos from your calendars (see `local_settings.py.example`)

## Making your own

The framework is extensible, so you can write your own screens as well, each screen is a Python module providing a `Screen` class that inherits from `AbstractScreen`.

For more information on how to create your own screens, check the wiki.

## Message queue

There's also a message queue interface to control the screen from other apps. (example command line client available in `cli.py`)

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

* Install the remaining Python dependencies
```shell
cd ~/epdtext
sudo pip3 install -r requirements.txt
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

To reload using the CLI client:
```shell
cd ~/epdtext
./cli.py reload
```

To switch to the uptime screen with the CLI:
```shell
cd ~/epdtext
./cli.py screen uptime
```
