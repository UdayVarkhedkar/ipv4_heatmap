README
======

This repository is for an interactive heatmap of all IPv4 addresses in the world. The heatmap is powered by an API endpoint which returns a list of coordinates of IPv4 addresses within a geographic coordinate area. The coordinate data for the IPv4 addresses is based upon [GeoLite2 data](https://dev.maxmind.com/geoip/geoip2/geolite2/).

[See the heatmap in production here.](https://sleepy-savannah-76404.herokuapp.com/) 


## Usage

Git clone this repo. There are a couple of necessary files that aren't included in this repo. The GeoLite2 csv is `Geolite2-City-Blocks-IPv4.csv` and can be installed [here](https://dev.maxmind.com/geoip/geoip2/geolite2/). In the root directory of this repository, create a `config.py` file that defines the `DB_NAME`, `DB_USER`, and `DB_PASS` for your local postgresql database. Additionally, create a `static/website/config.js` file that defines the `mapbox_access_token` used to retrieve the tiles for the leaflet map (This can be created for free [here](https://account.mapbox.com/auth/signup/?route-to=%22/access-tokens/%22)). Also, use `pip install -r requirements.txt` to install the dependencies specified.

After the initial file setup, run `python manage.py makemigrations` and `python manage.py migrate` in the root directory. Then run `python manage.py import_ip_locations [INSERT CSV FILE NAME HERE]` to import the ip network location data into your database. You may want to also run `python manage.py createsuperuser` to access the `/admin/` page. 

Finally, you should be ready to run `python manage.py runserver` to run the application locally.

## Room for Improvement

The main pain point with the application now is the API retrieval time. I attempted to address this and saw some improvements by limiting the level of granularity of the latitude/longitude values and ordering the Django model IPLocation by latitude/longitude values. Looking into indexing the latitude/longitude values could be beneficial. Additionally, identifying how to best compress the API response, perhaps using Django's GzipMiddleware, should lead to a good performance boost as well. g