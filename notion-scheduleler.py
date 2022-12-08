##
## scheduleler
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


def ReadRepeatfromNotionAction(Repeat):
    
    today = date.today()
    weeknumber = (today.isocalendar()[1] + 1 )
    
    print(today)
    print(weeknumber)

    #data +=  ' "title" , "rich_text": {"contains": "' + Action_title + '" '

    data = ' {"filter": { "property": '
    data +=  ' "Repeat", "select" : {"equals": "' + Repeat + '" '
    data +=  ' } } } ' 

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
                weeknumber_doDate = dodate.isocalendar()[1] + 1
                
                if done == True and weeknumber > weeknumber_doDate and repeat == "Weekly":
                    print('Update done flag and update do date to + 7 days :' + title)
                    dodate = dodate + datetime.timedelta(days=7)
                    UpdateAction(id, dodate, title)
                else:
                    print('do nothing :' + title) 
            else:
                print("Add new record")
                return True
    else:
        print("Error: " + response.status_code + " | " + response.text)
        return False
    return False 

def UpdateAction(id, Action_Date, title):
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

        if response.status_code == 200:
            print("updated :" + title + id )
        else:
            print ("Error: " + response.text )
            return False
        Comment = "Updated Do Date = " + Action_Date_str + " Done = False "

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
            print("updated :" + title + id )
            return True
        else:
            print ("Error: " + response.text )
            return False


    except:  
        return False
        
def actions():
    with open('Actions.txt') as f:
        string = f.readlines()
        return string
    return False

def main():
    if str(os.getenv('NOTION_TOKEN')) != 'None':
        print("NOTION_TOKEN = " + str(os.getenv('NOTION_TOKEN')))
        #ReadRepeatfromNotionAction('Daily')

        ReadRepeatfromNotionAction(Weekly)
    else:
        print("Error: NOTION_TOKEN missing " )
    
    #for ln in actions():
    #    ReadfromNotionAction(ln.replace('\n',''))



if __name__ == "__main__":
    main()
