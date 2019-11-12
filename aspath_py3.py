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
out = open('aspath_result.txt', 'w')

for l in lines[5:]:
    tokens = re.split(r' [ ]+', l)
    if len(tokens) != 6: continue
    ases = tokens[-1].split(' ')
    ases = [a for a in ases if a.isdigit() and a!='0']
    out.write(' '.join(ases) + '\n')

out.close()

