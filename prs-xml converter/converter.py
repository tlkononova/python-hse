# -*- coding: utf-8 -*-
"""
Created on Wed Jun 01 02:04:39 2016

@author: TK_adm
"""
import sys
import csv
from bs4 import BeautifulSoup
import lxml.html


def writeana(ana, w):
    anaelements = ana.split('\t')
    #print type(anaelements)
    gram = ana.split('\t')[13]
    gram = gram.replace(' ', ',')
    #print type(gram)
    #print type(anaelements[9])
    #print anaelements[9]
    if anaelements[12] != '' and anaelements[13] != '':
        w.write('      <ana lex="'+anaelements[9]+'" gr="'+anaelements[12]+','+gram+'" trans="'+anaelements[10]+'" />\n')
    else:
        w.write('      <ana lex="'+anaelements[9]+'" gr="" trans="'+anaelements[10]+'" />\n')
    



def fromPRStoXML(prsfile): #maybe not print \n as part of punctuation???
    prs = open(prsfile, 'r')
    
    w = open (prsfile[:-4]+'_xml.xml', 'w')
    w.write('<body>\n')
    
    sentence = []
    linenno = 0
    sentno = 1
    wordno = 1
    for line in prs:
        
        linenno += 1
        if linenno == 1: 
            meta = line.split('\t') 
           
        elif linenno != 1 and len(line.split('\t')) == len(meta): #reading the main part
           
            if int(line.split('\t')[0]) == sentno: # inside the same sentence              
                sentence.append(line)
            else:                       
                w.write('  <se>\n')
                anas = []
                wordno = 1
                k = 1
                for word in sentence:
                    
                    if int(word.split('\t')[1]) == wordno: # versions of one word
                        anas.append(word)
                        wordprev = word
                                                
                        if k == len(sentence): #last word in a sentence
                        
                        # check for left punctuation
                            if wordprev.split('\t')[15]:
                                w.write('    '+wordprev.split('\t')[15]+'\n')
                                
                                
                            w.write('    <w>\n')
                            #print 'final anas '+str(len(anas))
                            for ana in anas:
                                writeana(ana, w)
                                
                            w.write('      '+wordprev.split('\t')[4]+'\n    </w>\n')
                            
                            # check for right punctuation
                            if wordprev.split('\t')[16]:
                                w.write('    '+wordprev.split('\t')[16]+'\n')
                        k += 1 #next word 
                    else:
                        
                        # check for left punctuation
                        if wordprev.split('\t')[15]:
                                w.write('    '+wordprev.split('\t')[15]+'\n')
                        w.write('    <w>\n')
                       
                        for ana in anas:
                            writeana(ana, w)
                            
                        w.write('      '+wordprev.split('\t')[4]+'\n    </w>\n')
                        
                        # check for right punctuation
                        if wordprev.split('\t')[16]:
                                w.write('    '+wordprev.split('\t')[16]+'\n')
                        wordno += 1
                        anas = []
                        anas.append(word)
                        wordprev = word
                        if k == len(sentence):
                            
                            # check for left punctuation
                            if wordprev.split('\t')[15]:
                                w.write('    '+wordprev.split('\t')[15]+'\n')
                                
                            w.write('    <w>\n')
                           
                            for ana in anas:
                                writeana(ana, w)
                               
                            w.write('      '+wordprev.split('\t')[4]+'\n    </w>\n')
                            
                            # check for right punctuation
                            if wordprev.split('\t')[16]:
                                w.write('    '+wordprev.split('\t')[16]+'\n')
                        k += 1
                w.write('  </se>\n')
                
                sentno += 1
                sentence = []
                sentence.append(line)
        
    w.write('</body>')
    
    w.close()



def checkPunct(punct):
    if punct !='\n':
        punct = punct.strip('\n')
        indent = 1
        while indent:
            if punct[0] == ' ':               
                punct = punct.strip()
            else:
                indent = 0
    else:
        punct = ''
    return punct

