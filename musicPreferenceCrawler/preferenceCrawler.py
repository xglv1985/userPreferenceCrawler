import urllib2
from BeautifulSoup import *
from urlparse import urljoin
import pymongo
import time

class crawler:
    def __init__(self):
        self.mongodbInit()
        
    def mongodbInit(self):
        self.client = pymongo.MongoClient("localhost", 27017)
        
    def getMusciPreferenceDb(self):
        db = self.client.musicpreference
        return db.musicpreference
    
    def isUserInDb(self, userId):
        userNum = self.getMusciPreferenceDb().count({"userId" : userId})
        return userNum > 0
    
    def person2music(self, url):
        print url
        name = getNameFromMusicCollect(url)
        hobby = []
        try:
            c = urllib2.urlopen(url)
        except:
            print "Could not open %s" % url
            return
        try:
            soup = BeautifulSoup(c.read())
        except:
            print "Unicode error %s" % url
            return
        links = soup('a')
        for link in links:
            if not link.has_key('title'):
                continue
            linkUrl = link['href']
            if linkUrl.find("https://music.douban.com/subject/") != -1: 
                print '    ' + linkUrl
                hobby.append(getMusicIdFromMusicUrl(linkUrl))
        self.getMusciPreferenceDb().insert_one({"userId": name, "hobbyList": hobby})
    
    def crawl(self, pages, depth = 10):
        visited = set()
        for i in range(depth):
            newpages = set()
            for page in pages:
                visited.add(page)
                userId = getNameFromUserSite(page)
                if self.isUserInDb(userId):
                    print 'userId is visited db %s' % userId
                    continue
                retryTime = 0
                while retryTime < 10:
                    try:
                        c = urllib2.urlopen(page)
                        break;
                    except:
                        print "Could not open without login %s" % page
                        time.sleep(3)
                        continue
                try:
                    soup = BeautifulSoup(c.read())
                except:
                    print "Unicode error %s" % page
                    continue
                
                links = soup('a')
                for link in links:
                    linkUrl = link['href']
                    if linkUrl.find("https://music") != -1 and linkUrl.find("collect") != -1: 
                        self.person2music(linkUrl)
                    if isPersonSite(linkUrl) and linkUrl not in visited:
                        newpages.add(linkUrl)
                        
            pages = newpages
            
def isPersonSite(url):
    prefix = "https://www.douban.com/people/"
    if url.find(prefix) == -1:
        return False
    mid = url.split(prefix)
    suffix = mid[1]
    if suffix == '':
        return False
    res = suffix.split('/')
    if (len(res) == 1) or (len(res) == 2 and res[1] == ''):
        return True
    return False

def getNameFromUserSite(url):
    prefix = "https://www.douban.com/people/"
    res = url.split(prefix)
    suffix = res[1]
    nameList = suffix.split('/')
    
    return nameList[0]

def getNameFromMusicCollect(url):
    prefix = "https://music.douban.com/people/"
    res = url.split(prefix)
    suffix = res[1]
    nameList = suffix.split('/collect')
    
    return nameList[0]

def getMusicIdFromMusicUrl(url):
    prefix = "https://music.douban.com/subject/"
    res = url.split(prefix)
    suffix = res[1]
    nameList = suffix.split('/')
    
    return nameList[0]
            
def main():
    crawle = crawler()
    crawle.crawl(['https://www.douban.com/people/fengs/'])

if __name__ == '__main__':
    main()