from sys import stdin, argv
from itertools import ifilter, imap

struct = 0

unstruct_params = {}
struct_params = {}

def get_label(l, sl):
    if sl:
        return 'SL:%s' % l
    else:
        return l

def get_score(fields, unstruct_params, struct_params, sl):
    label_t_2 = get_label('_#_',sl)
    label_t_1 = get_label('_#_',sl)
    
    score = 0
    fields += [('',[],'','_#_'),('',[],'','_#_')]
    for i,fs in enumerate(fields):
        label = get_label(fs[3],sl)
        if i > 1:
            label_t_1 = get_label(fields[i-1][3], sl)
        if i > 2:
            label_t_2 = get_label(fields[i-2][3], sl)
        for feat_templ in fs[1]:            
            feat = "%s::%s" % (feat_templ, label)            
            if feat in unstruct_params:
                print ("%s %s" % (feat, unstruct_params[feat]))
                score += unstruct_params[feat]
                pass
        if label in struct_params:
            print ("%s %s" % (label, struct_params[label]))
            score += struct_params[label]
            pass
        blabel = "%s::%s" % (label_t_1,label)
        if blabel in struct_params:
            print ("%s %s" % (blabel, struct_params[blabel]))
            score += struct_params[blabel]
            pass
        tlabel = "%s::%s::%s" % (label_t_2,label_t_1,label)
        if tlabel in struct_params:
            print ("%s %s" % (tlabel, struct_params[tlabel]))
            score += struct_params[tlabel]
            pass
        label_t_2 = label_t_1
        label_t_1 = label

    return score

def print_score(fields, unstruct_params, struct_params):
    print (get_score(fields, unstruct_params, struct_params, 0) + 
           get_score(fields, unstruct_params, struct_params, 1))

for line in ifilter(lambda x: x != '', 
                    imap(lambda x: x.strip(), open(argv[1]))):
    if line == 'UNSTRUCTURED FEATURES':
        struct = 0
    elif line == 'STRUCTURED FEATURES':
        struct = 1
    else:
        if not struct:
            feat, label, param = line.split(' ')
            unstruct_params["%s::%s" % (feat, label)] = float(param)
        else:
            fields = line.split(' ')
            param = fields[-1]
            labels = fields[:-1]
            struct_params['::'.join(labels)] = float(param)

fields = []

for line in imap(lambda x: x.strip(), stdin):
    if line == '':
        print_score(fields, unstruct_params, struct_params)
        fields = []
    else:
        fields.append(line.split('\t'))
        fields[-1][1] = fields[-1][1].split(' ')

if fields != []:
    print_score(fields, unstruct_params, struct_params)
