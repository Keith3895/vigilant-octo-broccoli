FROM tiangolo/meinheld-gunicorn-flask:latest
RUN mkdir -p /app/identity_server
COPY ./identity_server /app/identity_server
COPY ./requirements.txt /app
RUN pip install -r requirements.txt