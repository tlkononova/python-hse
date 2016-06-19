# -*- coding: utf-8 -*-
"""
Created on Sun Jun 19 17:26:44 2016

@author: TK_adm
"""

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


def main():
    #dirpath = 'C:\\Users\\TK_adm\\Documents\\HSE\\comp_ling_progr\\python_adv\\kyrgyz lemmatizer\\kywiki\\'
    #morph = tokenizeGetMorph(dirpath)
    #getAffixes(morph)
    file2lemmatize = 'wiki2test.txt'
    lemmatize(file2lemmatize)
    
if __name__ == '__main__':
    main()