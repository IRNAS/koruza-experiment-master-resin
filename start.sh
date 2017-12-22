#!/bin/bash

# Enable i2c
modprobe i2c-dev

# Setup host DBUS socket location, which is needed for NetworkManager.
export DBUS_SYSTEM_BUS_ADDRESS=unix:path=/host/run/dbus/system_bus_socket

# Power off HDMI.
tvservice -o

# Start the main application.
./scripts/run-experiment.sh
