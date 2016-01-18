

alphabet = {}
f = open('amharic alph.tsv', 'r', encoding='utf-8')

c = 0

voc = []
cons = []

for line in f:
    line = line.strip('\n')
    line = line.split('\t')
    v = 0
    for ch in line:
        
        if c == 0 and v != 0:
            voc.append(ch)
        elif c != 0 and v == 0:
            cons.append(ch)
        elif c != 0 and v != 0:
            alphabet[ch] = cons[c-1]+voc[v-1]
        v += 1
    c += 1



f.close()

#print(alphabet)

f = open('amharic text.txt', 'r', encoding='utf-8')
w = open('amharic IPA.txt', 'w', encoding='utf-8')

stringIPA = ''

for line in f:
    for ch in line:
        if ch in alphabet:
            stringIPA += alphabet[ch]
        else:
            stringIPA += ch
    w.write(stringIPA)
    stringIPA = ''

w.close()
f.close()

