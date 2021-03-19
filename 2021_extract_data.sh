#!/bin/bash

#/data/wordpress is a location of static copy of wordpress website made by wayback_machine_downloader

find /data/wordpress/20* -name "index.html" -exec python3 2021_extract_data.py {} \;
