__author__ = 'Yangyang Hou <hyy.sun@gmail.com>'

import sys
import os
from subprocess import call, check_call, Popen, PIPE, STDOUT
from check_time import checktime

# Put the file names in a text file as the inputfile
# Assume that all files have been uploaded in the hadoop cluster 
# dir should be a hdfs directory

left_dir = sys.argv[1]
right_path = sys.argv[2]
var = sys.argv[3]
inputfile = sys.argv[4]

tmpstr = left_dir[7:]
index = tmpstr.find('/')
prefix = left_dir[0:7]+tmpstr[0:index]

cmd = 'hadoop fs -ls '+ left_dir
p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
content = p.stdout.read()
files = content.split('\n')

newpath = False
dirs2 = [] # These are directories that already exist in the output path
if call(['hadoop', 'fs', '-test', '-e', right_path]) == 0:
    cmd = 'hadoop fs -ls '+ os.path.join(right_path)
    p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
    content = p.stdout.read()
    dirs1 = content.split('\n')
    dirs1 = dirs1[:len(dirs1)-1]
    for i, dir in enumerate(dirs1):
        if not dir.startswith('Found'):
            basename = os.path.basename(dir)
            if basename != var:
                #print basename
                dirs2.append(basename)
else:
    newpath = True
print newpath
tmpfile = open(os.path.join('./', 'input.txt'),'w')

for file in files:
    file = file.split()
    if len(file) == 0: continue
    fname = file[-1] # get last entry
    if fname.endswith('.e'):
        fsize = int(file[4])
        print "Processing %s"%(fname)
        if fsize == 0:
            print >> sys.stderr, "Skipping file %s because of zero size"%(fname)
            continue
        basename = os.path.basename(fname)
        ind = basename.rfind('.')
        basename = basename[0:ind]
        outdir = os.path.join(right_path, basename)
        fname = prefix + fname
        result = True
        # only check it it exists if it isn't entirely a new path
        if newpath is False and call(['hadoop', 'fs', '-test', '-e', outdir]) == 0:
            #print outdir
            dirs2.remove(basename) # this is an existing directory 
                                   # we don't need to delete
            result = checktime(fname, outdir)
            if result:
                check_call(['hadoop', 'fs', '-rmr', outdir])
        if result:
            tmpfile.write("%s\n" % fname)
  
tmpfile.close()

for dir in dirs2:
    check_call(['hadoop', 'fs', '-rmr', os.path.join(right_path, dir)])

#inputfile = os.path.join(right_path,'input.txt')
if call(['hadoop', 'fs', '-test', '-e', inputfile]) == 0:
    check_call(['hadoop', 'fs', '-rm', inputfile])
check_call(['hadoop', 'fs', '-copyFromLocal', os.path.join('./','input.txt'), inputfile])

check_call(['rm', os.path.join('./', 'input.txt')])
