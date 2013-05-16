__author__ = 'David F. Gleich and Yangyang Hou <hyy.sun@gmail.com>'

import sys
import os
from subprocess import call, check_call, Popen, PIPE, STDOUT
from check_time import checktime

"""
Given a directory in HDFS, run through the full listing of all files within
that directory and output any missing "ranges" as far as the file numbering
scheme goes. Also, output a warning if a file has the wrong size.
"""

left_dir = sys.argv[1] # this is the dir we wish to index

cmd = 'hadoop fs -ls '+ left_dir
print >>sys.stderr, "cmd=", cmd
p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
content = p.stdout.read()
files = content.split('\n') # now we have a list of files

def filename2fset(path):
    """ Convert a filename into a file-set number by finding the first 
    number in the path starting from the filename. 

    If we cannot find a path in the filename, return -1
    Any non-negative number returned indicates we found a file-set number
    """
    fdir,fname = os.path.split(path)
    if len(fname) == 0 and len(fdir) == 0:
        return -1
    fsetnum=''
    for i,c in enumerate(fname):
        if c.isdigit():
            fsetnum+=c
    if len(fsetnum) > 0:
        return int(fsetnum)
    else:
        return filename2fset(fdir)


memmap = {}

for file in files:
    file = file.split()
    if len(file) == 0: 
        continue
    
    fname = file[-1]
    fsize = int(file[4])

    if fname.endswith('.e'):
        # get the fset no
        fsetno = filename2fset(fname)
        memmap[fsetno] = fsize

lastfset = max(memmap.iterkeys())
maxsize = max(memmap.itervalues())

# we should have files running from 1 to lastfset
for i in xrange(1, lastfset+1):
    if i in memmap:
        if memmap[i] == 0:
            print "Run %4i: zero size"%(i)
        elif memmap[i] <= 0.99*maxsize:
            print "Run %4i: small size (%.2f vs. %.2f)"%(i, memmap[i]/1e6, maxsize/1e6)
    else:
        print "Run %4i: missing"%(i)

    
