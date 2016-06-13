import re, os#, urllib.request
import requests
import json
import codecs
import time
import datetime


def getUsersfromCity(cityid, access_token):
    line = 'https://api.vk.com/method/users.search?count=420&city='+str(cityid)+'&v=5.52&access_token='+access_token
    
    r = requests.get(line).text
    
    userjson = json.loads(r, encoding='utf-8')
    #print userjson
    userlist = userjson[u'response'][u'items']

    useridstring = ''
    for userdic in userlist:
        userid = userdic[u'id']
        
        useridstring += str(userid)
        useridstring +=','
    useridstring = useridstring[:-1]
    return useridstring

#[{userid: ..., bdate: ..., city: 991, sex: ..., wall:[{date: ..., text: ...}, {date: ..., text: ...}, ...]}, ...]
    
def getUserMeta(useridstring, alldata, access_token):   
# get user meta data
    
    line = 'https://api.vk.com/method/users.get?user_ids='+useridstring+'&fields=bdate,sex&v=5.52&access_token='+access_token
    r = requests.get(line).text
    #print r
    #print type(str(r))
    #print 'printing '+str(r)[1000:]
    userdata = json.loads(r, encoding='utf-8')
    
    #print userdata
    
    userdatalist = userdata[u'response']
    for user in userdatalist:
        userid = user[u'id']
        try:
            bdate = user[u'bdate']
        except:
            bdate = ''
        try:
            sex = user[u'sex']
        except:
            sex = ''
        alldata[userid] = {u'bdate':bdate, u'sex':sex, u'wall':[]}
        try:
            getwall(userid, alldata, access_token)
        except:
            alldata[userid]['wall'] = False
            print(userid)
        
    return alldata
    
    #for userid in userlist:
    #userid= '56649'
    
    #w = open('getwall.txt', 'w')
    


def getwall(userid, alldata, access_token):
    line = 'https://api.vk.com/method/wall.get?owner_id='+str(userid)+'&count=100&filter=owner&v=5.52&access_token='+access_token
    r = requests.get(line).text
    userwall = json.loads(r, encoding='utf-8')
    
    #print userwall
    
    walllist = userwall[u'response'][u'items']
    for data in walllist:
        #print data[u'text']
        #w.write(data["text"].encode('utf-8'))
        #w.write('\nnew\n')
        #alldata.append({'userid':userid, 'bdate':bdate, 'sex':sex, 'wall':[]})
        if data[u'text'] != '':
            date = datetime.datetime.fromtimestamp(int(data[u'date']))
            date = datetime.datetime.isoformat(date, sep=' ')
            #date = time.strftime("%D %H:%M", time.localtime(int(data[u'date'])))
            alldata[userid][u'wall'].append({u'date':date, u'text':data[u'text']})#.encode('utf-8')})
   
#userid = '56649'
#alldata[userid] = {'bdate':bdate, 'sex':sex, 'wall':[]}
#getwall(userid)


def writedata(alldata, cityid):
    w = open('usermeta_'+str(cityid)+'.csv', 'w', encoding='utf-8')
    f = open('alluserwall_'+str(cityid)+'.csv', 'w', encoding='utf-8')
    w.write('userid\tbirthdate\tsex\n')
    f.write('userid\tdate\ttext\n')
    os.mkdir('.\\walls_'+str(cityid))
    for user in alldata:
        if alldata[user]['wall']:
            w.write(str(user)+'\t')
            w.write(str(alldata[user]['bdate'])+'\t')
            w.write(str(alldata[user]['sex'])+'\n')
            t = open('.\\walls_'+str(cityid)+'\\'+str(user)+'.csv', 'w', encoding='utf-8')
            t.write('date\ttext\n')
            for text in alldata[user]['wall']:
                textprep = text['text'].replace('\n', '*new paragraph*')
                t.write(str(text['date'])+'\t'+textprep+'\n')
                f.write(str(user)+'\t'+str(text['date'])+'\t'+textprep+'\n')
            t.close()
        
    w.close()
    f.close()


def main():
    alldata = {}
    
    access_token='299ff2b8259d2c12b1a53c2b9b07cff7ec98de3b139b012b38f87688462dff9027343e9aa372c85f87f4e'
    
    # get users from the same city
    #cityid = 97
    cityid = 97 #Mozhaisk
    
    useridstring = getUsersfromCity(cityid, access_token)
    #print useridstring.encode('utf-8')
    getUserMeta(useridstring, alldata, access_token)
    
    #id3359999
    
    #write data in files
    writedata(alldata, cityid)
    '''
    w = open('usermeta.csv', 'w', encoding='utf-8')
    f = open('alluserwall.csv', 'w', encoding='utf-8')
    w.write('userid\tbirthdate\tsex\n')
    f.write('userid\tdate\ttext\n')
    for user in alldata:
        w.write(str(user)+'\t')
        w.write(str(alldata[user]['bdate'])+'\t')
        w.write(str(alldata[user]['sex'])+'\n')
        t = open('.\\walls\\'+str(user)+'_wall.csv', 'w', encoding='utf-8')
        t.write('date\ttext\n')
        for text in alldata[user]['wall']:
            textprep = text['text'].replace('\n', '*new paragraph*')
            t.write(str(text['date'])+'\t'+textprep+'\n')
            f.write(str(user)+'\t'+str(text['date'])+'\t'+textprep+'\n')
        t.close()
        
    w.close()
    f.close()
    '''
    #write texts
    '''
    w = open('userwall.txt', 'w', encoding='utf-8')
    
    w.write()
    w.write(json.dumps(alldata))
    w.close()
    '''
    
if __name__ == '__main__':
    main()
