#!/opt/python-2.5.2/bin/python2.5
# Nat Byington
# LING 572 HW9 TBL Learner
# Create a model file based on training data.

import sys
import re
from sets import Set

def find_best_rule(docs):
    '''Takes a list of documents and returns the rule with highest net gain.'''
    
    '''The return value is in the form of ((rule), net_gain). '''
    # rule_tally will track feature based rules. Each key will be in the form of
    # (feature, fromClass, toClass), and the value will be net gain.
    rule_tally = {}
    for doc in docs:
        true_class = doc[0]
        cur_class = doc[1]
        features = doc[2]
        if cur_class == true_class:
            for f in features:
                for c in CLASSES:
                    if c != true_class:
                        rule = (f, true_class, c)
                        if rule in rule_tally:
                            rule_tally[rule] -= 1
                        else:
                            rule_tally[rule] = -1
        else:
            for f in features:
                rule = (f, cur_class, true_class)
                if rule in rule_tally:
                    rule_tally[rule] += 1
                else:
                    rule_tally[rule] = 1
    # Sort rule_tally by values to find the rule with the highest net gain.
    rules = rule_tally.items()
    rules.sort(lambda x,y:cmp(x[1],y[1]), reverse=True) # sort by net gain
    return rules[0]

def transform(docs, rule):
    '''Change the given doc list according to the given rule.'''
    feature = rule[0]
    from_class = rule[1]
    to_class = rule[2]
    for doc in docs:
        if (doc[1] == from_class) and (feature in doc[2]):
            doc[1] = to_class


# Read file names from arguments.
training = open(sys.argv[1])
model_file = open(sys.argv[2], 'w')
MIN_GAIN = int(sys.argv[3])

DEFAULT_CLASS = 'guns'
CLASSES = Set([])

# Put each training document into a data structure for ease of processing.
# data struc: ['true class', 'current class', ([set of features])]
# doc_list contains list of these data structures
doc_list = []
for line in training.readlines():
    feature_set = Set([])
    doc = ['', DEFAULT_CLASS, feature_set]
    doc[0] = re.match(r'^[\S]+ ([\S]+) ', line).group(1) # true class
    if doc[0] not in CLASSES:
        CLASSES.add(doc[0])
    features = re.findall(r'([A-Za-z]+) [0-9]+', line) # list of features in doc
    for f in features:
        doc[2].add(f) # add feature to feature_set
    doc_list.append(doc)

model_file.write(DEFAULT_CLASS + '\n')

# Find best rules, add them to model file, transform, rinse & repeat.
proceed = True
while proceed:
    best_rule = find_best_rule(doc_list)
    x = best_rule[1] # net gain of best rule
    if x >= MIN_GAIN:
        output = ' '.join(best_rule[0])
        model_file.write(output + ' ' + str(x) + '\n')
        transform(doc_list, best_rule[0]) # change the doc_list according to rule
    else:
        proceed = False

