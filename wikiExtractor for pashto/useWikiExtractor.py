# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 17:28:25 2016

@author: TK_adm
"""

import os
import re

def extractWiki(filename, dirname):
    #path to the working dir
    dirPath = "C:\\Users\\TK_adm\\Documents\HSE\\comp_ling_progr\\python_adv\\wiki\\"
    
    inFile = dirPath+dirname+filename
    outDir = dirPath+dirname+"extracted\\"
    
    #path to python2
    python = '\"C:\\Users\\TK_adm\\Anaconda3\\envs\\snakes2\\python.exe '
    wiki = dirPath+'WikiExtractor.py '
    out = '-o '+outDir
    inp = ' '+inFile+'\"'
    print(python+wiki+out+inp)
    os.system(python+wiki+out+inp)



def main():
    #Pashto wiki dump
    dirname = 'pswiki\\'    
    filename = 'pswiki.bz2.xml'
    extractWiki(filename, dirname)


if __name__ == '__main__':
    main()    
