# -*- coding: utf-8 -*-
"""
Created on Wed Jun 15 13:01:05 2016

@author: TK_adm
"""
import json
import os
#morph = {}
#morphset = set()
#morphset1 = set()
#morphset2 = set()


#filename = 'kywiki-20160501-pages-articles-multistream.xml'


def tokenizeGetMorph(extractedwikiDir):
#path to extracted wiki
    #dirpath = 'C:\\Users\\TK_adm\\Documents\\HSE\\comp_ling_progr\\python_adv\\kyrgyz lemmatizer\\kywiki\\'
    dirpath = extractedwikiDir
    morph = {}
    punct = r'?؟!.,:;-–+_•“×%→ /\()�&÷…٪٫{}[]،"*؛»« '
    l = open('kywiki_token.txt', 'w', encoding='utf-8') 
    for d, dirs, files in os.walk(dirpath):
        
        for f in files:
            filename = os.path.join(d,f) 
            
            with open(filename, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.startswith('</doc') or line.startswith('<doc'):
                        continue
                    cleanline = line.replace('<br>','')
                    words = cleanline.split()
                    for w in words:
                        #count = 1
                        word = w.strip(punct)
                        word = word.strip(punct)
                        l.write(word+' ')
                        for x in range(3,len(word)):
                            if word[x:] not in morph:
                                morph[word[x:]] = 1
                            else:
                                morph[word[x:]] += 1
    l.close()
    f.close()
    
    return morph
    
def getAffixes(morph):
    morph = morph
    morphset = set()
    
    #for m in morph:
        #a.write(str(m)+'='+str(morph[m])+', ')
    
    #a.write('\n\nget affix\n\n')
    
    #s0 = open('kywiki_lemm_s0.txt', 'w') 
    #s1 = open('kywiki_lemm_s1.txt', 'w') 
    #s2 = open('kywiki_lemm_s2.txt', 'w') 
    with open('kywiki_token.txt', 'r', encoding='utf-8') as f:
        for line in f:
            #if line.startswith('</doc') or line.startswith('<doc'):
                #continue
    
                
        #for line in f:
            words = line.split()
            #k = 0
            for word in words:
                #count = 1
                #count1 = 1
                #score1 = 0
                #count2 = 1
                #score2 = 0
                #word = w.strip(punct)
                #word = word.strip(punct)
                prevfreq = 0
                #prevscore1 = 0
                #prevscore2 = 0
                if len(word)>3:
                    for x in range(3,len(word)):
                        freq = morph[word[x:]]
                        #score1 = freq*(len(word)-x)
                        #score2 = freq+(len(word)-x)
                        if freq > prevfreq*50 and prevfreq != 0:
                            morphset.add(word[x:])
                            #a.write(word+', aff: '+word[x:]+', f: '+str(freq)+', pf: '+str(prevfreq)+'\n')
                            
                            #if k < 100000:
                                #a.write(str(freq)+'>'+str(prevfreq)+' ')
                                #k+=1
        
                            '''
                            if count:
                                #s0.write(word[:x]+'$'+word[x:]+' ')
                                count -= 1
                            if score1 > prevscore1*1.5 and prevscore1 != 0 and count1:
                                #s1.write(word[:x]+'$'+word[x:]+' ')
                                count1 = 0
        
                            if score2 > prevscore2*1.5 and prevscore2 != 0 and count2:
                                #s2.write(word[:x]+'$'+word[x:]+' ')
                                count2 = 0
                            '''
                        prevfreq = freq
                    #prevscore2 = score2
                    #prevscore1 = score1
          
    #s0.close()
    #s1.close()
    #s2.close()
    
    #a.write('\n\n\final listn\n')
    #w.write(json.dumps(morphset, encoding='utf-8')) 
    print(len(morphset))
    a = open('affixes.txt', 'w', encoding='utf-8')
    for m in morphset:  
        a.write(str(m)+' ')#, encoding='utf-8'))                
    a.close()


'''
def lemmatize(filename):
    a = open('affixes.txt', 'r', encoding='utf-8')
    aff = a.read()
    affixes = set(aff.split())
    
    #filename = 'wiki2test.txt'                
    r = open(filename[:-4]+'_lemm.txt', 'w', encoding='utf-8')
    f = open(filename, 'r', encoding='utf-8')
    
    punct = r'?؟!.,:;-–+_•“×%→ /\()�&÷…٪٫{}[]،"*؛»« '
    for line in f:
        if line.startswith('</doc') or line.startswith('<doc'):
            continue
        cleanline = line.replace('<br>','')
        words = cleanline.split()
        for w in words:
            #count = 1
            word = w.strip(punct)
            word = word.strip(punct)
            k = 0
            if len(word)>3:
                for x in range(3,len(word)):
                    if word[x:] in affixes:
                        r.write(word[:x]+'$'+word[x:]+' ')
                        k = 1
                        break
            if k == 0:
                r.write(word)
    r.close()
    f.close()
'''

def main():
    dirpath = 'C:\\Users\\TK_adm\\Documents\\HSE\\comp_ling_progr\\python_adv\\kyrgyz lemmatizer\\kywiki\\'
    morph = tokenizeGetMorph(dirpath)
    getAffixes(morph)
    #file2lemmatize = 'wiki2test.txt'
    #lemmatize(file2lemmatize)
    
if __name__ == '__main__':
    main()