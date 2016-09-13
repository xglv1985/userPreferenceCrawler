import pymongo

client = pymongo.MongoClient("localhost", 27017)
db = client.musicDistance
cursor = db.musicDistance.find()

i = 0
globalNearestDistance = 1.0
nearestPair = ['','']
for item in cursor:
    userId = item['userId']
    distanceList = item['distanceList']
    nearestDistance = 1.0
    nearestUser = ''
    for ele in distanceList:
        if ele['distance'] < nearestDistance:
            nearestDistance = ele['distance']
            nearestUser = ele['userId']
    print str(i) + ' The nearest neighbor of user ' + userId + ' is ' + nearestUser + ', with the distance of ' + str(nearestDistance)
    if nearestDistance < globalNearestDistance and nearestDistance > 0:
        globalNearestDistance = nearestDistance
        nearestPair[0] = userId
        nearestPair[1] = nearestUser
    i += 1
print nearestPair[0] + ' ' + nearestPair[1] + ' ' + str(globalNearestDistance)