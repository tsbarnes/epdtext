# epdtext

A simple display manager app for the [WaveShare 2.7in e-Paper HAT](https://www.waveshare.com/2.7inch-e-paper-hat.htm)

![Picture](/screenshots/picture.jpg)

## Screens

The app provides a number of screens that can be displayed on the e-paper HAT, and allows switching between them with the builtin buttons.

The included screens are:

* `dashboard` - a dashboard widget showing the current weather, next calendar event, and next task

![Screenshot](/screenshots/dashboard.png)

* `uptime` - a system info viewer

![Screenshot](/screenshots/system.png)

* `affirmations` - display positive affirmations (or whatever kind you want, really)

![Screenshot](/screenshots/affirmations.png)

* `fortune` - shows a random fortune from the fortune database (requires the `fortune-mod` package)
  * Install `fortune-mod` with this command: `sudo apt install fortune-mod`

![Screenshot](/screenshots/fortune.png)
* `calendar` and `tasks` - shows a list of upcoming events or todos from your calendars (see `local_settings.py.example`)

![Screenshot](/screenshots/calendar.png)
![Screenshot](/screenshots/tasks.png)

* `weather` - shows the current weather

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
  * You can copy `local_settings.py.example` to `local_settings.py` and edit it to configure `epdtext`
  * **NOTE**: if you're using a different Waveshare screen, you can use the `DRIVER` setting to configure it
  * See the wiki for more configuration help

* Also optional is installing the systemd unit.

```shell
cp ~/epdtext/epdtext.service /etc/systemd/system
sudo systemctl enable epdtext
```

## Setup on Arch Linux ARM

* First, enable the SPI inferface on the Pi if you haven't already.
* Then, install the Python requirements

```shell
sudo apt install python-pip python-pillow python-numpy python-gpiozero
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
sudo pip install -r requirements.txt
```

* Then (optionally) create local_settings.py and add your settings overrides there.
  * You can copy `local_settings.py.example` to `local_settings.py` and edit it to configure `epdtext`
  * **NOTE**: if you're using a different Waveshare screen, you can use the `DRIVER` setting to configure it
  * You'll have to set the `LOGO` setting, as it defaults to assuming it's installed in `/home/pi`
  * See the wiki for more configuration help

* Also optional is installing the systemd unit.

```shell
cp ~/epdtext/epdtext.service /etc/systemd/system
```

You'll need to edit the `/etc/systemd/system/epdtext.service` file and change `/home/pi` to `/home/alarm`
(or the home directory of the user you checked it out as) and change the User line to root.

Also of note, on Arch Linux ARM, epdtext must be run as root.

## Usage

To start up the app without `systemd`, run this command:
```shell
cd ~/epdtext
python3 app.py
```

To start the app with ´systemd´, run this:
```shell
sudo systemctl start epdtext
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

## epdtext-web

There's now a web frontend to epdtext! Check out [epdtext-web](https://github.com/tsbarnes/epdtext-web)
