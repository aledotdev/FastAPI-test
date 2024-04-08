# Ale.dev Annotations:

I chose the FastAPI framework for this project because it is meant to be a simple service with a specific purpose (syncing providers' event data and making it available to be queried via a REST endpoint). If the project's scope needs to be expanded to include additional functionalities such as user authentication and a backoffice, I would recommend using another framework like Django, which offers better support for larger projects.

I opted for an RDBMS for storage and SQLAlchemy as the ORM because they are recommended by FastAPI and work perfectly for queries. If we need to sync data from multiple providers, where the event data differs from each one and requires handling dynamic data, we could consider implementing a NoSQL storage solution like MongoDB.

I have worked with asyncio functions, but I understand they can complicate integration with other distributed/async message processing systems like Celery, Airflow, etc. However, for the current scope, they work well. In case the project grows significantly and needs to handle many sync providers at the same time, this sync script will face challenges, and we will need to implement a more appropriate tool for that task.


The API can scale horizontally, and the database can also scale by adding more replicas for searching. If we need to improve response time, we can implement some caching strategies.

One strategy could be to cache every EventResponse item and only fetch event_ids from the database. With this caching strategy, we can reduce the I/O with the database and the CPU usage required to create SQLAlchemy model objects and Pydantic schemas.

Another strategy depends on the usage patterns we observe. For example, if our most frequent queries are for 'Tomorrow's events' and 'Next week's events,' we could cache the entire response. This approach could significantly reduce the workload on the database and API workers.

All caching strategies depend on the frequency of sync updates and the difficulty of refreshing/expiring cache data. We need to balance performance between reads and writes.


Regarding code quality, I've implemented a pre-commit check to analyze adherence to certain code standards. I use:
- Black for code style (PEP8)
- Isort for import styles
- Pylint for Python linting

It also checks other file formats such as JSON, .env, or .toml files, and alerts about/cleans up debug statements or private keys.
I recommend integrating these checks into the CI/CD tool. Additionally, we should include a tool to scan code and libraries for security issues, for example, https://snyk.io.


## How to run the project

```
git clone it clone git@github.com:aledotdev/aiocometd.git
cd alejandro.devalis

# create python virtual env
python -m venv .env
pip install poetry
source .env/bin/active

# install project deps and run tests
make test

# Create db and add a provider (it drops all previous data)
make init_test_db

# run Sync events service (keeps running and refresh each 60s by default)
make sync_events

# run app in dev mode
make run

```

## Access to api doc:
http://127.0.0.1:8000/docs/

## Search Event API URL
http://127.0.0.1:8000/search/?starts_at=2021-06-30&ends_at=2021-07-31T23:59


We can override any setting with a custom .env file. It should be name `.env-local` and should be located on the project root.

Due SQLite does not support Timezones for datetimes some tests are skipped to avoid failing. We can use a Postgres DB overwriting the setting `DB_URL`
```
example:
DB_URL="postgresql+asyncpg://event_provider:event_provider@localhost:5432/event_provider"
```
