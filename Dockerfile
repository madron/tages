FROM ubuntu:20.04

# Packages
RUN     apt-get update \
    &&  DEBIAN_FRONTEND=noninteractive apt-get install -y gosu uwsgi-plugin-python3 python3-pip nginx python3-psycopg2 \
    &&  rm -rf /var/lib/apt/lists/* \
    \
    # forward request and error logs to docker log collector
    &&  ln -sf /dev/stdout /var/log/nginx/access.log \
    &&  ln -sf /dev/stderr /var/log/nginx/error.log


# Requirements
COPY requirements.txt /src/requirements.txt
RUN  pip3 install -r /src/requirements.txt

# Docker dir
COPY docker /docker/
COPY docker/nginx-base.conf /etc/nginx/nginx.conf

# Docker misc
ENTRYPOINT ["/docker/entrypoint.sh"]
CMD ["uwsgi", "--plugin", "/usr/lib/uwsgi/plugins/python38_plugin.so", "--master", "--processes", "1", "--threads", "8", "--chdir", "/src", "--module=settings.wsgi:application", "--http-socket", ":8000", "--stats", ":9191"]
WORKDIR /src/

ENV DJANGO_SETTINGS_MODULE=settings.prod

# Source
COPY manage.py /src/
COPY settings /src/settings
COPY tages /src/tages
RUN chmod 755 /src/manage.py

# Collect static files
RUN    rm -rf /src/docker \
    && python3 /src/manage.py collectstatic --link --noinput --verbosity=0
