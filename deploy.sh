#!/bin/bash
if [ ! -d /bin/internet_monitor ]; then
	mkdir -p /bin/internet_monitor;
fi

cp ./scan.py /bin/internet_monitor/scan.py
