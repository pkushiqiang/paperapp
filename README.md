Start up the service
--------------------

1.  unzip the file, run below to start the containers

    docker-compose up --build

2.  There will be three containers to be created:

    1.  paper_web: the  Flask-restful app

    2.  paper_db: PostgreSQL server

    3.  paper_cache: Redis server

3.  If it is the first time to run the service, it will backfill the data
    automatically. You can see it will download the csv files, and backfill to
    the database.

You will keep seeing messages like this: "Meet csv format error in line:  119”,
which means the program meets CSV format error in papers.csv. The backfill process
will take about 1 minutes.

1.  You can see message like "Running on http://0.0.0.0:5000/ (Press CTRL+C to
    quit)”, which means the service app is ready.

Access the Service
------------------

1.  <http://127.0.0.1:5000/>  - If it should shows

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
{
    "status": "Good"
}
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1.  <http://127.0.0.1:5000/authors> - List all the authors

2.  <http://127.0.0.1:5000/authorinfo/<author id>> - get author info, and all
    his papers. e.g.<http://127.0.0.1:5000/authorinfo/1727782>

 

 

 

 
