import google.oauth2.credentials
import google_auth_oauthlib.flow

from googleapiclient.descovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

CLIENT_SECRETS_FILE = ".\\Bot\\client_secret.json"

SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

client = serv()

def serv():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_console()
    return build(API_SERVICE_NAME, API_VERSION) #, credentials = credentials)

def search_list(query, mResults = 1):
    vList = _search_list(client,
                         part = 'snippet',
                         maxResults = mResults,
                         q = query,
                         type = "video")
    
    return vList

def _search_list(**kwargs):
    response = client.search().list(**kwargs).execute()
    
    items = []
    for x in response['items']:
        Id = x["id"]["videoId"]
        Title = x["snippet"]["title"]
        ChanId = x["snippet"]["channelId"]
        ChanTitle = x["snippet"]["channelTitle"]
        Thumb = x["snippet"]["thumbnails"]["default"]["url"]
    
    return items

