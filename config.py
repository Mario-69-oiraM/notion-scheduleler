import os

#config stuff 
Weekly = 'Weekly'
Every_work_day = 'Every work day'
Bi_weekly = "Bi-weekly"

logfile = 'schedulelerlog.txt'

    
NotionHeader = {}

NotionHeader = { 'Authorization': 'Bearer ' + str(os.getenv('NOTION_TOKEN')) ,
                'Content-Type': 'application/json',
                'Notion-Version': '2022-06-28'
                }
                
NotionHeader_heartbeat = { 'Authorization': 'Bearer ' + str(os.getenv('NOTION_TOKEN_heartbeat')) ,
                'Content-Type': 'application/json',
                'Notion-Version': '2022-06-28'
                }


actions_database_id = "cbf1a5a1dae148dbabac74a98f5534c0"
heartbeat_database_id = "6a6b13d5d7ae49daa0b8bb4a54e5af18"
NotionAPIDatabases =  'https://api.notion.com/v1/databases/'
NotionAPIPages = 'https://api.notion.com/v1/pages/'
NotionAPICommnets = 'https://api.notion.com/v1/comments/'

# end config stuff 