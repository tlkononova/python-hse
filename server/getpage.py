# -*- coding: utf-8 -*-
"""
Created on Thu Jun 02 19:07:58 2016

@author: TK_adm
"""
import urllib.request
import re



def checkLink(url):
    if url in usedLinks:
        #print('1')
        return False, False
        
    if url == myurl or '.html' in url and '#' not in url and 'url=' not in url:
        if 'http' not in url:
            fullurl = myurl + url
        elif 'evening-kazan.ru' in url:
            fullurl = url
            #print('check1 ok')
        else:
            #print('2')
            return False, False
    else:
        #print('3')
        return False, False

    if fullurl in usedLinks:
        return False, False
    usedLinks.add(fullurl)
    usedLinks.add(url)
    #s.write(fullurl)
    try:
        html = openurl(fullurl)
    except:
        #print(fullurl)
        return False, False
    if html == False:
        #print('4')
        return False, False
    else:
        return fullurl, html
    


def openurl(url):
    req = urllib.request.Request(url, data=None, headers={'User-Agent':
                                                             'Mozilla/5.0 (Windows NT 6.3; WOW64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.117 Safari/537.36'})
    
    f = urllib.request.urlopen(req)
    

    if f.getcode() == 200:
        html = f.read().decode('utf-8')
        return html
    else:
        #print(url)
        return False
        

#counter = 0
newLinks = []
myurl = "http://www.evening-kazan.ru"
newLinks.append(myurl)    
    
usedLinks = set()

counter = 3



while newLinks and counter:
    
    url = newLinks[0]
    newLinks = newLinks[1:]
   
    check, html = checkLink(url)
    if check == False:
        #print('doesn\'t check')
        continue
    else:
        url = check
        w = open('page_'+str(4-counter)+'.txt', 'w', encoding='utf-8')
        w.write(url+'\n')
        w.write(html)
        w.close()
        #print(counter)
        counter -= 1
    #meta[16] = fullurl

    #if meta[4] != None and meta[-1] != None:
        #meta, j = writeArticle(meta, j)
        #updateMeta(meta)
    #else:
        #print('write')
        #writePage(fullurl, html)
        
    findLinks = set(re.findall("href=[\"\'](.[^\"\']+)[\"\']", html, re.I))
    #print(len(findLinks))
    findLinks = list(findLinks - usedLinks)
    newLinks.extend(findLinks)
    newLinks = list(set(newLinks))
    #print(len(findLinks))
    
    #counter -= 1
  
#w.close()    
    
    
