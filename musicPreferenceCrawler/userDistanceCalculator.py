import pymongo
            
#tanimoto diatance
def tanimoto(user1, user2):
    user1HobbyList = user1['hobbyList']
    user2HobbyList = user2['hobbyList']
    if len(user1HobbyList) == 0 or len(user2HobbyList) == 0:
        return 1.0
    orCount = len(user1HobbyList) + len(user2HobbyList)
    andCount = 0
    for item in user1HobbyList:
        if item in user2HobbyList:
            andCount += 1 
    return 1.0 - (float(andCount) / (orCount - andCount))

def absolutelyCommonCount(user1, user2):
    user1HobbyList = user1['hobbyList']
    user2HobbyList = user2['hobbyList']
    if len(user1HobbyList) == 0 or len(user2HobbyList) == 0:
        return 1.0
    andCount = 0
    for item in user1HobbyList:
        if item in user2HobbyList:
            andCount += 1 
    return float (1.0) / (andCount + 1.0)

class calculator:
    def __init__(self):
        self.mongodbInit()
        
    def mongodbInit(self):
        self.client = pymongo.MongoClient("localhost", 27017)
        
    def getMusicPreferenceDb(self):
        db = self.client.musicpreference
        return db.musicpreference
    
    def getDistanceDb(self):
        db = self.client.musicDistance
        return db.musicDistance
        
    def loadAllUserPreferences(self, distance = absolutelyCommonCount):
        cursor1 = self.getMusicPreferenceDb().find()
        res = [{'userId': item['userId'], 'distanceList': []} for item in cursor1]
        cursor = self.getMusicPreferenceDb().find()
        i = 0
        while i <= 4010:
            j = i + 1
            while j <= 4010:
                d = distance(cursor[i], cursor[j])
                distanceBetweenIAndOthers = res[i]['distanceList']
                withJ = {"userId": cursor[j]['userId'], "distance": d}
                distanceBetweenIAndOthers.append(withJ)
                    
                distanceBetweenJAndOthers = res[j]['distanceList']
                withI = {"userId": cursor[i]['userId'], "distance": d}
                distanceBetweenJAndOthers.append(withI)
                
                j += 1
            
            print res[i]
            
            nearest = 1.0
            nearestUser = ''
            for item in res[i]['distanceList']:
                if item['distance'] < nearest:
                    nearest = item['distance']
                    nearestUser = item['userId']
            print nearestUser + ' ' + str(nearest)
            print res[i]['userId'] + ' over'
            i += 1
                
        for item in res.items():
            self.getDistanceDb().insert_one(item)

def main():
    calc = calculator()
    calc.loadAllUserPreferences()
#     calc.test()
    

if __name__ == '__main__':
    main()