#!/opt/python-2.5.2/bin/python2.5
# Nat Byington
# LING 572 HW9 TBL Decoder
# Classifies test data using TBL rules from a model file.

import sys
import re
import time
from sets import Set


# Read arguments.
test = open(sys.argv[1])
model_file = open(sys.argv[2])
output = open(sys.argv[3], 'w')
N = int(sys.argv[4])

# Read model file to create list of TBL rules.
rules = [] # list of TBL rules
DEFAULT_CLASS = model_file.readline().strip()
x = 1
while x <= N:
    raw_rule = model_file.readline()
    if raw_rule:
        match = re.match(r'([A-Za-z]+) ([A-Za-z]+) ([A-Za-z]+) [0-9]+', raw_rule)
        rule = (match.group(1), match.group(2), match.group(3))
        rules.append(rule)
    x += 1

# Read test data, create data structure for each document.
# data struc: ['instance', 'true class', 'current class', ([set of features]), [list of transforms]]
# doc_list contains list of these data structures
doc_list = []
doc_count = 0
for line in test.readlines():
    feature_set = Set([])
    doc = ['', '', DEFAULT_CLASS, feature_set, []]
    doc[0] = re.match(r'^([\S]+) ([\S]+) ', line).group(1) # instance
    doc[1] = re.match(r'^([\S]+) ([\S]+) ', line).group(2) # true class
    features = re.findall(r'([A-Za-z]+) [0-9]+', line) # list of features in doc
    for f in features:
        doc[3].add(f) # add feature to feature_set
    doc_count += 1
    doc_list.append(doc)

# Transform docs based on rules.
for rule in rules:
    for doc in doc_list:
        if (rule[1] == doc[2]) and (rule[0] in doc[3]):
            doc[2] = rule[2] # transform current class
            doc[4].append(rule) # add to list of this doc's transformations

# Create output file and calculate accuracy.
correct_count = 0.0
for doc in doc_list:
    if doc[1] == doc[2]:
        correct_count += 1 # doc was correctly classified
    out_list = [doc[0], doc[1], doc[2]]
    for rule in doc[4]:
        t = ' '.join(rule)
        out_list.append(t)
    out = ' '.join(out_list)
    output.write(out + '\n')
print correct_count / doc_count

    
    
    
    
