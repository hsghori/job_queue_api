FROM python:3.7

# set up environment
ENV PYTHONUNBUFFERED 1

# set up python environment
RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# copy files over
COPY manage.py /app/
COPY pytest.ini /app/
COPY api /app/
COPY queue_service /app/
