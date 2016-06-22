#! /usr/bin/env python3

from sys import argv, stderr

ce = 0
ec = 0
cc = 0
ee = 0

def handle_zero(s):
    if s == '"0"':
        return '0'
    elif s == '0':
        return ''
    else:
        return s

def eval(input_word, sys_word, gold_word):
    global ce, ec, ee, cc

    orig_input_word = input_word
    orig_sys_word = sys_word
    orig_gold_word = gold_word

    input_word = ''.join([handle_zero(x) for x in input_word])
    sys_word = ''.join([handle_zero(x) for x in sys_word])
    gold_word = ''.join([handle_zero(x) for x in gold_word])

    if input_word == gold_word:
        if sys_word == gold_word:
            cc += 1
        else:
            ce += 1
    else:
        if sys_word == gold_word:
            ec += 1
        else:
            ee += 1

if len(argv) != 3:
    stderr.write('USAGE: %s sys_file gold_file\n' % argv[0])
    exit(1)

sys_file = open(argv[1])
gold_file = open(argv[2])

while 1:
    sys_line = sys_file.readline()
    gold_line = gold_file.readline()

    sys_line = sys_line.strip()
    gold_line = gold_line.strip()

    if sys_line == '' or gold_line == '':
        break
    sys_line = sys_line.strip()
    gold_line = gold_line.strip()
    
    sys_output = sys_line
    gold_input, gold_output = gold_line.split(' ')

    #assert(sys_input == gold_input)

    eval(gold_input, sys_output, gold_output)

print ("ec=%u ce=%u cc=%u ee=%u" % (ec, ce, cc, ee))
print ("Correction Rate (tp - fp) / (tp + fn): %.5f" % ((ec - ce)*1.0/(ec+ee)))
