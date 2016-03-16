# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 23:03:14 2016

@author: TK_adm
"""

import re, os, lxml.html, urllib.request
import pymystem3
from pymystem3 import  Mystem


def getMetaData(html):

    tree = lxml.html.fromstring(html)
    
    try:
        category = tree.xpath('.//li[starts-with(@class, "taxonomy_term")]/a/text()')[0] 
    except:
        category = 'None'


    try:
        author = tree.xpath('.//div[@class="author heading--meta"]/text()')[0]
    except:
        author = 'Noname'

    try:
        date = tree.xpath('.//div[@class="submitted heading--meta"]/text()')[0]
    except:
        date = 'None'

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
                
        else:
             articleList = tree.xpath('.//div[@class="node"]//div[@class="content"]//p//text()')
             if articleList:
                 for p in articleList:
                     article += p
                     article += '\n'
            
             if not article or len(article)<5:            
                 article = None
                 
    except:
        article = None
        
        
    titleLem = 'None'
    if title != None:
        titleStrip = re.sub('[^\\w|\\s]', '', title)
        lemmas = m.lemmatize(titleStrip)
        titleLem = ''.join(lemmas[:-1])    


    year = 'None'
    if date != 'None':
        reg = re.search('\d+\.(\d+)\.(\d+)', date)
        #month = m.group(1)
        year = '20'+reg.group(2)    
        dateForm = reg.group(0)
        date = dateForm[:-2]+year
 

    metadata = ['PATH', author, '', '', title, titleLem, date, 'публицистика', '', '', category, '',
    'нейтральный', 'н-возраст', 'н-уровень', 'республиканская', 'URL', 'Вечерняя Казань',
    '', year, 'газета', 'Россия', 'республика Татарстан', 'ru', article]
    
    return metadata

def updateMeta(meta):

    for i in meta[:-2]:
        w.write(i+'\t')
    w.write(meta[-2])
    w.write('\n')
      
    return True
    
    
def writeArticle(meta, j):

    date = meta[6]

    reg = re.search('\d+\.(\d+)\.(\d+)', date)
    if reg != None:
        month = reg.group(1)
        year = reg.group(2)
    else:
        month = 'm'
        year = 'y'


    filename = '.\\test\\'+year+'\\'+month+'\\plain_text\\article'+str(j)+'.txt' 
    filename_lemm_txt = '.\\test\\'+year+'\\'+month+'\\lemmatized_txt\\article'+str(j)+'_lemm.txt'       
    filename_lemm_xml = '.\\test\\'+year+'\\'+month+'\\lemmatized_xml\\article'+str(j)+'_lemm.xml'
    
    meta[0] = filename    
    
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w", encoding='utf-8') as f:
        #meta data @@
        f.write('@au ')
        f.write(meta[1])
        f.write('\n')
        f.write('@ti ')
        f.write(meta[6])
        f.write('\n')
        f.write('@topic ')
        f.write(meta[10])
        f.write('\n')
        f.write('@url ')
        f.write(meta[16])
        f.write('\n')  
        # article text
    
        f.write(meta[-1])
        
    
    f.close()
    
    tmp = '.\\test\\tmp.txt'
    with open(tmp, "w", encoding='utf-8') as f:
        f.write(meta[-1])
    f.close()
    
    os.makedirs(os.path.dirname(filename_lemm_txt), exist_ok=True)   
    os.makedirs(os.path.dirname(filename_lemm_xml), exist_ok=True)
    
    os.system(r'C:\Installers\mystem.exe -icd '+tmp+' '+filename_lemm_txt)
    os.system(r'C:\Installers\mystem.exe -icd --format xml '+tmp+' '+filename_lemm_xml)
    j += 1    
    return meta, j


def checkLink(url):
    if url in usedLinks:
        return False, False
        
    if url == myurl or '.html' in url and '#' not in url and 'url=' not in url:
        if 'http' not in url:
            fullurl = myurl + url
        elif 'evening-kazan.ru' in url:
            fullurl = url
        else:
            return False, False
    else:
        return False, False

    if fullurl in usedLinks:
        return False, False
    usedLinks.add(fullurl)
    usedLinks.add(url)

    try:
        html = openLink(fullurl)
    except:
        print(fullurl)
        return False, False
    if html == False:
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
        

m = Mystem()
newLinks = []

j = 1

myurl = "http://www.evening-kazan.ru"
newLinks.append(myurl)

w = open(r'.\test\meta.tsv', 'w', encoding='utf-8')
w.write('path\tauthor\tsex\tbirthday\theader\theader_lemmatized\tcreated\tsphere\tgenre_fi\ttype\ttopic\tchronotop\tstyle\taudience_age\taudience_level\taudience_size\tsource\tpublication\tpublisher\tpubl_year\tmedium\tcountry\tregion\tlanguage\n')

usedLinks = set()

counter = 10000

while newLinks and counter:
    
    url = newLinks[0]
    newLinks = newLinks[1:]
   
    check, html = checkLink(url)
    if check == False:
        continue
    else:
        fullurl = check
 
    meta = getMetaData(html)
    meta[16] = fullurl

    if meta[4] != None and meta[-1] != None:
        meta, j = writeArticle(meta, j)
        updateMeta(meta)
        
    findLinks = set(re.findall("href=[\"\'](.[^\"\']+)[\"\']", html, re.I))
    findLinks = list(findLinks - usedLinks)
    newLinks.extend(findLinks)
    newLinks = list(set(newLinks))
    
    counter -= 1
  
w.close()
