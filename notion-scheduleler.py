##
## scheduleler
##
##  export NOTION_TOKEN=

from json import decoder
import requests 
import re 
from datetime import datetime
from datetime import date
import os
import json
import configparser
import string
import datetime

#config stuff 
Weekly = 'Weekly'
Every_work_day = 'Every work day'
Bi_weekly = "Bi-weekly"

NotionHeader = {}

NotionHeader = { 'Authorization': 'Bearer ' + str(os.getenv('NOTION_TOKEN')) ,
                'Content-Type': 'application/json',
                'Notion-Version': '2022-06-28'
                }

actions_database_id = "cbf1a5a1dae148dbabac74a98f5534c0"
NotionAPIDatabases =  'https://api.notion.com/v1/databases/'
NotionAPIPages = 'https://api.notion.com/v1/pages/'
NotionAPICommnets = 'https://api.notion.com/v1/comments/'

# end config stuff 

def SaveResult(Json_text):
    with open('.db2.json','w',encoding='utf8') as f:
            json.dump(Json_text,f,ensure_ascii=False)  


def ReadRepeatfromNotionAction():
    
    today = date.today()
    FromDate = date.today()
    weeknumber = (today.isocalendar()[1] + 1 )

    log = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '\n'
    
    print(today)
    print(weeknumber)

    #data +=  ' "title" , "rich_text": {"contains": "' + Action_title + '" '

    data = ' {"filter": { "or": [ '
    data +=  ' { "property": "Repeat", "select" : {"equals": "' + Weekly + '" } }, '
    data +=  ' { "property": "Repeat", "select" : {"equals": "' + Every_work_day + '" } }, '
    data +=  ' { "property": "Repeat", "select" : {"equals": "' + Bi_weekly + '" } }'
    data +=  ' ] } } '

    response = requests.post(NotionAPIDatabases + actions_database_id + '/query', headers=NotionHeader, data=data)
    
    print(response.status_code)
    if response.status_code == 200: 
        data_dict = json.loads(response.text)
        if bool(data_dict["results"]):
            #print(data_dict["results"][0]["properties"])
            #SaveResult(data_dict["results"])
            for OneItem in data_dict["results"]:
                SaveResult(OneItem)
                id = OneItem["id"]
                title = OneItem["properties"]["Name"]["title"][0]["text"]["content"]
                repeat = OneItem["properties"]["Repeat"]["select"]["name"]
                done = OneItem["properties"]["Done"]["checkbox"]
                dodate = datetime.datetime.strptime(OneItem["properties"]["Do Date"]["date"]["start"],'%Y-%m-%d').date()
                FromDate = dodate
                weeknumber_doDate = dodate.isocalendar()[1] + 1
                
                if done == True and repeat == Weekly: #and weeknumber > weeknumber_doDate:
                    dodate = dodate + datetime.timedelta(days=7)
                    UpdateAction(id, FromDate, dodate, title)

                if done == True and repeat == Bi_weekly: # and (weeknumber - 1) > (weeknumber_doDate) 
                    dodate = dodate + datetime.timedelta(days=14)
                    UpdateAction(id, FromDate, dodate, title)

                elif done == True and repeat == Every_work_day: #and dodate < today 
                    dodate = dodate + datetime.timedelta(days=1)
                    while dodate.isoweekday() >= 6:
                        dodate = dodate + datetime.timedelta(days=1)
                    UpdateAction(id, FromDate, dodate, title)
                    log += 'Update ' + Every_work_day + ' > ' + title

                else:
                    log += 'do nothing :' + title
                    print('do nothing :' + title) 
            else:
                print("Empty record " + str(datetime.datetime.now()))
            
    else:
        print("Error: " + str(response.status_code) + " | " + response.text)
        return False
    updatelog(log)    
    return True

def UpdateAction(id, FromDate, Action_Date, title):
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

        response = requests.request("PATCH", NotionAPIPages + id, headers=NotionHeader, data=updateData)

        if response.status_code != 200:
            print ("Error: " + response.text )
            return False

        Comment = 'Updated ' + title + ' repeat date ' + FromDate.strftime('%Y-%m-%d') + ' to ' + Action_Date.strftime('%Y-%m-%d') 

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
        
        response = requests.request("POST", NotionAPICommnets, headers=NotionHeader, data=updateComment)

        if response.status_code == 200:
            print(Comment)
            log += Comment + '/n'
            return True
        else:
            log += "Error: " + response.text
            print ("Error: " + response.text )
            return False


    except:  
        return False
    
def updatelog(log):
    try:
        updateData = ' { "properties":  '
        updateData += ' { '
        updateData += '     "Done": {'
        updateData += '            "checkbox": false '
        updateData += '              }, '
        updateData += '       "Do Date": { '
        updateData += '         "date": { '
        #updateData += '                 "start": "' + Action_Date_str + '" '
        updateData += '                  } ' 
        updateData += '                } '
        updateData += ' } }'

        #response = requests.request("PATCH", NotionAPIPages + id, headers=NotionHeader, data=updateData)
    
        return True
    except:  
        return False
        
def actions():
    with open('Actions.txt') as f:
        string = f.readlines()
        return string
    return False

def main():
    if str(os.getenv('NOTION_TOKEN')) != 'None':
        print("NOTION_TOKEN = found " )

        ReadRepeatfromNotionAction()
    else:
        print("Error: NOTION_TOKEN missing " )

if __name__ == "__main__":
    main()
