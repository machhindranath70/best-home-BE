# best-home-BE
this is the backend repo for best home

In the conda vertual enverment --> 

        conda create -n geodjango_env python=3.11 gdal geos proj psycopg2 -c conda-forge
        conda activate geodjango_env
        pip install -r requirements.txt

API call
http://127.0.0.1:8000/api/property-info-nearby/?lat=17.435163253265348&lon=78.39314127554101&radius=3000 
