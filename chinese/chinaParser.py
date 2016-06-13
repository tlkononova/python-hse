# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 18:55:08 2016

@author: TK_adm
"""

def annotate(word, dicentry, w):
    w.write('\n<w>')
    if type(dicentry) == list:
        wordList = dicentry
        for entry in wordList:
            transcr, sem = entry
            w.write('<ana lex = "'+word+'" transcr="'+transcr+'" sem="'+sem+'"/>')  
            
    else:
        transcr, sem = dicentry
        sem = sem.replace('"', "'")
        w.write('<ana lex = "'+word+'" transcr="'+transcr+'" sem="'+sem+'"/>')  
      
    w.write(word+'</w>')
    #<ana lex="节" transcr="jie1" sem="see_節骨眼|节骨眼[jie1_gu5_yan3]"/>

def createChineseDic(dicfile):
    Dict = {}
    #k =  0
    f = open(dicfile, 'r', encoding='utf-8')
    w = open('chin-eng.csv', 'w', encoding='utf-8')
    for line in f:
        #if k > 100:
            #break
        if line[0] == '#':
            continue
        splitLine = line.split()
        try: # in case there are faulty lines
            lex = splitLine[1]
        except:
            continue
        
        transcr = ''
        t = 0
        for word in splitLine:
            if word[0] == '[' and t == 0:
                transcr += word[1:]
                t = 1
                if word[-1] == ']':
                    break
            elif t == 1:
                transcr += (' '+ word)
                if word[-1] == ']':
                    
                    break
        transcr = transcr [:-1]         
        
        sem = ''
        s = 0
        for word in splitLine:
            if word[0] == '/' and s == 0 :
                sem += word[1:]
                s = 1
            elif s == 1:
                sem += (' '+ word)
        sem = sem[:-1]
        sem = sem.replace('/', ', ')
        
        #w.write(lex +'\t'+ transcr +'\t'+ sem+'\n')
        if lex not in Dict:
            Dict[lex] = (transcr, sem)
        else:
            if type(Dict[lex]) != list:
                sem1 = Dict[lex]
                Dict[lex] = []
                Dict[lex].append(sem1)
                Dict[lex].append((transcr, sem))
            else:
                Dict[lex].append((transcr, sem))
    
    f.close()  
    w.close()  
    return Dict

def proccessChinese(file2proccess, Dict):

    f = open(file2proccess, 'r', encoding='utf-8')
    w = open(file2proccess[:-4]+'_result.xml', 'w', encoding='utf-8')
    #k = 10
    for line in f:
    #while k:
        #line = f.readline()
        if line[:4] != '<se>':
            w.write(line)
            continue  
        else:
            w.write('<se>')
            
        chLine = line[4:-6]
        print('line to proccess: '+chLine)
        
        symbs = chLine
        procSymb = 0
        T = 1
        while T:
            for x in range(len(chLine)):
                if symbs in Dict:
                    print(symbs+' in!')                    
                    annotate(symbs, Dict[symbs], w)
                    procSymb += len(symbs)
                    break
                elif len(symbs) == 1 and symbs not in Dict:
                    print(symbs+' not in, just punct')
                    w.write(symbs)
                    #T = 0
                    procSymb += 1
                    break
                else:
                    print(symbs+' cut to')
                    symbs = symbs[:-1]
                    print(symbs)
            symbs = chLine[procSymb:]
            if procSymb == len(chLine):
                print('end line')
                break
        w.write('</se>\n')
        #k -= 1
    
    w.close()
    f.close()
    #dif meanings

def main():
    dicfile = 'cedict_ts.u8'
    Dict = createChineseDic(dicfile)
    file2proccess = 'stal.xml'
    proccessChinese(file2proccess, Dict)


if __name__ == '__main__':
    main()
