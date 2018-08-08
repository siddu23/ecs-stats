FROM 370531249777.dkr.ecr.ap-south-1.amazonaws.com/ubuntu-nginx-sql:2.0.0

# set timezone
RUN rm /etc/localtime
RUN ln -s /usr/share/zoneinfo/Asia/Kolkata /etc/localtime
RUN export TZ=Asia/Kolkata

# service base
RUN mkdir -p /service

# copy code
COPY __init__.py wsgi.py gunicorn_conf.py app.py router.py /service/
COPY requirements.txt /service

RUN mkdir -p /service/src
RUN mkdir -p /service/conf

COPY src/* /service/src/
COPY conf/* /service/conf/

#setup nginx
RUN rm /etc/nginx/sites-available/default
COPY prerequisite/nginx.conf /etc/nginx/
RUN service nginx restart

COPY prerequisite/service.nginx /etc/nginx/sites-available/service
RUN ln -s /etc/nginx/sites-available/service /etc/nginx/sites-enabled/

#setup init script
COPY prerequisite/init.sh /service/

#set work dir
WORKDIR /service

#install dependencies
RUN pip install -q -r requirements.txt

#container port expose
EXPOSE 80

CMD ["/bin/bash", "init.sh"]
