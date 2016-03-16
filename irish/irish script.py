import re
import urllib.request

IrishDict = {}
forms = []

regLemma = '<h3 headword_id.+?>(.+\\s+)?(\\S+)<\/h3>'
regForms = 'Forms:\\s*(.+?)<\/p>'

# reading from web
'''
number = input('введите число от 1 до 43345 (например, 500): ')
f = urllib.request.urlopen('http://dil.ie/'+str(number))
text = f.read().decode('utf-8')
'''
# reading from file

f = open('irish word.txt', 'r', encoding='utf-8')
text = f.read()


resLemma = re.search(regLemma, text)
if resLemma != None:
    lemma = resLemma.group(2)

resForms = re.search(regForms, text)
if resForms != None:
    string = resForms.group(1)
    forms = string.split(sep=', ')
else:
    forms = lemma,
        
f.close()

for f in forms:
    IrishDict[f] = lemma

print(IrishDict)


'''
w = open('irish dict.txt', 'w', encoding='utf-8')
for form in IrishDict:
    entry = form+' -- '+IrishDict[form]
    w.write(entry+'\n')

w.close()
'''
