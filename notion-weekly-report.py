##
## scheduleler
##
##  export NOTION_TOKEN=
##  export NOTION_TOKEN_heartbeat=
##  export NOTION_TOKEN_reports= 

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


def ReadActions():
    #read report table 
    # Start Date
    # End Date
    # Ready

    data = ' {"filter": { "or": [ '
    data +=  ' { "property": "Ready", "checkbox" : {"equals": false } } '
    data +=  ' ] } } '
    #SaveResult(data)
    response = requests.post(config.NotionAPIDatabases + config.reports_database_id + '/query', headers=config.NotionHeader(config.tokenActions), data=data)
    
    if response.status_code == 200: 
        data_dict = json.loads(response.text)
        if bool(data_dict["results"]):
            #SaveResult(data_dict)
            for ReportItem in data_dict["results"]:
                SaveResult(ReportItem)
                ReportItem_id = ReportItem["id"]
                startDate = ReportItem["properties"]["Start Date"]["date"]["start"]
                endDate = ReportItem["properties"]["End Date"]["date"]["start"]
                #GetPage(ReportItem_id)
                data = ' {"filter": { "and": [ '
                data +=  ' { "property": "Do Date", "date" : {"on_or_after": "' + startDate + '" } }, '
                data +=  ' { "property": "Do Date", "date" : {"on_or_before": "' + endDate + '" } } '
                data +=  ' ] } } '
                #SaveResult(data)
                # people - 939aa24f98a5445cb4dfd8c49e8264b2
                ActionResponse = requests.post(config.NotionAPIDatabases + config.actions_database_id + '/query', headers=config.NotionHeader(config.tokenActions), data=data)
                if ActionResponse.status_code == 200: 
                    Action_data_dict = json.loads(ActionResponse.text)
                    #SaveResult(Action_data_dict)
                    for Action_Item in Action_data_dict["results"]:                        
                        People = []
                        #SaveResult(OneItem["properties"]["People"]["relation"])
                        Action_Item_pageURL = Action_Item["url"]
                        Action_Item_ID = Action_Item["id"]
                        for Person in Action_Item["properties"]["People"]["relation"]:
                            People.append(Person)
                            #response = requests.request("GET", config.NotionAPIPages + Person, headers=config.NotionHeader(config.tokenActions))
                        
                        UpdateReport(ReportItem_id, startDate ,endDate, Action_Item_pageURL,Action_Item_ID)

                else:
                    SaveResult(ActionResponse.text)
    else:
        SaveResult(response.text)

        
    return True

def GetPage(pageid):
    
    response = requests.request("GET", config.NotionAPIPages + pageid, headers=config.NotionHeader(config.tokenActions))
    data_dict = json.loads(response.text)
    SaveResult(data_dict)

def UpdateReport(id, StartDate, EndDate, Action_Item_pageURL, Action_Item_ID):
    Title = 'Activity from ' + StartDate + ' to ' + EndDate
    try:
        updateData = ' { "properties":  '
        updateData += ' { '
        updateData += '     "Name": {'
        updateData += '            "title": [ { "text": { "content": "' + Title + '"} }  ]'
        updateData += '              } '
        updateData += ' } }'
        
        response = requests.request("PATCH", config.NotionAPIPages + id, headers=config.NotionHeader(config.tokenActions), data=updateData)

        if response.status_code != 200:
            logfile("Error: " + response.text )
            return False
        
        # updateData =  ' { "children": [ ' 
        # updateData += ' { "object": "block", '
        # updateData += '   "type": "paragraph", "paragraph": { '
        # updateData += '   "rich_text": [ { "type": "text", '
        # updateData += '   "text": { "content": "' + Action_Item_pageURL + '", "link": null  } '
        # updateData += '   } ] } } ] }'
        
        # updateData =  ' { "children": [ ' 
        # updateData += ' { "object": "block", '
        # updateData += '   "type": "embed", '
        # updateData += '   "embed": { "url": "' + bodyData + '" } '
        # updateData += '    } ] } '

        # updateData =  ' { "children": [ ' 
        # updateData += ' { "object": "block", '
        # updateData += '   "type": "bookmark", '
        # updateData += '   "bookmark": { "url": "' + Action_Item_pageURL + '" } '
        # updateData += '    } ] } '

        # updateData =  ' { "children": [ { ' 
        # updateData += ' "type": "link_to_page", '
        # updateData += ' "link_to_page": { '
        # updateData += ' "type": "page_id",' 
        # updateData += ' "page_id": "{0}"'.format(Action_Item_ID) 
        # updateData += ' } } ] }'

        updateData =  ' { "children": [  ' 
        updateData += ' { "object": "block", '
        updateData += ' "type": "link_to_page", '
        updateData += ' "link_to_page": { '
        updateData += ' "type": "page_id",' 
        updateData += ' "page_id": "{0}"'.format(Action_Item_ID) 
        updateData += ' } } ] }'

        SaveResult(updateData)
        response = requests.request("PATCH",config.NotionAPIBlocks.format(id), headers=config.NotionHeader(config.tokenActions), data=updateData)
        
        data_dict = json.loads(response.text)
        SaveResult(data_dict)

    except: 
        logfile("Error: UpdateAction" )
        return False
    
def main():
    try: 
        if (str(os.getenv(config.tokenActions)) != 'None') and (str(os.getenv(config.tokenHeartbeat)) != 'None'):
            #updateheartbeat("Heartbeat - Reports schedule")
            ReadActions()
            #ReadRepeatfromNotionAction()
        else:
            logfile("Error: NOTION_TOKEN missing! " )
    except Exception as e:
        logfile("Main error " + e  )
    
if __name__ == "__main__":
    main()
