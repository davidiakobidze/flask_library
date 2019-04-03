FROM postgres:10.5

EXPOSE 5432:5432

COPY ./flask_library_app/docker/data.sql /docker-entrypoint-initdb.d/