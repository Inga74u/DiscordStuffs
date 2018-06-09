import google.oauth2.credentials
import google_auth_oauthlib.flow

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

YoutubeData = {
    "DevKey": "AIzaSyARrlze9cAf1RsLw46ATn9orIGEQB4s6VE",
    "API_Service_Name": "youtube",
    "API_Version":  "v3"
    }

def serv(Data):
    return build(Data["API_Service_Name"], Data["API_Version"], developerKey = Data["DevKey"])

client = serv(YoutubeData)

def search_list(query, mResults = 1):
    vList = _search_list(client,
                         part = 'snippet',
                         maxResults = mResults,
                         q = query,
                         type = "video")
    
    return vList

def _search_list(client, **kwargs):
    response = client.search().list(**kwargs).execute()
    
    items = []
    for x in response['items']:
        Id = x["id"]["videoId"]
        Title = x["snippet"]["title"]
        ChanId = x["snippet"]["channelId"]
        ChanTitle = x["snippet"]["channelTitle"]
        Thumb = x["snippet"]["thumbnails"]["default"]["url"]
        
        items.append({"id": Id,
                      "title": Title,
                      "chanid": ChanId,
                      "chantitle": ChanTitle,
                      "thumbnail": Thumb})
    
    return items

