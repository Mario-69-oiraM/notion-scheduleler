import config

import requests
import json
from datetime import datetime
from datetime import date
import datetime
import logging

level=logging.DEBUG

def SaveResult(Json_text):
    with open('.db2.json','w',encoding='utf8') as f:
            json.dump(Json_text,f,ensure_ascii=False)  
    return True


def logfile(log :str):
    try:
        ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(config.logfile, "a") as f: 
            f.writelines(log)
        return True 
    except ValueError as e:
        print(e)

def updateheartbeat(log):
    #try:
    updateData = '{ "parent": { "database_id": "6a6b13d5d7ae49daa0b8bb4a54e5af18" }, '
    updateData += ' "properties": { "Text": { "title": [ { "text": { "content": "' + log + '" } } ] } '
    updateData += '  } }'
    response = requests.post(config.NotionAPIPages , headers=config.NotionHeader(config.tokenHeartbeat), data=updateData)
    if response.status_code == 200: 
        return True
    else:
        return False
    #except:  
    #    return False