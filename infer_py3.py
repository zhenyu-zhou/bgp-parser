#!/usr/bin/env python3
'''
Created on Oct 2, 2019

@author: zzy
'''

import re
import subprocess
import sys

if len(sys.argv) != 2:
    print("Usage: %s <INPUT_FILE>" % (sys.argv[0]))
    sys.exit(-1)

cmd = 'bzcat %s' % (sys.argv[1])
lines = str(subprocess.check_output(cmd, shell=True)).split('\\n')
out = open('infer_result.txt', 'w')

neighbor = {}
for l in lines[5:]:
    tokens = re.split(r' [ ]+', l)
    if len(tokens) != 6: continue
    ases = tokens[-1].split(' ')
    ases = list(set([int(a) for a in ases if a.isdigit() and a!='0']))
    for i in range(len(ases)-1):
        a1 = ases[i]
        a2 = ases[i+1]
        if a1 not in neighbor: neighbor[a1] = []
        if a2 not in neighbor: neighbor[a2] = []
        neighbor[a1].append(a2)
        neighbor[a2].append(a1)
print('Step 1/3: Finish building neighbor (size %d)' % len(neighbor))

degree = {}
for a in neighbor:
    neighbor[a] = list(set(neighbor[a]))
    degree[a] = len(neighbor[a])

transit = {}
for l in lines[5:]:
    tokens = re.split(r' [ ]+', l)
    if len(tokens) != 6: continue
    ases = tokens[-1].split(' ')
    ases = list(set([int(a) for a in ases if a.isdigit() and a!='0']))
    max_degree = -1

    idx = -1
    for i in range(len(ases)):
        a = ases[i]
        if max_degree < degree[a]:
            max_degree = degree[a]
            idx = i
    assert(idx >= 0)
    for i in range(idx):
        x = ases[i]
        y = ases[i+1]
        if x not in transit:
            transit[x] = set()
        if y not in transit[x]:
            transit[x].add(y)
    for i in range(idx, len(ases)-1):
        x = ases[i+1]
        y = ases[i]
        if x not in transit:
            transit[x] = set()
        if y not in transit[x]:
            transit[x].add(y)
print('Step 2/3: Finish building DAG (size %d)' % len(transit))

for a1 in transit:
    for a2 in transit[a1]:
        if a2 in transit:
            t = a1 in transit[a2]
        else:
            t = False
            
        if t:
            out.write('Sibling-to-sibling %s %s\n' % (a1, a2))
        else:
            out.write('Customer-to-provider %s %s\n' % (a1, a2))
            out.write('Provider-to-customer %s %s\n' % (a2, a1))
print('Step 3/3: Finish relationship inference')

out.close()

