#! /usr/bin/env python3

#import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')

from sys import stdin, stderr
import re
from re import match

def tok(chars):
    return [tok for tok in re.split('("0"|%.|.)', chars, re.UNICODE) if tok != '']

def extract_feats(input_word, gold_word):
    if len(input_word) != len(gold_word):
        print(input_word + " " + gold_word)
        exit(1)

    if len(input_word) == 0:
        return

    iletters = []
    gletters = []

    if match("<.*[|].*>", input_word[0]):
        for i_and_g in input_word:
            i_and_g = i_and_g[1:-1]
            i, g = i_and_g.split('|')
            iletters.append(i)
            gletters.append(g)

    for i in range(len(input_word)):
        il = input_word[i]
        gl = '|'.join(tok(gold_word[i]))
#        gl = gold_word[i]

        feats = []
        f1 = 'FEAT1:' + input_word[i]
        feats.append(f1)
        if len(input_word[i-1:i+1]) == 2:
            f2 = 'FEAT2:' + ''.join(input_word[i-1:i+1])
            feats.append(f2)
        if len(input_word[i:i+2]) == 2:
            f3 = 'FEAT3:' + ''.join(input_word[i:i+2])
            feats.append(f3)
        if len(input_word[i-1:i+2]) == 3: 
            f4 = 'FEAT4:' + ''.join(input_word[i-1:i+2])
            feats.append(f4)
        if len(input_word[i-2:i+1]) == 3: 
            f5 = 'FEAT5:' + ''.join(input_word[i-2:i+1])
            feats.append(f5)
        if len(input_word[i:i+3]) == 3:
            f6 = 'FEAT6:' + ''.join(input_word[i:i+3])
            feats.append(f6)        
        if len(input_word[i+1:i+4]) == 3:
            f7 = 'FEAT7:' + ''.join(input_word[i+1:i+4])
            feats.append(f7)
        if len(input_word[i-3:i]) == 3:
            f8 = 'FEAT8:' + ''.join(input_word[i-3:i])
            feats.append(f8)

        print('%s\t%s\t%s\t%s\t%s' % (il, ' '.join(feats), il, gl, '_'))

    print('')

if __name__=='__main__':
    gold_word = ['#']
    input_word = ['#']

    for line in stdin:
        line = line.strip()

        if line == '':
            input_word.append('#')
            gold_word.append('#')
            extract_feats(input_word, gold_word)
            input_word = ['#']
            gold_word = ['#']
        else:
            input_l, _sep, gold_l = line.split(' ')
            
            gold_word.append(gold_l)
            input_word.append(input_l)
            
