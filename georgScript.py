

alphabet = {}
f = open('alphabet.txt', 'r', encoding='utf-8')
for line in f:
    georg, ipa = line.split()
    alphabet[georg] = ipa

f.close()

f = open('georg.txt', 'r', encoding='utf-8')
w = open('georgIPA.txt', 'w', encoding='utf-8')

stringIPA = ''

for line in f:
    for ch in line:
        if ch in alphabet:
            stringIPA += alphabet[ch]
        else:
            stringIPA += ch
            print(ch)
    w.write(stringIPA)
    stringIPA = ''

w.close()
f.close()
