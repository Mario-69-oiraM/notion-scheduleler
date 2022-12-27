import config
import requests

def updateheartbeat(log):
    try:
        updateData = '{ "parent": { "database_id": "6a6b13d5d7ae49daa0b8bb4a54e5af18" }, '
        updateData += ' "properties": { "Text": { "title": [ { "text": { "content": "' + log + '" } } ] } '
        updateData += '  } }'
        response = requests.post(config.NotionAPIPages , headers=config.NotionHeader_heartbeat, data=updateData)
        if response.status_code == 200: 
            return True
        else:
            return False
    except:  
        return False