__author__ = 'Yangyang Hou <hyy.sun@gmail.com>'

import sys
import os
from subprocess import call, check_call, Popen, PIPE, STDOUT
from check_time import checktime

"""
Given a directory in HDFS, run through the full listing of all files within
that directory, and construct a map between the contents of "params.dat" and
the filename and filenumber.
"""

left_dir = sys.argv[1] # this is the dir we wish to index

tmpstr = left_dir[7:] # this removes hdfs://
index = tmpstr.find('/') # find the first path
prefix = left_dir[0:7]+tmpstr[0:index] # this builds the path

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
    file = file.split(' ')
    fname = file[len(file)-1]
    if fname.endswith('params.dat'):
        # get the fset no
        fsetno = filename2fset(fname)
        
        # read this file 
        cmd = 'hadoop fs -cat '+ fname
        print >>sys.stderr, "cmd=", cmd
        p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
        content = p.stdout.read()
        
        size = None
        seed = None
        
        lines = content.split('\n')
        for line in lines:
            parts = line.split()
            if len(parts) != 2: continue
            if parts[1] == 'size':
                size = float(parts[0])
            if parts[1] == 'seed':
                seed = parts[0] # keep seed with the original precision
        
        if size is None or seed is None:
            print >> sys.stderr, "Could not find size or seed in %s"%(fname)
        else:
            memmap[fsetno] = (size, seed)
            
for fsetno, params in memmap.iteritems():
    print "%i %.18e %s"%(fsetno, params[0], params[1])
    