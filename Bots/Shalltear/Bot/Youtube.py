import google.oauth2.credentials
import google_auth_oauthlib.flow

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

YoutubeData = {
    "DevKey": "AIzaSyARrlze9cAf1RsLw46ATn9orIGEQB4s6VE",
    "API_Service_Name": "youtube",
    "API_Version":  "v3"
    }

def _is_private(Title, Desc):
    if Title == "Private video":
        if Desc == "This video is private.":
            return True
    return False

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
        Title = x["snippet"]["title"]
        Desc = x["snippet"]["description"]

        if not _is_private(Title, Desc):
            Id = x["id"]["videoId"]
            ChanId = x["snippet"]["channelId"]
            ChanTitle = x["snippet"]["channelTitle"]
            Thumb = x["snippet"]["thumbnails"]["default"]["url"]
            
            items.append({"id": Id,
                          "title": Title,
                          "chanid": ChanId,
                          "chantitle": ChanTitle,
                          "thumbnail": Thumb,
                          "playlist": None})
    
    return items

def search_playlist(query, mResults = 1):
    pList = _search_playlist(client,
                             part = 'snippet',
                             maxResults = mResults,
                             q = query,
                             type = "playlist")

    return pList


def _search_playlist(client, **kwargs):
    response = client.search().list(**kwargs).execute()
    
    items = []
    for x in response['items']:
        Id = x["id"]["playlistId"]
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

def get_playlist_items(Id):
    items = _get_playlist_items(client,
                                part = 'snippet',
                                maxResults = 50,
                                playlistId = Id)

    return items

def _get_playlist_items(client, **kwargs):
    response = client.playlistItems().list(**kwargs).execute()

    items = []
    for x in response['items']:
        Title = x["snippet"]["title"]
        Desc = x["snippet"]["description"]

        if not _is_private(Title, Desc):
            Id = x["snippet"]["resourceId"]["videoId"]
            ChanId = x["snippet"]["channelId"]
            ChanTitle = x["snippet"]["channelTitle"]
            Thumb = x["snippet"]["thumbnails"]["default"]["url"]

            items.append({"id": Id,
                          "title": Title,
                          "chanid": ChanId,
                          "chantitle": ChanTitle,
                          "thumbnail": Thumb,
                          "playlist": kwargs['playlistId']})

    try:
        nextPageToken = response["nextPageToken"]
    except:
        nextPageToken = None

    while nextPageToken != None:
        response = client.playlistItems().list(**kwargs, pageToken = nextPageToken).execute()

        for x in response['items']:
            Id = x["snippet"]["resourceId"]["videoId"]
            Title = x["snippet"]["title"]
            ChanId = x["snippet"]["channelId"]
            ChanTitle = x["snippet"]["channelTitle"]
            Thumb = x["snippet"]["thumbnails"]["default"]["url"]

            items.append({"id": Id,
                          "title": Title,
                          "chanid": ChanId,
                          "chantitle": ChanTitle,
                          "thumbnail": Thumb})

        try:
            nextPageToken = response["nextPageToken"]
        except:
            nextPageToken = None

    return items
        
