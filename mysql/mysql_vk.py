# -*- coding: utf-8 -*-
"""
Created on Sat Jun 11 02:18:31 2016

@author: TK_adm
"""
import pymysql
import csv

def main():    

    conn = pymysql.connect(host='localhost', user='guest1', password='n76Je4=wx6H', db='guest1_tk', charset='utf8mb4')
    
    cur = conn.cursor()
    
    try:
        cur.execute('create database guest1_VKTatianaKononova DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;')
    except:
        print('database already exists')
    cur.execute('use guest1_VKTatianaKononova;')
    
    
    path = ''
    with open(path+'usermeta_97.csv', 'r', encoding='utf-8') as csvf:
            
        cur.execute('create table VK_meta (userid INT(10), birthdate VARCHAR(10), sex INT(1), PRIMARY KEY(userid));')       
        
        meta = csv.DictReader(csvf, delimiter='\t')
        
        for row in meta:
            string="'"+str(row['userid'])+"','"+str(row['birthdate']+"','"+str(row['sex'])+"'")
            
            cur.execute('insert into VK_meta (userid, birthdate, sex) value ('+string+');')
    
    
    with open(path+'alluserwall_97.csv', 'r', encoding='utf-8') as csvf:
    
        cur.execute('create table VK_wall (userid INT(10), date VARCHAR(20), text VARCHAR(10000)) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;')       
        
        wall = csv.DictReader(csvf, delimiter='\t')
        
        for row in wall:
            
            string="'"+str(row['userid'])+"','"+str(row['date']+"','"+str(row['text'])+"'")
            
            try:
                cur.execute('insert into VK_wall (userid, date, text) value ('+string+');')
            except:
                print(str(row['text']))
    
    
            
    conn.commit()        
    cur.close()
    conn.close()
    
if __name__ == "__main__":
    main()