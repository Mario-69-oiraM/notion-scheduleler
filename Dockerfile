FROM python:3.8

# set the working directory
WORKDIR /app

# install dependencies
COPY ./requirements.txt /app
RUN pip install --no-cache-dir --upgrade -r requirements.txt

RUN apt-get update && apt-get -y install cron
RUN apt-get update && apt-get -y install nano

RUN crontab -l | { cat; echo "*/1 * * * * bash /app/runSchedule"; } | crontab -

# copy the scripts to the folder
COPY . /app
# Give execution rights on the cron scripts
RUN chmod 755 /app/runSchedule
#RUN chmod 0644 /app/runSchedule

# start the server
ARG NOTION_TOKEN
ENV NOTION_TOKEN ${NOTION_TOKEN}

#CMD cron
