# -*- coding: utf-8 -*-
"""
concordancer for pashto wiki dump

Created on Mon Mar 14 17:28:25 2016

@author: TK_adm
"""

import re, os

def concordance(dirPath):

    punct = r'?؟!.,:;-–+_•“×%→ /\()�&÷…٪٫{}[]،"*؛»« '
    
    
    freqDic = {}
    
    for filename in os.listdir(dirPath):
        f = open(dirPath+filename, 'r', encoding='utf-8')
    
        for line in f:
            words = line.split()
            for word in words:
                if re.search('[a-zA-Zа-яА-Я<>=0-9]', word) != None:
                    continue
        
                wordS = word.strip(punct)
                wordS = wordS.strip(punct)
                
                if wordS in punct:
                    continue
                if wordS.isnumeric():
                    continue
                if wordS not in freqDic:
                    freqDic[wordS] = 1
                else:
                    freqDic[wordS] += 1
        f.close()
    #i = 1    
    w = open(dirPath+'concordance.tsv', 'w', encoding='utf-8')        
    dicSorted = sorted(freqDic.items(), key=lambda tup: tup[1], reverse=True)
    for word in dicSorted:
        w.write(word[0]+'\t'+str(word[1])+'\n')
        #i+=1    
    w.close()
    
def main():
    
    dirPath = '.\\pswiki\\extracted\\AA\\' #path to dir with extracted wiki files
    concordance(dirPath)
    

if __name__ == '__main__':
    main()    
