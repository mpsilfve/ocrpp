#! /usr/bin/env python3

from cProfile import run

from sys import stdin, argv, stderr, stdout
from libhfst import HfstInputStream, regex, empty_fst, \
create_hfst_output_stream, TROPICAL_OPENFST_TYPE
from pickle import load

from compile_fst_model import escape, LS, CL, RL, NL

LMASS=0.999

def get_lcands(ichar, lcands, fixed_label = None):
    if not ichar in lcands:
        return [ichar]
    else:
        cands = []
        tot = 0
        for l, mass in lcands[ichar]:
            lc = '|'.join([s for s in l])
            if fixed_label != None and lc != fixed_label:
                continue
            cands.append(lc)

            tot += mass
            if tot >= LMASS:
                break
        return cands

def get_outputs(e, ustr_model):
    f_templates = e[1]
    labels = []
    for l in e[2]:
        score = 0
        for ft in f_templates:
            feat = ft + LS + l
            if feat in ustr_model:
                score += ustr_model[feat]
            if '|' in l:
                for sl in l.split('|'):
                    feat = ft + LS + 'SL:' + sl
                    if feat in ustr_model:
                        score += ustr_model[feat]
        labels.append([l, score])
    return labels

def get_symbs(o):
    ostr =  ' '.join([escape(l) for l in o.split('|')])
    if ' ' in ostr:
        ostr = CL + ' '  + ostr
    else:
        ostr = RL + ' ' + ostr + ' ' + NL
    return ostr
def remove_markers(p):
    p = p.replace('_#_','')
    p = p.replace('<LS>','')
    p = p.replace('<CL>','')
    p = p.replace('<RL>','')
    p = p.replace('<NL>','')
    p = p.replace('|','')
    p = p.replace('#','')
    p = p.replace('EPS','')
    return p

def get_top_outputs(outputs, str_model, top_n):
    fst = empty_fst()
    
    outputs = [[['_#_',0]]] * 2 + outputs + [[['_#_',0]]] * 2

    fst = regex("0")

    for os in outputs:
        os_fst = empty_fst()
        for o, score in os:
            o_fst = regex("%s %s::%f %s" % (LS, get_symbs(o), score, LS))
            os_fst.disjunct(o_fst)
        fst.concatenate(os_fst)
    fst.compose(str_model)
    fst.remove_epsilons()
    fst.determinize()
#    fst.minimize()
    fst.n_best(top_n)    

    paths = [(p[0][1], p[0][0]) for p in fst.extract_paths().values()]
    paths.sort()
    return [(remove_markers(p[1]), p[0]) for p in paths]

def display_results(entry, ustr_model, str_model, top_n):
    if entry != []:
        outputs = [get_outputs(e, ustr_model) for e in entry]
        top_outputs = get_top_outputs(outputs, str_model, top_n)
        for o, s in top_outputs:
            if o == '':
                print('EMPTY')
            else:
                print(o)
        print()
        stdout.flush()
        
def main():
    if len(argv) != 3:
        stderr.write('USAGE: cat inputs | %s model_prefix N' % argv[0])
        exit(1)
    lcands = load(open(argv[1] + '.lc','rb'))
    ustr_model = load(open(argv[1] + '.ustr', 'rb'))
    str_model = HfstInputStream(argv[1] + '.str').read()
    top_n = int(argv[2])

    entry = []
    counter = 0
    for line in map(lambda x: x.strip(), stdin):
        if line == '':
            counter += 1
            stderr.write("%u\r" % counter)
            display_results(entry, ustr_model, str_model, top_n)
            entry = []
        else:
            ichar, feats, _, label, _ = line.split('\t')
            if label == '_':
                entry.append((ichar, feats.split(' '), 
                              get_lcands(ichar, lcands)))
            else:
                entry.append((ichar, feats.split(' '), 
                              get_lcands(ichar, lcands, label)))
    stderr.write('\n')
    display_results(entry, ustr_model, str_model, top_n)

if __name__=='__main__':
    main()
