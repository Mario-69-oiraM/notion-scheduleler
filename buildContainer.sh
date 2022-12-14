echo "# Auto build from buildContainer script"  > crontab
echo NOTION_TOKEN=$NOTION_TOKEN >> crontab
echo PYTHONPATH=/app/appRequirements >> crontab
echo " " >> crontab
echo "# Run automation every min" >> crontab
echo "* * * * * bash /app/runSchedule.sh >> /var/log/myjob.log 2>&1" >> crontab


docker build -t my-python --build-arg NOTION_TOKEN=$NOTION_TOKEN .
