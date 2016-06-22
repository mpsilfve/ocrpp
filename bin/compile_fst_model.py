#! /usr/bin/env python3

from sys import stdin, stderr, argv

from libhfst import empty_fst, regex, fst, create_hfst_output_stream, \
                    TROPICAL_OPENFST_TYPE
from pickle import dump

STRUCTID = 'STRUCTURED FEATURES'
UNSTRUCTID = 'UNSTRUCTURED FEATURES'
LS = '"<LS>"'
CL = '"<CL>"' 
RL = '"<RL>"' 
NL = '"<NL>"'
ENUM=1
def escape(s):
    if s == '0':        
        return 'EPS'
    elif s == '"0"':
        return s
    elif s == '"%"':
        return '"%"'
    elif s == '%"' or s == '"':
        return '%"'
    else:
        return '"%s"' % s.replace(' ','" "')

def get_struct_center(l_string, weight):
    l_string = l_string.replace('|', ' ')

    if 'SL:' in l_string:
        l_string = l_string[3:]
        return ("%s -> [%s]::%f ||" % (escape(l_string),escape(l_string),weight),
                "%s %s (\%s) _ (\%s) %s" % (LS,
                                            CL,
                                            LS,
                                            LS,
                                            LS))
    elif ' ' in l_string:
        return ("%s -> [%s]::%f ||" % (escape(l_string),escape(l_string),weight),
                "%s %s _ %s" % (LS,
                                CL,
                                LS))
    else:
        return ("%s -> [%s]::%f ||" % (escape(l_string),escape(l_string),weight),
                "%s %s _ %s %s" % (LS,
                                   RL,
                                   NL,
                                   LS))

def get_label_context(l_string):
    l_string = l_string.replace('|', ' ')
    if 'SL:' in l_string:
        l_string = l_string[3:]
        return "%s %s (\%s) %s (\%s) %s" % (LS,
                                            CL,
                                            LS,
                                            escape(l_string),
                                            LS,
                                            LS)
    elif ' ' in l_string:
        return "%s %s %s %s" % (LS,
                                CL,
                                escape(l_string),
                                LS)
    else:
        return "%s %s %s %s %s" % (LS,
                                   RL,
                                   escape(l_string),
                                   NL,
                                   LS)

def get_struct_feat(labels, weight):
    center_label = labels[-1]
    center, center_context = get_struct_center(center_label, weight)

    context_labels = labels[:-1]
    left_context = ' '.join([get_label_context(l) for l in context_labels])

    rule_str = ' '.join([center, left_context, center_context])

    return regex(rule_str), rule_str

if __name__=='__main__':
    is_structured = 0
    
    unstructured_model = {}

    structured_rules = regex('?*')
    structured_model = regex('?*')

    oustr = open(argv[1] + '.ustr','wb')

    ostr = create_hfst_output_stream(argv[1] + '.str',
                                     TROPICAL_OPENFST_TYPE, 
                                     1)

    seen_struct_feats = set()

    for i, line in enumerate(map(lambda x: x.strip(), stdin)):
        if line == '':
            continue
        if line == STRUCTID:
            stderr.write("Structured features.\n")
            is_structured = 1
        elif line == UNSTRUCTID:
            stderr.write("Unstructured features.\n")
            is_structured = 0
        else:
            if is_structured:
                fields = line.split(' ')
                weight = -float(fields[-1])/ENUM
                labels = fields[:-1]
                struct_feat, struct_feat_str = get_struct_feat(labels, weight)
                if not struct_feat_str in seen_struct_feats:
                    if not struct_feat :
                        print(struct_feat_str, line)
                    structured_rules.compose(struct_feat)
                else:
                    stderr.write('skipping: %s \n' % struct_feat_str) 
                seen_struct_feats.add(struct_feat_str)
                structured_rules.minimize()
                
                if i % 100 == 0:
                    stderr.write('\n')
                    stderr.write('Composing...\n')
                    structured_model.compose(structured_rules)
                    structured_model.minimize()
                    stderr.write('Done. Fst model size %u\n' % 
                                 structured_model.number_of_states())
                    structured_rules = regex('?*')
            else:
                ft_string, l_string, weight_str = line.split(' ')
                weight = -float(weight_str)/ENUM

                unstructured_model["%s%s%s" % (ft_string, LS, l_string)] = \
                    weight

            stderr.write('LINE: %u\r' % i)

    print()
    print('Composing...')
    structured_model.compose(structured_rules)
    structured_model.minimize()
    print('Done. Size %u' % 
          structured_model.number_of_states())
    
    dump(unstructured_model, oustr)
    ostr.write(structured_model)
    
