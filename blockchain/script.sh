#!/bin/bash
sudo modprobe fuse
sudo groupadd fuse

user="$(whoami)"
sudo usermod -a -G fuse $user
# This script is used to start the blockchain network
/tmp/ganache-2.7.1-linux-x86_64.AppImage --host