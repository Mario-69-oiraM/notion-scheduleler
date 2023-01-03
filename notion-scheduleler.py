##
## scheduleler
##
##  export NOTION_TOKEN=
##  export NOTION_TOKEN_heartbeat=
# comment 

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
from helper import updateheartbeat ,SaveResult, logfile
import calendar

def ReadRepeatfromNotionAction():
    
    today = date.today()
    FromDate = date.today()
    weeknumber = (today.isocalendar()[1] + 1 )

    data = ' {"filter": { "or": [ '
    data +=  ' { "property": "Repeat", "select" : {"equals": "' + config.Weekly + '" } }, '
    data +=  ' { "property": "Repeat", "select" : {"equals": "' + config.Every_work_day + '" } }, '
    data +=  ' { "property": "Repeat", "select" : {"equals": "' + config.Monthly + '" } }, '
    data +=  ' { "property": "Repeat", "select" : {"equals": "' + config.Bi_weekly + '" } }'
    data +=  ' ] } } '

    response = requests.post(config.NotionAPIDatabases + config.actions_database_id + '/query', headers=config.NotionHeader(config.tokenActions), data=data)
    
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
                    
                if done == True and repeat == config.Monthly:
                    exitCtr = 0
                    go = False
                    days_in_month = (calendar.monthrange(dodate.year, dodate.month)[1]) + 1
                    expectedMonth = dodate.month + 1
                    
                    tempdoDate = dodate + datetime.timedelta(days=days_in_month)
                    daymovement = -1 
                    
                    while go == False:
                        tempdoDate = tempdoDate + datetime.timedelta(days=daymovement)
                        print(str(tempdoDate) + ' ' + str(tempdoDate.isoweekday()))

                        if tempdoDate.month > expectedMonth:
                            daymovement = -1                        
                        elif tempdoDate.month < expectedMonth:
                                daymovement = 1
                        if (tempdoDate.isoweekday() < 6) and (tempdoDate.month == expectedMonth):
                            go = True
                        if exitCtr > 15:
                            logfile('Error: Monthly date select fail' + title) 
                            go = True
                        exitCtr += 1
                            
                    UpdateAction(id, FromDate, tempdoDate, title, repeat)

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

        response = requests.request("PATCH", config.NotionAPIPages + id, headers=config.NotionHeader(config.tokenActions), data=updateData)

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
        
        response = requests.request("POST", config.NotionAPICommnets, headers=config.NotionHeader(config.tokenActions), data=updateComment)

        if response.status_code == 200:
            logfile(Comment)
            return True
        else:
            logfile("Error: " + response.text)
            return False
    except: 
        logfile("Error: UpdateAction" )
        return False
    

def main():
    try: 
        if (str(os.getenv(config.tokenActions)) != 'None') and (str(os.getenv(config.tokenHeartbeat)) != 'None'):
            updateheartbeat("Heartbeat - Action schedule")
            ReadRepeatfromNotionAction()
        else:
            logfile("Error: NOTION_TOKEN of NOTION_TOKEN_heartbeat missing! " )
    except Exception as e:
        logfile("Main error " + e  )
    
if __name__ == "__main__":
    main()
