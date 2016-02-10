import re, os, lxml.html, urllib.request
import pymystem3
from pymystem3 import  Mystem


m = Mystem()
newLinks = []

i = 1
j = 2

def getMetaData(html):

    tree = lxml.html.fromstring(html)
    #category
    #<li class="taxonomy_term_93 first last">
    #<a href="/categories/ekonomika.html" rel="tag" title="">Экономика</a>
    #</li>

    
    try:
        category = tree.xpath('.//li[starts-with(@class, "taxonomy_term")]/a/text()')[0]
    #/locale[starts-with(@name, "en")]
    #div[@*[starts-with(name(), 'val')]]    
    except:
        category = 'None'

    #author
    #<div class="author heading--meta">Марина ЮДКЕВИЧ</div>
    try:
        author = tree.xpath('.//div[@class="author heading--meta"]/text()')[0]
    except:
        author = 'None'

    #date
    #<div class="submitted heading--meta">19.01.16 07:43</div>
    try:
        date = tree.xpath('.//div[@class="submitted heading--meta"]/text()')[0]
    except:
        date = 'None'

    #title
    #<h1 class="title title-story">Баланс «Ак Барс» банка приукрасили химически</h1>
    try:
        title = tree.xpath('.//h1[@class="title title-story"]/text()')[0]
    except:
        title = None
        
    
    article = ''
    try:    
        articleList = tree.xpath('.//span[starts-with(@class, "s")]/text()')
        if articleList:
            for p in articleList:
                article += p
                article += '\n'
                print('span type\n'+article[:50])
        else:
            article = tree.xpath('.//div[@class="content"]//p/text()')[0]
            
            if not article or len(article)<5:            
                article = None
                print('None')
            else:
                print('content\n'+article[:50])
    except:
        article = None
        #print(type(articleList))     
        #if articleList[0] == None:
            #print('empty')
            #article = tree.xpath('.//div[@class="content"]/p/text()')[0]
            #print(article)
        '''    
        for p in articleList:
            article += p
            article += '\n'
        print('span type\n'+article)
        '''
    #except:
        #article = None
        #print('except')
        '''
        try:        
            article = tree.xpath('.//div[@class="content"]/p/text()')[0]
            print('content type\n'+ article)
        except:
            article = None
        '''
    #print(type(article))    
    metadata = category, author, date, title, article 
    return metadata

def updateMeta(meta):
    for i in meta[:-1]:
        w.write(i+'\t')
        #if meta.index(i) != 0:
        #    w.write('\t'+i)
        #else:
        #    w.write(i)   
    #w.write('\n')
    title = meta[3]    
    titleStrip = re.sub('[^\\w|\\s]', '', title)

    lemmas = m.lemmatize(titleStrip)
    titleLem = ' '.join(lemmas)    
    w.write(titleLem)
    return True

def writeArticle(meta, j):
    html = meta[-1]
    title = meta[3]
    titleStrip = re.sub('[^\\w|\\s]', ' ', title)    
    #category = meta[0]
    date = meta[2]

    m = re.search('\d+\.(\d+)\.(\d+)', date)
    month = m.group(1)
    year = '20'+m.group(2)

    #os.path.normpath(path)
    '''    
    try:
        #filename = '.\kazan\\'+year+'\\'+month+'\\'+category+'\\'+titleStrip+'.txt'
        filename = '.\kazan\\'+year+'\\'+month+'\\'+titleStrip+'.txt'        
        w.write(filename+'\n')    
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w", encoding='utf-8') as f:
            f.write(html)
    except:
        print('failed to writeArticle name: '+titleStrip)
        #filename = '.\kazan\\'+year+'\\'+month+'\\'+category+'\\'+'article'+j+'.txt'
        filename = '.\kazan\\'+year+'\\'+month+'\\'+'article'+j+'.txt'        
        w.write(filename+'\n')    
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w", encoding='utf-8') as f:
            f.write(html)
        j += 1
    '''

    #filename = '.\kazan\\'+year+'\\'+month+'\\'+category+'\\'+'article'+j+'.txt'
    filename = '.\kazan\\'+year+'\\'+month+'\\'+'article'+str(j)+'.txt'        
    w.write(filename+'\n')    
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w", encoding='utf-8') as f:
        f.write(html)
    j += 1
    f.close()
    filename_tagged = filename[:-4]+'_tagged.txt'
    filename_xml = filename[:-4]+'.xml'
    os.system(r'C:\Installers\mystem.exe -icd '+filename+' '+filename_tagged)
    os.system(r'C:\Installers\mystem.exe -icd --format xml '+filename+' '+filename_xml)
    return j

'''
def writePage(url, html):
    urlStrip = re.sub('[./\\:\'\"%?=_]', '-', url)
    try:    
        s = open(r'.\kazan\other\\'+urlStrip+'.txt', 'w', encoding='utf-8')    
        s.write(html)    
    except:
        print('failed to writePage name: '+urlStrip)        
        s = open(r'.\kazan\other\\'+'name'+i+'.txt', 'w', encoding='utf-8')    
        s.write(html) 
        i += 1
    s.close()
'''
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
        html = openLink(fullurl)
    except:
        print(fullurl)
        return False, False
    if html == False:
        #print('4')
        return False, False
    else:
        return fullurl, html
    


def openLink(url):
    req = urllib.request.Request(url, data=None, headers={'User-Agent':
                                                         'Mozilla/5.0 (Windows NT 6.3; WOW64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.117 Safari/537.36'})

    f = urllib.request.urlopen(req)
    if f.getcode() == 200:
        html = f.read().decode('utf-8')
        return html
    else:
        print(url)
        return False
        



#myurls = ['','']
#myurls[0] = "http://www.evening-kazan.ru/articles/balans-ak-bars-banka-priukrasili-himicheski.html"
myurl = "http://www.evening-kazan.ru"
#url = 'http://www.evening-kazan.ru//articles//kak-ohranniki-kazanskogo-chopa-stali-zhertvami-dela-molodogvardeyca.html'
testurl = 'http://www.evening-kazan.ru/articles/broshennyh-v-tatarstane-35-cirkovyh-zhivotnyh-priyutili-na-avtobaze.html'
newLinks.append(myurl)
#newLinks.append(testurl)

os.makedirs(r'.\kazan\other', exist_ok=True)
w = open(r'.\kazan\meta.tsv', 'w', encoding='utf-8')
w.write('category\tauthor\tdate\ttitle\ttitle lemmatized\tpath\n')


usedLinks = set()
'''
req = urllib.request.Request(url, data=None, headers={'User-Agent':
                                                         'Mozilla/5.0 (Windows NT 6.3; WOW64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.117 Safari/537.36'})

f = urllib.request.urlopen(req)
html = f.read().decode('utf-8')
meta = getMetaData(html)
print(meta)
'''
#title = meta[3]
#print(re.sub('[\?.\"/\\:\'"%?=_«»]', ' ', title))

counter = 50

while newLinks:
    
    url = newLinks[0]
    newLinks = newLinks[1:]
   
    check, html = checkLink(url)
    if check == False:
        #print('doesn\'t check')
        continue
    else:
        fullurl = check
 
    meta = getMetaData(html)

    if meta[3] != None and meta[4] != None:
        updateMeta(meta)
        j = writeArticle(meta, j)
    #else:
        #print('write')
        #writePage(fullurl, html)
        
    findLinks = set(re.findall("href=[\"\'](.[^\"\']+)[\"\']", html, re.I))
    findLinks = list(findLinks - usedLinks)
    newLinks.extend(findLinks)
    newLinks = list(set(newLinks))
    
    #counter -= 1
  
w.close()
