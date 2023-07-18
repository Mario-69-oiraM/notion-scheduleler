FROM python:3.8

# set the working directory
WORKDIR /app

RUN apt-get update && apt-get -y install pip
RUN sudo apt-get install ffmpeg


# install dependencies
COPY requirements.txt /app
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r requirements.txt --target=/app/appRequirements
ENV PYTHONPATH=/app/appRequirements

RUN apt-get update && apt-get -y install cron
#RUN apt-get update && apt-get -y install nano

#RUN crontab -l | { cat; echo "*/1 * * * * bash /app/runSchedule"; } | crontab -

# copy the scripts to the folder
COPY . /app

ENV TZ=America/Los_Angeles
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ARG NOTION_TOKEN
ENV NOTION_TOKEN ${NOTION_TOKEN}
ENV NOTION_TOKEN_heartbeat ${NOTION_TOKEN_heartbeat}

# Give execution rights on the cron scripts
RUN chmod +x /app/runSchedule.sh

# Adding crontab to the appropiate location
ADD crontab /etc/cron.d/my-cron-file

# Giving executable permission to crontab file
RUN chmod 0644 /etc/cron.d/my-cron-file

# Running crontab
RUN crontab /etc/cron.d/my-cron-file

# Creating entry point for cron 
ENTRYPOINT ["cron", "-f"]
