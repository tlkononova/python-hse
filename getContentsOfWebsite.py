import urllib.request
import re

def checkLink(url):
    if 'html' in url and '#' not in url and 'url=' not in url:
        if 'http' not in url:
            fullurl = myurl + url
        elif 'evening-kazan.ru' in url:
            fullurl = url
        else:
            return False, False
    else:
        return False, False

    if fullurl not in usedLinks:
        usedLinks.add(fullurl)
        html = openLink(fullurl)
        if html == False:
            return False, False
        else:
            return fullurl, html
    else:
        return False, False

    
def openLink(url):
    req = urllib.request.Request(url, data=None, headers={'User-Agent':
                                                         'Mozilla/5.0 (Windows NT 6.3; WOW64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.117 Safari/537.36'})

    f = urllib.request.urlopen(req)
    if f.getcode() == 200:
        html = f.read().decode('utf-8')
        return html
    else:
        return False


def getLinks(html):
    
    for link in re.findall("href=[\"\'](.[^\"\']+)[\"\']", html, re.I):
        check, content = checkLink(link)
        if check == False:
            continue
        else:
            fullurl = check

            w.write('\n link:\n')
            w.write(fullurl)

            urlStrip = re.sub('[./\\:\'\"%]', '-', fullurl)
            
            c = open(r'.\website contents\\'+urlStrip+'.txt', 'w', encoding='utf-8')
            c.write(content)
            c.close()
         
            getLinks(content)

    return None


myurl = "http://www.evening-kazan.ru"

html = openLink(myurl)

myurlStrip = re.sub('[./\\:\'\"%#]', '-', myurl)
c = open(r'.\website contents\\'+myurlStrip+'.txt', 'w', encoding='utf-8')
c.write(html)
c.close()

w = open('newsLinks.txt', 'w', encoding='utf-8' )

usedLinks = set()
getLinks(html)

w.close()   
