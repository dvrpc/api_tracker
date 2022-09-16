#!/bin/bash                                         

# activate the virtual environment and then run the script
source /srv/api/api_tracker/ve/bin/activate

python /srv/api/api_tracker/crawler/crawler.py
