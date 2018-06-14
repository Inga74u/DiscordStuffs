import requests
import json

class OsuTracker:
    def __init__(self, Key):
        self.Key = Key
        
        self.TrackerList = {}
        self.NewTracked = {}
        self.OsuBase = "https://osu.ppy.sh/api/"
    
    def GetTracked(self):
        Tracked = self.NewTracked
        self.NewTracked = {}
        
        return Tracked
    
    def AddTrack(self, UserId, Mode):
        Headers = {"k": self.Key,
                   "u": UserId,
                   "m": Mode}
        
        Data = requests.get(OsuBase + "get_user", Headers)
        if Data.status_code == 200:
            Data = json.loads(Data.content.decode('utf-8'))
            
            Headers = {"k": self.Key,
                   "u": UserId,
                   "m": Mode,
                   "limit": 1}
            
            Name = Data[0]['username']
        
            Data = requests.get(self.OsuBase + "get_user_best", Headers)
            if Data.status_code == 200:
                Data = json.loads(Data.content.decode('utf-8'))
                
                MapData = Data[0]
                Score = MapData['score']
                MaxCombo = MapData['maxcombo']
                c300 = MapData['count300']
                c100 = MapData['count100']
                c50 = MapData['count50']
                cMiss = MapData['countmiss']
                Rank = MapData['rank']
                PP = MapData['pp']
                Perfect = MapData['perfect']
                
                DataTable = {'Name': Name,
                             'Score': Score,
                             'Combo': MaxCombo,
                             'c300': c300,
                             'c100': c100,
                             'c50': c50,
                             'cMiss': cMiss,
                             'Rank': Rank,
                             'PP': PP,
                             'Prefect': Perfect}
                
                try:
                    self.TrackerList[UserId]
                except:
                    self.TrackerList[UserId] = {}
                
                self.TrackerList[UserId][Mode] = DataTable
    
    def _TrackingLoop(self):
        while 1:
            for UserId in self.TrackerList:
                for Mode in self.TrackerList[UserId]:
                    Name = self.TrackerList[UserId][Mode]['Name']
                    
                    Headers = {"k": self.Key,
                               "u": UserId,
                               "m": Mode,
                               "limit": 1}
                    
                    Data = requests.get(self.OsuBase + "get_user_best", Headers)
                    if Data.status_code == 200:
                        Data = json.loads(Data.content.decode('utf-8'))
                        
                        MapData = Data[0]
                        Score = MapData['score']
                        MaxCombo = MapData['maxcombo']
                        c300 = MapData['count300']
                        c100 = MapData['count100']
                        c50 = MapData['count50']
                        cMiss = MapData['countmiss']
                        Rank = MapData['rank']
                        PP = MapData['pp']
                        Perfect = MapData['perfect']

                        DataTable = {'Name': Name,
                                     'Score': Score,
                                     'Combo': MaxCombo,
                                     'c300': c300,
                                     'c100': c100,
                                     'c50': c50,
                                     'cMiss': cMiss,
                                     'Rank': Rank,
                                     'PP': PP,
                                     'Prefect': Perfect}
                        
                        if DataTable != self.TrackerList[UserId][Mode]:
                            self.TrackerList[UserId][Mode] = DataTable
                            self.NewTracked[UserId] = {}
                            self.NewTracked[UserId][Mode] = DataTable
