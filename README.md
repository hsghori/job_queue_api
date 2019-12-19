# HTTP Job queue API

This package provides an API for a url "get data" service. The user can use the API to post a "job" with a URL from which
to fetch data. The jobs are placed in a redis queue and executed in queue order. Once the job is completed, the resulting 
data is stored in the DB.

Usage:
- `POST {host}/api/job/` with data `{'url': <url>}` creates a job using the provided url. 
	- Two jobs with the same URL cannot be requested within an hour of each other - the second job will result in a 400
	  response.
- `GET {host}/api/job/<pk>/` returns the data about an individual job.
- `GET {host}/api/job/` returns a list of jobs. The optional query parameters are:
	- `latest=True` returns the latest job.
	- `status=[Q|C|P|F]` filters by status (Q=queued, C=completed, P=processing, F=failed)
	- `url=[url]` filters by the job's url

Note:
- `examples/client.py` gives a sample of how to use the API. 
- When running locally using docker, the host is `http://0.0.0.0:8000/`

## Launching the service

In the project root
1. Run `make build`
2. Run `make start`

This will build the docker images and launch the containers. If you have not run the initial database migrations you will 
need to run them by following the steps below.

In a separate terminal
1. Run `make shell`
2. Run `make`

The service should now be up and ready to accept API calls.

## Relevant files

- `queue_service/settings.py`: Configuration settings for the Django server
- `api/models.py`: Database models
- `api/views.py`: API code

## Work to be done

- More comprehensive unit tests
- UI client to create, and search for jobs
- Move docker logs to a file instead of stdout 
