import requests
import json
import config
from helper import SaveResult, logfile
import datetime

def IsNoteinRange(pageid, startDate, endDate):
    try:
        response = requests.get(config.NotionAPIPages + pageid, headers=config.NotionHeader(config.tokenActions))
        data_dict = json.loads(response.text)
        #dodate = datetime.datetime.strptime(OneItem["properties"]["Do Date"]["date"]["start"],'%Y-%m-%d').date()
        
        noteDate = data_dict["properties"]["Updated Date"]["formula"]["date"]["start"]

        #noteDate = datetime.datetime.strptime(noteDate,'%Y-%m-%d')
        noteDate_str = noteDate.strftime('%Y-%m-%d')

        print(noteDate_str)
        print(noteDate.strftime('%Y-%m-%d'))
        #startDate, endDate
        
        return data_dict
    except ValueError as e: 
        logfile("Error: " + e )
        return False


def GetDatabaseQuery(databaseId : str, filter : str, token=config.tokenActions):
    try:
   
        response = requests.post(config.NotionAPIDatabases + databaseId + '/query', headers=config.NotionHeader(config.tokenActions), data=filter)
        
        data_dict = json.loads(response.text)
        SaveResult(data_dict["results"])
        return data_dict["results"]
    except: 
        logfile("Error: UpdateAction" )
        return False

def UpdatePageTitle(id, StartDate, EndDate ):
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
        
    except: 
        logfile("Error: UpdateAction" )
        return False
    

def AppendLinktoPage(id, page_id):
    try:
        
        updateData =  ' { "children": [  ' 
        updateData += ' { "object": "block", '
        updateData += ' "type": "link_to_page", '
        updateData += ' "link_to_page": { '
        updateData += ' "type": "page_id",' 
        updateData += ' "page_id": "{0}"'.format(page_id) 
        updateData += ' } } ] }'

        SaveResult(updateData)
        response = requests.request("PATCH",config.NotionAPIBlocks.format(id), headers=config.NotionHeader(config.tokenActions), data=updateData)
        
        data_dict = json.loads(response.text)
        SaveResult(data_dict)
    except: 
        logfile("Error: UpdateAction" )
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


    