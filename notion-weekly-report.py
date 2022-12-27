##
## scheduleler
##
##  export NOTION_TOKEN=
##  export NOTION_TOKEN_heartbeat=

from json import decoder
import requests 
import re 
from datetime import datetime
from datetime import date
import os
import json
import configparser
import config
import string
import datetime
from helper import updateheartbeat

def SaveResult(Json_text):
    with open('.db2.json','w',encoding='utf8') as f:
            json.dump(Json_text,f,ensure_ascii=False)  
    return True

def logfile(log):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    f = open(config.logfile, "a")
    f.writelines(ts + ' | ' + log +'\n')
    f.close()
    return True 


def ReadRepeatfromNotionAction():
    
    today = date.today()
    FromDate = date.today()
    weeknumber = (today.isocalendar()[1] + 1 )

    data = ' {"filter": { "or": [ '
    data +=  ' { "property": "Repeat", "select" : {"equals": "' + config.Weekly + '" } }, '
    data +=  ' { "property": "Repeat", "select" : {"equals": "' + config.Every_work_day + '" } }, '
    data +=  ' { "property": "Repeat", "select" : {"equals": "' + config.Bi_weekly + '" } }'
    data +=  ' ] } } '

    response = requests.post(config.NotionAPIDatabases + config.actions_database_id + '/query', headers=config.NotionHeader, data=data)
    
    logfile('Notion Connection ' + str(response.status_code))
    logfile('##########################################################')

    if response.status_code == 200: 
        data_dict = json.loads(response.text)
        if bool(data_dict["results"]):
            for OneItem in data_dict["results"]:
                SaveResult(OneItem)
                id = OneItem["id"]
                title = OneItem["properties"]["Name"]["title"][0]["text"]["content"]
                repeat = OneItem["properties"]["Repeat"]["select"]["name"]
                done = OneItem["properties"]["Done"]["checkbox"]
                dodate = datetime.datetime.strptime(OneItem["properties"]["Do Date"]["date"]["start"],'%Y-%m-%d').date()
                FromDate = dodate
                weeknumber_doDate = dodate.isocalendar()[1] + 1
                
                if done == True and repeat == config.Weekly: #and weeknumber > weeknumber_doDate:
                    dodate = dodate + datetime.timedelta(days=7)
                    UpdateAction(id, FromDate, dodate, title, repeat)

                if done == True and repeat == config.Bi_weekly: # and (weeknumber - 1) > (weeknumber_doDate) 
                    dodate = dodate + datetime.timedelta(days=14)
                    UpdateAction(id, FromDate, dodate, title, repeat)

                elif done == True and repeat == config.Every_work_day: #and dodate < today 
                    dodate = dodate + datetime.timedelta(days=1)
                    while dodate.isoweekday() >= 6:
                        dodate = dodate + datetime.timedelta(days=1)
                    UpdateAction(id, FromDate, dodate, title, repeat)

                else:
                    logfile('do nothing :' + title) 
            #else:
            #    logfile("Empty record ")
            
    else:
        logfile("Error: " + str(response.status_code) + " | " + response.text)
        return False    
    return True

def UpdateAction(id, FromDate, Action_Date, title, repeat):
    Action_Date_str = Action_Date.strftime('%Y-%m-%d')
    try:
        updateData = ' { "properties":  '
        updateData += ' { '
        updateData += '     "Done": {'
        updateData += '            "checkbox": false '
        updateData += '              }, '
        updateData += '       "Do Date": { '
        updateData += '         "date": { '
        updateData += '                 "start": "' + Action_Date_str + '" '
        updateData += '                  } ' 
        updateData += '                } '
        updateData += ' } }'

        response = requests.request("PATCH", config.NotionAPIPages + id, headers=config.NotionHeader, data=updateData)

        if response.status_code != 200:
            logfile("Error: " + response.text )
            return False

        Comment = title + ' Updated -: repeat date [' + repeat + '] from:' + FromDate.strftime('%Y-%m-%d') + ' to:' + Action_Date.strftime('%Y-%m-%d') 

        updateComment = ' {"parent": { '
        updateComment += ' "page_id": "' + id + '" '
        updateComment += ' }, '
        updateComment += '  "rich_text": [ '
        updateComment += ' { '
        updateComment += ' "text": { '
        updateComment += ' "content": "' + Comment + '" '
        updateComment += ' } '
        updateComment += ' } '
        updateComment += ' ] }'
        
        response = requests.request("POST", config.NotionAPICommnets, headers=config.NotionHeader, data=updateComment)

        if response.status_code == 200:
            logfile(Comment)
            return True
        else:
            logfile("Error: " + response.text)
            return False
    except: 
        logfile("Error: UpdateAction" )
        return False
    
# def updateheartbeat(log):
#     try:
#         updateData = '{ "parent": { "database_id": "6a6b13d5d7ae49daa0b8bb4a54e5af18" }, '
#         updateData += ' "properties": { "Text": { "title": [ { "text": { "content": "' + log + '" } } ] } '
#         updateData += '  } }'
#         response = requests.post(config.NotionAPIPages , headers=config.NotionHeader_heartbeat, data=updateData)
#         if response.status_code == 200: 
#             return True
#         else:
#             return False
#     except:  
#         return False

def main():
    try: 
        if (str(os.getenv('NOTION_TOKEN')) != 'None') and (str(os.getenv('NOTION_TOKEN_heartbeat')) != 'None'):
            logfile("NOTION_TOKEN = not found" )
            updateheartbeat("Heartbeat - Action schedule")
            ReadRepeatfromNotionAction()
        else:
            logfile("Error: NOTION_TOKEN of NOTION_TOKEN_heartbeat missing! " )
    except Exception as e:
        logfile("Main error " + e  )
    
if __name__ == "__main__":
    main()
