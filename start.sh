#!/bin/bash

# Enable i2c
modprobe i2c-dev

# Setup host DBUS socket location, which is needed for NetworkManager.
export DBUS_SYSTEM_BUS_ADDRESS=unix:path=/host/run/dbus/system_bus_socket

# Start the main application.
echo "Running all KORUZA experiment monitoring scripts."
nohup python ./scripts/link-test.py > /var/log/koruza-link-test.log &
nohup python ./scripts/weather.py > /var/log/koruza-weather.log &
wait
