##
# docker run -d -t --name notionscheduleler python
# git clone https://mario-69-mario@github.com/Mario-69-Mario/notion-scheduleler
# pip install requests

#/usr/config

#cd /usr/notion-scheduleler

#git config credential.helper cache

#git pull https://mario-69-mario@github.com/Mario-69-Mario/notion-scheduleler

# chmod 755 runSchedule
# export NOTION_TOKEN=
#0-59 * * * * /Users/jaai/anaconda3/bin/python3/python ~/PycharmProjects/dailySearch.py trees >> ~/woah.log 2>&1

cd /
mkdir temp-git
cd temp-git
git# git clone https://mario-69-mario@github.com/Mario-69-Mario/notion-scheduleler .
cd /temp-git
git pull
cd /app
cp /temp-git/*.py . 
python3 /app/notion-scheduleler.py
