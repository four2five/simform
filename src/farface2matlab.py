"""
Convert output from the farface dump into a matlab file for future analysis.

This script has many hardcoded attributes. For instance, we assume that the
farface is on the grid [-0.05,0.05]x[-0.05x0.05] and has 129 points in that
region, such that we can convert to indexed locations via:

    yi = (y + 0.05)/(0.1/128)
    zj = (a + 0.05)/(0.1/128)
    
We also assume that all of the info for a file is localized.    

Usage:
hadoop fs -cat farface.txt/part-* | python farface2matlab.py farface.mat
"""

__author__ = 'David F. Gleich <dgleich@purdue.edu>'

import sys
import numpy
import scipy.io

def parse_line(line):
    line = line.replace('"','')
    line = line.replace('\\t','\t')
    line = line.split()
    return line
    
def parse_farface(f):
    F = numpy.zeros((129,129))
    yz = []
    
    def place_entry(parsed_line):
        y = float(parsed_line[2])
        z = float(parsed_line[3])
        yi = int(round((y + 0.05)/(0.1/128.)))
        zj = int(round((z + 0.05)/(0.1/128.)))
        F[yi,zj] = float(parsed_line[7]) # the last entry
        return (y,z)
          
    fset = None
    
    # read the other lines
    for i in xrange(129*129):
        line = parse_line(f.readline())
        if len(line) == 0:
            print "found empty line"
            if fset is None:
                return None
            else:
                assert(False)
        if fset is None:
            fset = int(line[0])
        assert fset == int(line[0]), \
            "when reading fset %i, the entry on line %i listed fset=%s"%(
            fset, i, line[0])
        y, z = place_entry(line)
        yz.append((y, z))
    
    return fset, F, yz    

def parse_lines(f):
    while 1:
        p = parse_farface(f)
        if p is not None:
            yield p
        else:
            return

def main():
    output = sys.argv[1]
    fsets = set()
    yzcoord = None
    with open(output,'wb') as f:
        for fset, F, yz in parse_lines(sys.stdin):
            print "Writing fset=%i"%(fset)
            scipy.io.savemat(f,{'farface%i'%(fset):F})
            assert(fset not in fsets)
            fsets.add(fset)
            yzcoord = yz
        yz = numpy.mat(yzcoord)
        scipy.io.savemat(f,{'yz':yz})
        
        fsetv = numpy.zeros(max(fsets))
        for fset in fsets:
            fsetv[fset-1] = 1.
        scipy.io.savemat(f,{'fsets':fsetv})
        
if __name__=='__main__':
    main()
        
        
            
    
    
