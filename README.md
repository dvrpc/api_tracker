# api_tracker

This repo contains a crawler and an API. The crawler looks for DVRPC domains in files used in web products on the production server (mounted at /mnt/w on linux3.dvrpc.org), and saves that information in a database on a nightly basis. See crawler/crawler.py for additional details. The API then exposes that information to the frontend (see <https://github.com/dvrpc/API-Inventory>). The API documentation is located at <http://linux3.dvrpc.org/api/api-tracker/v1/docs>.
