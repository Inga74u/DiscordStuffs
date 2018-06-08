from googleapiclient.descovery import build
from google_auth_oauthlib.flow import InstalledAppFlow


def search_list(query, mResults = 1, t = "video"):
    vList = _search_list(client,
                         part = 'snippet',
                         maxResults = mResults,
                         q = query,
                         type = t)
    
    return vList

def _search_list(**kwargs):
    response = client.search().list(**kwargs).execute()
    
    
