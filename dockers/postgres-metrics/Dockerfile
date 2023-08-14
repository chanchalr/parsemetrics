FROM postgres:latest

#RUN apk update && apk upgrade

ADD ./docker-entrypoint-initdb.d /docker-entrypoint-initdb.d
ADD custom_pg_hba.conf /
RUN mkdir -p /app/logs/postgres
RUN chmod a+rw /app/logs/postgres
ENV POSTGRES_PASSWORD=m3tr1cs
ENV POSTGRES_USER=postgres
ENV SDL_POSTGRES_PASSWORD=p@ssw0rd
CMD ["postgres", "-c" , "logging_collector=on", "-c", "log_directory=/app/logs/postgres", "-c", "hba_file=/custom_pg_hba.conf","-c", "max_connections=1000"]
