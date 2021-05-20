
# Set the base image
FROM ubuntu:20.04

# File Author / Maintainer
LABEL maintainer="francisco.pulice@outlook.com"

ENV TZ=America/Panama
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

WORKDIR /home/transformers

RUN apt-get update && apt-get upgrade -y && apt-get install -y apache2 \
        software-properties-common \ 
        python3-pip

RUN pip install transformers[torch]
RUN pip install --upgrade tensorflow
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

RUN apt-get install libapache2-mod-wsgi-py3 -y 

# Copy over the apache configuration file and enable the site
COPY 000-default.conf /etc/apache2/sites-available/000-default.conf

RUN chmod -R 777 /var/www/ && chmod -R 777 /tmp && 
# Copy files
COPY . /home/transformers

ENV NLTK_DATA /nltk_data/
ADD . $NLTK_DATA

EXPOSE 80


CMD  /usr/sbin/apache2ctl -D FOREGROUND