def fromXMLtoPRS(xmlfile):
        
    
    xml = open(xmlfile, 'r')
    docXML = xml.read()
       
    soup = BeautifulSoup(''.join(docXML), 'xml')
    
    rowDic = {}
    
    punctprev = ''
        
    with open(xmlfile[:-4]+'_prs.prs', 'w') as prsfile:
        
        fieldnames = ['#sentno','#wordno','#lang','#graph','#word','#indexword','#nvars','#nlems','#nvar','#lem','#trans','#trans_ru','#lex','#gram','#flex','#punctl','#punctr','#sent_pos']
        writer = csv.DictWriter(prsfile, fieldnames=fieldnames, delimiter = '\t', restval = '', lineterminator='\n')
    
        writer.writeheader()
        
        # inside sentence
        sentno = 0
        sentences = soup.findAll('se')
        for sent in sentences:
            sentno += 1
            
            # inside words
            wordno = 0
            words = sent.findAll('w')
            
            for wo in words:
                wordno += 1
                
                # get left punctuation
                punctl = ''
                punctl = wo.findPreviousSibling(text=True)
                punctl = checkPunct(punctl)
                
                    
                if punctl == punctprev:
                    punctl = ''
                print punctl
                
                # get right punctuation
                punct = ''
                punct = wo.findNextSibling(text=True)
                punct = checkPunct(punct)
            
                   
                   
                if wordno == 1:
                    sent_pos = 'bos'
                elif wordno == len(words):
                    sent_pos = 'eos'
                    
                else:
                    sent_pos = ''
                    
                # get lemmas
                anas = wo.findAll('ana')
                nvars = len(anas)
               
                nvar = 1
                lems = set()
                for ana in anas:
                    lem = ana['lex'].encode('utf-8')
                    lems.add(lem)
                    
                    # get word (token)
                    wordtext = ''
                    wordtext = ana.findNextSibling(text=True)
                    wordtext = checkPunct(wordtext)
                   
                    
                nlems = len(lems)
                
                # get data from ana
                for ana in anas:           
                    lem = ana['lex'].encode('utf-8')
                    #lems.add(lem)
                    #flex = ana['morph']
                    lexgram = ana['gr'].encode('utf-8')
                    lexgram = lexgram.split(',')
                    lex = lexgram[0]
                    
                    gram = ' '.join(lexgram[1:])
                    try:                       
                        morph = ana['morph'].encode('utf-8')
                        gram = ' '.join((gram, morph))
                    except:
                        gram = gram
                        
                    gram = gram.replace('.', ' ')
                    gram = gram.replace(',', ' ')
                    trans = ana['trans'].encode('utf-8')
                    
                    
                    graph = ''                    
                    if wordtext[0].isupper():
                        graph = 'cap'
                        
                    punctprev = punct
                    
                    # write line in prs file
                    
                    rowDic['#sentno'] = sentno
                    rowDic['#wordno'] = wordno
                    #rowDic['#lang'] 
                    rowDic['#graph'] = graph
                    rowDic['#word'] = wordtext.encode('utf-8')
                    #rowDic['#indexword']
                    rowDic['#nvars'] = nvars
                    rowDic['#nlems'] = nlems
                    rowDic['#nvar'] = nvar
                    rowDic['#lem'] = lem
                    rowDic['#trans'] = trans
                    #rowDic['#trans_ru']
                    rowDic['#lex'] = lex
                    rowDic['#gram'] = gram
                    #rowDic['#flex'] = *?
                    rowDic['#punctl'] = punctl
                    rowDic['#punctr'] = punct
                    rowDic['#sent_pos'] = sent_pos
                    
                    writer.writerow(rowDic)
                    rowDic = {}
                    
                    nvar += 1
               
    
def main(argv):
    
    '''Usage:
    #-h Help
    arg1 Input file
    arg2 Output format ('xml' or 'prs')    
    '''
		
    if len(argv) != 3:
        print(main.__doc__) # вызывает комментарии
    else: 
        inputfile = argv[1] 
        outputformat = argv[2]
        
        if outputformat == 'prs':
            fromXMLtoPRS(inputfile)
        elif outputformat == 'xml':
            fromPRStoXML(inputfile)
            
		
		
    
    
if __name__ == '__main__':
    main(sys.argv)
    