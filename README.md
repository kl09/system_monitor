# System Monitoring

There are 2 services:
* `monitor_producer` for checking web urls statuses and pushing them to kafka.
* `monitor_consumer` for getting data from kafka and saving them in PostgreSQL.

### Lint and test

`make lint` - run linter

`make up` - start local services: kafka, psql, etc.

`make test` - run local tests, based on local services. Run after you launched local services with `make up`.


### Install

1. `sudo apt install libpq-dev python3-dev` - -install the prerequsisites for building the psycopg2 package.

2. `pip install -r requirements.txt` - install required modules.

3. Create `config/kafka.json` file. There is `config/kafka_example.json` an example.

4. Create `config/psql.json` file. There is `config/psql_example.json` an example.

5. Add ssl certs for kafka to `config/ssl/kafka`.

So, your config file should look like:
```
-config/
--ssl/
----ca.pem
----service.cert
----service.key
--kafka.json
--pgsql.json
```


### Running


Run `make start_producer` to run producer app.

Run `make start_consumer` to run consumer app.
