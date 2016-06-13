# -*- coding: utf-8 -*-
"""
Created on Sat Jun 11 02:18:31 2016

@author: TK_adm
"""

import pymysql
import csv
#connect server
#conn = pymysql.connect(host='localhost' (if local)//ip(if not), 
	#user='guest1', password='n76Je4=wx6H', db='guest1_tk', charset='utf8')

conn = pymysql.connect(host='localhost', user='guest1', password='n76Je4=wx6H', db='guest1_tk', charset='utf8')

cur = conn.cursor()
'''
cur.execute('create table'+var+';') #sql command

Извлечение из базы данных
cur.execute('select ....')
result = cur.fetchall()
print(result)

for r in cur.execute(...):
	print(r)
	
print(cur.description)
'''

#import csv
#path = 'C:\\Users\\TK_adm\\Documents\\HSE\\comp_ling_progr\\python_adv\\api\\vk auth\\vk_api_auth-master\\'

#cur.execute('DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci')
#ALTER TABLE table_name CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

#try:
    #cur.execute('create database guest1_VKTatianaKononova;')
#except:
    #print('database already exists')
cur.execute('use guest1_VKTatianaKononova;')

path = ''
with open(path+'usermeta_97.csv', 'r', encoding='utf-8') as csvf:
    #meta = csv.reader(csv, delimiter='\t')
    #for row in meta:
        
    cur.execute('create table VKmeta (userid INT(10), birthdate VARCHAR(10), sex INT(1), PRIMARY KEY(userid));')       
    meta = csv.DictReader(csvf, delimiter='\t')
    for row in meta:
        string="'"+str(row['userid'])+"','"+str(row['birthdate']+"','"+str(row['sex'])+"'")
        #print (string)
        cur.execute('insert into VKmeta (userid, birthdate, sex) value ('+string+');')


with open(path+'alluserwall_97.csv', 'r', encoding='utf-8') as csvf:

    cur.execute('create table VKwall (userid INT(10), date VARCHAR(20), text VARCHAR(10000)) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;')       
    wall = csv.DictReader(csvf, delimiter='\t')
    for row in wall:
        
        string="'"+str(row['userid'])+"','"+str(row['date']+"','"+str(row['text'])+"'")
        #print (string)
        try:
            cur.execute('insert into VKwall (userid, date, text) value ('+string+');')
        except:
            print(str(row['text']))


        
conn.commit()        
cur.close()
conn.close()

#insert into VKmeta (userid, birthdate, sex) value ('5823804','25.6.1987','1');