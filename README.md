# koruza-experiment-master-resin
Master device for controlling KORUZA experimental deployment for use with http://resin.io management system for embedded devices.

This code allows for deployment of a KORUZA experiment as described in https://github.com/IRNAS/koruza-experiment-v2 and is to be uploaded to a Raspberry Pi device currently implementing the following functions:
 * `scripts/link-test.py` ssh into test routers and run ping to measure packet loss
 * `scripts/weather.py` collect measurements from a weather station Renkforce WH2600
 * custom scripts can be easily added to support additional sensors

This device then reports the measurements to Nodewatcher platform, for example http://kw.koruza.net or other custom deployment. To report correct measurements and associate them with the right KORUZA Pro devices, correct configuration is required.

## Configuration
Configuration is done by placing files on a resin managed device into the `/data` partition, the following is required:
 * `/data/config.yml` contains the information about the experiment setup and links
 * `/data/secrets.yml` contain the HMAC access key to write measurements to nodewatcher, make sure you introduce a trusted HMAC key to nodewatcher for every unit you wish reporting to be part of

Sample configuration files are part of this repository in folder `data`. Create the config file and copy it to correct partition.
